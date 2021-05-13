# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_inventory')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_inventory')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')

    @api.onchange('analytic_account_id')
    def _onchange_of_aa(self):
        for line in self.move_lines:
            line.analytic_account_id = self.analytic_account_id.id

    @api.onchange('analytic_tag_ids')
    def _onchange_of_at(self):
        for line in self.move_lines:
            line.analytic_tag_ids = [(6, 0, self.analytic_tag_ids.ids)]