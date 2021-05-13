from odoo import models, fields, api

class HrContract(models.Model):
	_inherit = 'hr.employee'
	#max_loan_amt = fields.Float(string="Max Loan Amount")
	loan_balance = fields.Float(string="Loan Balance")

class ResUsers(models.Model):
    _inherit = 'res.users'
    allow_loan_balance = fields.Boolean('Allow Loan Balance')

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    loan_balance = fields.Float(string="Loan Balance")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.")