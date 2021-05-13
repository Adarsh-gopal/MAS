# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountChequeRegister(models.Model):
    _name = "account.cheque.register"
    _description = "Account Cheque Register"
    _rec_name = 'cheque_number'

    cheque_number = fields.Char(string="Cheque Number")
    date = fields.Date(default=fields.Date.context_today)
    payment_id = fields.Many2one('account.payment', copy=False)
    journal_entry_no = fields.Char(string='Journal Entry Number')
    partner_id = fields.Many2one('res.partner', string='Partner Name', copy=False)
    amount = fields.Float(string='Amount')
    memo = fields.Char()
    status = fields.Char()
