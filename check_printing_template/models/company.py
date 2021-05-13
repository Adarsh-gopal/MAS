# -*- coding: utf-8 -*-


from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    # here, key has to be full xmlID(including the module name) of all the
    # new report actions that you have defined for check layout
    account_check_printing_layout = fields.Selection(selection_add=[
        ('check_printing_template.action_cheque_print_report', 'Print Cheque Srilanka'),
    ], ondelete={
        'check_printing_template.action_cheque_print_report': 'set default',
    })
