from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import date 
from dateutil import relativedelta
import pdb

class HrContract(models.Model):
    _inherit = "hr.contract"


    total_ctc = fields.Monetary("Total CTC")
    current_month_salary = fields.Char("Current Month Salary")

class HrContractors(models.Model):
    _name = "hr.contractors"
    _description = "HR Contractors"

    name = fields.Char('Name')

class HrLoanAcc(models.Model):
    _inherit = 'hr.loan'

    date_of_joinings = fields.Date('Date Of Joining')
    current_month_salary = fields.Char("Current Month Salary")
    remaining_advance_amount = fields.Float('Remaining Advance Amount',store=True,tracking=True,compute='compute_remaining_amount')
    contractors_visible = fields.Boolean('Contractors')
    contractors = fields.Many2one('hr.contractors',string=' Contractors')

    @api.onchange('employee_id')
    def current_salary(self):
        for l in self:
            var = self.env['hr.contract'].search([('employee_id','=',l.employee_id.id)])
            l.current_month_salary = var.current_month_salary

    @api.onchange('employee_id')
    def date_of_joining(self):
        for l in self:
            l.date_of_joinings = l.employee_id.date_of_joining

    @api.depends('state')
    def compute_remaining_amount(self):
        for l in self:
            if l.state == 'approve':
                l.remaining_advance_amount = l.balance_amount
            else:
                l.remaining_advance_amount = 0.0




