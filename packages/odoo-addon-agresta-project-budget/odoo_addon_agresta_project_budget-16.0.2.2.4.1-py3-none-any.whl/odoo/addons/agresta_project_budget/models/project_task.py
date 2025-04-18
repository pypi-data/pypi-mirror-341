# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import datetime

class Task(models.Model):
    _inherit = "project.task"

    task_update_ids = fields.One2many(
        string="Actualizaciones de fase",
        comodel_name="project.task.update",
        inverse_name="task_id",
    )
    budget_amount = fields.Monetary(
        string="Presupuesto",
        currency_field="currency_id",
        help="Amount asigned to this task",
    )
    subtasks_budget_amount = fields.Monetary(
        "Presupuesto en subtareas",
        compute="_compute_subtask_effective_hours",
        recursive=True,
        store=True,
        help="Amount asigned on subtasks",
        currency_field="currency_id",
    )
    execution_pcnt = fields.Float(
        string="Ejecución pcnt.",
        help="Execution percent of the task",
        compute="_compute_last_update",
        store=True,
    )
    currency_id = fields.Many2one(
        related="project_id.analytic_account_id.company_id.currency_id",
        string="Moneda",
    )
    project_execution_weight = fields.Selection(
        related="project_id.execution_weight", store=1
    )
    execution_value = fields.Float(
        string="Valor ejecución", compute="_compute_execution_value", store=True
    )

    last_project_update_date = fields.Date (related="project_id.last_authomatic_update_id.date")

    @api.depends("execution_pcnt", "budget_amount")
    def _compute_execution_value(self):
        for record in self:
            record.execution_value = record.execution_pcnt * record.budget_amount/100

    @api.depends("task_update_ids.date", "task_update_ids.execution_pcnt", "task_update_ids")
    def _compute_last_update(self):
        for rec in self:
            last_update = rec.task_update_ids.sorted(key=lambda r: r.date)
            if last_update:
                rec.execution_pcnt = last_update[-1].execution_pcnt
            else:
                rec.execution_pcnt = 0

    @api.depends("child_ids.budget_amount", "child_ids.subtasks_budget_amount")
    def _compute_subtask_effective_hours(self):
        for task in self.with_context(active_test=False):
            task.subtasks_budget_amount = sum(
                child_task.budget_amount + child_task.subtasks_budget_amount
                for child_task in task.child_ids
            )
