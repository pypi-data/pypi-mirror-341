# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectUpdate(models.Model):
    _inherit = "project.update"

    auto = fields.Boolean("Es automático", default=False)
    total_budget = fields.Float("Presupuesto total", readonly=True)
    execution_pcnt = fields.Float(
        string="Ejecución pcnt.",
        help="Execution percent of project",
    )
    project_task_update_ids = fields.Many2many(
        "project.task.update", string="Actualizaciones tareas", help="Task updates"
    )
    currency_id = fields.Many2one(
        related="project_id.analytic_account_id.company_id.currency_id",
        string="Moneda",
    )
    project_execution_weight = fields.Selection(
        related="project_id.execution_weight", store=1
    )
    ## Update existing field
    progress = fields.Float(readonly=True)
    total_execution = fields.Monetary("Total ejecución", readonly=True)
    total_hours = fields.Float("Total hours", readonly=True)
    material_expenses = fields.Monetary("Gastos materiales", readonly=True)
    total_incomes = fields.Monetary("Ingresos", readonly=True)
    execution_value = fields.Float(
        string="Valor ejecución", compute="_compute_execution_value", store=True
    )
    real_time_evaluation = fields.Float(string="Real time evaluation", readonly=True)

    project_hourly_price = fields.Float(string="Precio Hora", readonly=True)
    project_allocated_hours = fields.Float(string="Horas reservadas", readonly=True)
    project_hourly_expenses = fields.Monetary(string="Gastos Horas", readonly=True)
    project_total_expenses = fields.Monetary(string="Gastos Totales", readonly=True)
    project_balance_hours = fields.Float(string="Balance Horas", readonly=True)
    project_execution_kpi = fields.Monetary(string="Ejecución KPI", readonly=True)


    project_analytic_account = fields.Many2one(related="project_id.analytic_account_id", store=True)
    project_analytic_plan = fields.Many2one(related="project_id.analytic_account_id.plan_id", store=True)
    project_user_id = fields.Many2one(related="project_id.user_id", store=True)
    project_is_follower = fields.Many2one(related="project_id.user_id", store=True)





    @api.depends("project_task_update_ids.current_execution")
    def _compute_execution_value(self):
        for record in self:
            record.execution_value = 0
            for task in record.project_task_update_ids:
                record.execution_value += task.current_execution

    def button_recalculate(self):
        self.project_id.project_recalculate_execution(self.date)
