# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')

    @api.onchange('invoice_vendor_bill_id')
    def _onchange_invoice_vendor_bill(self):
        if self.invoice_vendor_bill_id:
            self.analytic_account_id = self.invoice_vendor_bill_id.analytic_account_id
            self.analytic_tag_ids = [(6, 0, self.invoice_vendor_bill_id.analytic_tag_ids.ids)]
        
        return super(AccountMove, self)._onchange_invoice_vendor_bill()
    
    def action_register_payment(self):
        analytic_account = self[0].analytic_account_id
        analytic_tags = self[0].analytic_tag_ids
        for rec in self:
            if rec.analytic_account_id != analytic_account or rec.analytic_tag_ids != analytic_tags:
                raise ValidationError(_("""Analytic Account or Tags do not match in all selected Items"""))
        
        res = super(AccountMove, self).action_register_payment()
        res['context']['default_analytic_account_id'] = analytic_account.id
        res['context']['default_analytic_tag_ids'] = [(6,0,analytic_tags.ids)]

        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    @api.depends('move_id')
    def _compute_analytic_account(self):
        for rec in self:
            if not rec.exclude_from_invoice_tab:
                if rec.move_id.analytic_account_id and not rec.analytic_account_id:
                    rec.analytic_account_id = rec.move_id.analytic_account_id.id
                if rec.move_id.analytic_tag_ids and not rec.analytic_tag_ids:
                    rec.analytic_tag_ids = [(6, 0, rec.move_id.analytic_tag_ids.ids)]