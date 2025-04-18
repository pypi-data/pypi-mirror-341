# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

import datetime
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    execution_weight = fields.Selection(
        [
            ("budget", "En base al presupuesto de la tarea [nuevo campo en tareas]"),
            ("hours", "En base a las horas calculadas"),
            ("none", "No se autocalcula"),
        ],
        string="Como valoramos cada tarea?",
        default="budget",
    )
    total_budget = fields.Float("Presupuesto Total",related="last_authomatic_update_id.total_budget", store=True, tracking=True)
    hourly_price = fields.Monetary("Precio Horario", tracking=True, default=0, group_operator = False)
    last_update_execution_pcnt = fields.Float("Ejec. %",
        related="last_authomatic_update_id.progress", store=True
    )
    last_update_execution_amount = fields.Monetary( "Ejecución Total",
        related="last_authomatic_update_id.total_execution", store=True
    )
    last_update_total_hours = fields.Float( "Horas gastadas", 
        related="last_authomatic_update_id.total_hours", store=True
    )
    last_update_material_expenses = fields.Monetary("Gastos materiales",
        related="last_authomatic_update_id.material_expenses", store=True
    )
    last_update_total_incomes = fields.Monetary("Ingresos",
        related="last_authomatic_update_id.total_incomes", store=True
    )
    allocated_hours = fields.Float(
        string="Horas reservadas", compute="_compute_allocated_hours"
    )
    hourly_expenses = fields.Monetary("Gastos Horas", compute="_compute_hourly_expenses", store=True)
    total_expenses = fields.Monetary("Gastos Totales", compute="_compute_total_expenses", store=True)
    balance_hours = fields.Float(compute="_compute_balance_hours", store=True)
    execution_kpi = fields.Monetary(compute="_compute_kpi_execution", store=True)
    real_time_evaluation = fields.Float(
        related="last_authomatic_update_id.real_time_evaluation", store=True
    )

    last_authomatic_update_id=fields.Many2one(
        comodel_name="project.update",
        string='Last authomatic update',
        compute="_compute_last_authomatic_update", 
        store=True)

    @api.depends("update_ids")
    def _compute_last_authomatic_update(self):
        for record in self:
            last_update = self.env["project.update"].search(
                [("project_id", "=", record.id), ("auto",'=',True)],
                order="date desc",
                limit=1,
            )        
            if last_update:
                record.last_authomatic_update_id = last_update.id


    @api.depends("hourly_price", "last_update_total_hours")
    def _compute_hourly_expenses(self):
        for record in self:
            record.hourly_expenses = record.hourly_price * record.last_update_total_hours

    @api.depends("hourly_expenses", "last_update_material_expenses")
    def _compute_total_expenses(self):
        for record in self:
            record.total_expenses = (
                record.hourly_expenses + record.last_authomatic_update_id.material_expenses
            )

    @api.depends("last_authomatic_update_id.total_execution", "total_expenses")
    def _compute_balance_hours(self):
        for record in self:
            record.balance_hours = (
                record.last_authomatic_update_id.total_execution - record.total_expenses
            )

    @api.depends(
        "last_authomatic_update_id.total_execution",
        "last_authomatic_update_id.material_expenses",
        "last_update_total_hours",
    )
    def _compute_kpi_execution(self):
        for record in self:
            if record.last_update_total_hours != 0:
                record.execution_kpi = (
                    record.last_authomatic_update_id.total_execution
                    - record.last_authomatic_update_id.material_expenses
                ) / record.last_update_total_hours
            else:
                record.execution_kpi =0

    def project_recalculate_execution(self, date):
        for project in self:
            if project.execution_weight == "none":
                next

            executed = 0
            total = 0
            task_updates = []
            for task in project.task_ids:
                _logger.debug(
                    "Last update project weight type -%s- ", project.execution_weight
                )
                if project.execution_weight == "budget":
                    total = total + task.budget_amount
                    _logger.debug("Last update date %s ", date)
                    last_update = self.env["project.task.update"].search(
                        [("task_id", "=", task.id), ("date", "<=", date)],
                        order="date desc",
                        limit=1,
                    )
                    # list_updates= task.task_update_ids.filtered(lambda l: l.date <= date).sorted(lambda m: m.date,reverse=True)
                    if last_update:
                        # last_update = list_updates[0]
                        _logger.debug(
                            "Last update for task executed pcnt %s - %s",
                            last_update.execution_pcnt,
                            date,
                        )
                        executed = executed + (
                            task.budget_amount * last_update.execution_pcnt / 100
                        )
                        task_updates.append(last_update.id)
                    else:
                        task_update = self.env["project.task.update"].create(
                            {
                                "task_id": task.id,
                                "execution_pcnt": 0,
                                "description": f"Automatic",
                                "date": date,
                            }
                        )
                        task_updates.append(task_update.id)

                elif project.execution_weight == "hours":
                    total = total + task.planned_hours
                    executed = executed + task.effective_hours

                _logger.debug(
                    "Last update for task executed %s - total %s", executed, total
                )
            if total > 0:
                project_total_pcnt = 100 * executed / total
                project_total_executtion = executed
            else:
                project_total_pcnt = 0
                project_total_executtion = 0
            acls = self.env["account.analytic.line"].search(
                [("account_id", "=", project.analytic_account_id.id)]
            )
            hours = 0
            expenses = 0
            incomes = 0
            real_time_expenses = 0
            for acl in acls:
                if acl.date <= date:
                    if acl.product_uom_id.id == self.env.ref("uom.product_uom_hour").id:
                        hours = hours + acl.unit_amount
                        real_time_expenses = real_time_expenses - acl.amount
                    else:
                        if acl.amount < 0:
                            expenses = expenses - acl.amount
                        else:
                            incomes = incomes + acl.amount

            existing_update = self.env["project.update"].search(
                [
                    ("project_id", "=", project.id),
                    ("date", "=", date),
                    ("auto", "=", True),
                ]
            )
            if existing_update:
                existing_update.write(
                    {
                        "progress": project_total_pcnt,
                        "progress_percentage": project_total_pcnt,
                        "total_budget": total,
                        "total_execution": project_total_executtion,
                        "total_hours": hours,
                        "material_expenses": expenses,
                        "total_incomes": incomes,
                        "project_task_update_ids": [(6, 0, task_updates)],
                        "real_time_evaluation": real_time_expenses,
                        "project_hourly_price": project.hourly_price,
                        "project_allocated_hours": project.allocated_hours,
                        "project_hourly_expenses": project.hourly_expenses,
                        "project_total_expenses": project.total_expenses,
                        "project_balance_hours": project.balance_hours,
                        "project_execution_kpi": project.execution_kpi,
                    }
                )
            else:
                self.env["project.update"].create(
                    {
                        "status": project.last_update_id.status if project.last_update_id.status else "on_track",
                        "total_budget": total,
                        "project_id": project.id,
                        "name": f"Automatic update for {date:%d/%m/%Y}",
                        "auto": True,
                        "progress": project_total_pcnt,
                        "progress_percentage": project_total_pcnt,
                        "total_execution": project_total_executtion,
                        "date": date,
                        "total_hours": hours,
                        "material_expenses": expenses,
                        "total_incomes": incomes,
                        "project_task_update_ids": [(6, 0, task_updates)],
                        "real_time_evaluation": real_time_expenses,
                        "project_hourly_price": project.hourly_price,
                        "project_allocated_hours": project.allocated_hours,
                        "project_hourly_expenses": project.hourly_expenses,
                        "project_total_expenses": project.total_expenses,
                        "project_balance_hours": project.balance_hours,
                        "project_execution_kpi": project.execution_kpi,
                    }
                )

    @api.model
    def recalc_execution_active_projects(self):
        projects = self.env["project.project"].search([])
        _logger.debug("Begin general recalculation for projects")
        last_month_date = datetime.date.today().replace(day=1) - datetime.timedelta(
            days=1
        )
        for project in projects:
            _logger.debug("Begin recalculation for project -%s- on -%s-",project.name,last_month_date)
            project.project_recalculate_execution(last_month_date)
        _logger.debug("End general recalculation for projects")

    @api.depends("task_ids.planned_hours")
    def _compute_allocated_hours(self):
        for record in self:
            task_ids = self.env["project.task"].search([("project_id", "=", record.id)])
            planned_hours = 0
            for task_id in task_ids:
                planned_hours += task_id.planned_hours
            record.allocated_hours = planned_hours
