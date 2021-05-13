# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_inventory')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_inventory')

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        data = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)

        for line in data:
            data[line]['analytic_account_id'] = self.analytic_account_id.id
            data[line]['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]
        
        return data

    



    # required for import only

    
    # def _action_confirm(self, merge=True, merge_into=False):
    #     recs = super(StockMove, self)._action_confirm()

    #     for rec in recs:
    #         if rec.name and rec.name[:9] == 'New Move:':
    #             lines = rec.picking_id.move_line_ids.filtered(lambda x: x.move_id == rec)
    #             for line in lines:
    #                 rec.analytic_account_id = line.analytic_account_id.id
    #                 rec.analytic_tag_ids = [(6, 0, line.analytic_tag_ids.ids)]

    #     return recs