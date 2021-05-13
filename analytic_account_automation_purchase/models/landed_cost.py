# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AdjustmentLines(models.Model):
    _inherit = "stock.valuation.adjustment.lines"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_inventory')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_inventory')

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id):
        data = super(AdjustmentLines, self)._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)
        
        for line in data:
            line[2]['analytic_account_id'] = self.analytic_account_id.id
            line[2]['analytic_tag_ids'] = [(6,0,self.analytic_tag_ids.ids)]

        return data
