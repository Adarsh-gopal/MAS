from odoo import api, fields, models, _,exceptions
from datetime import date


class AccountMove(models.Model):
    _inherit = "account.move"

    new_invoice_date_due = fields.Date(string="Due Days" ,related='invoice_date_due')
 
    
