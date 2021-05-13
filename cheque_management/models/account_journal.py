# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    lot_lines = fields.One2many('account.cheque.lot', 'journal_id', string='Cheque Lot Lines', copy=True)
