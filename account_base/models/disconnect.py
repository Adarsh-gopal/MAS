# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = "account.move"
    
    @api.onchange('invoice_date')
    def _onchange_invoice_date(self):
        if self.invoice_date:
            if not self.invoice_payment_term_id and (not self.invoice_date_due or self.invoice_date_due < self.invoice_date):
                self.invoice_date_due = self.invoice_date
            if self.move_type not in ('in_invoice','in_refund','in_receipt'):
                if self.date != self.invoice_date:  # Don't flag date as dirty if not needed
                    self.date = self.invoice_date
            self._onchange_currency()