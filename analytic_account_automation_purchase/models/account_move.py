# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('purchase_vendor_bill_id')
    def _onchange_purchase_auto_complete(self):

        if self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
            self.analytic_account_id = self.purchase_id.analytic_account_id
            self.analytic_tag_ids = [(6, 0, self.purchase_id.analytic_tag_ids.ids)]
        
        elif self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            # self.analytic_account_id = self.invoice_vendor_bill_id.analytic_account_id
            # self.analytic_tag_ids = [(6, 0, self.invoice_vendor_bill_id.analytic_tag_ids.ids)]

        return super(AccountMove, self)._onchange_purchase_auto_complete()

    # @api.onchange('analytic_account_id')
    # def _onchange_of_aa(self):
    #     for line in self.line_ids:
    #         if not line.analytic_account_id:
    #             line.analytic_account_id = self.analytic_account_id.id

    # @api.onchange('analytic_tag_ids')
    # def _onchange_of_at(self):
    #     for line in self.line_ids:
    #         if not line.analytic_tag_ids:
    #             line.analytic_tag_ids = [(6, 0, self.analytic_tag_ids.ids)]