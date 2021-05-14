from odoo import api, fields, models, _,exceptions
from datetime import date


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_due_date = fields.Date(string="Due Date" ,related='invoice_date_due')
 
    
