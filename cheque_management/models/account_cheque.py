# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import pdb

class AccountChequeLot(models.Model):
    _name = "account.cheque.lot"
    _description = "Account Cheque Lot"
    _rec_name = 'cheque_lot_number'

    def _get_last_number(self):
        return self.env['ir.sequence'].next_by_code('account.cheque.lot')

    cheque_lot_number = fields.Char(string="Cheque Lot Number")
    from_number = fields.Char(string="From Number", default=1)
    to_number = fields.Char(string="To Number", default=1)
    last_number = fields.Char(string="Last Number")
    next_number = fields.Char(string="Next Number", default=lambda x: str(int(x.last_number + 1)), compute='_compute_next_number', store=True)
    active = fields.Boolean(string="Active")
    journal_id = fields.Many2one('account.journal', string='Account Journal', required=True, ondelete='cascade', index=True, copy=False)

    @api.depends('last_number')
    def _compute_next_number(self):
        for record in self:
            record.next_number = str(int(record.last_number) + 1)

    @api.onchange('last_number')
    def _onchange_last_number(self):
        self.next_number = str(int(self.last_number) + 1)

    @api.onchange('active')
    def _onchange_active(self):
        if int(self.next_number) > int(self.to_number):
            raise ValidationError(_("Cheque books has been consumed"))

    @api.model
    def create(self, vals):
        res = super(AccountChequeLot, self).create(vals)
        for cheque in self:
            cheque.next_number = str(int(cheque.last_number) + 1)
            if int(cheque.next_number) > int(cheque.to_number):
                raise ValidationError(_("Cheque books has been consumed"))
        return res
