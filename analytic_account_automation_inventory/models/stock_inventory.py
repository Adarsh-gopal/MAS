# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_inventory')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_inventory')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        data = super(InventoryLine, self)._get_move_values(qty, location_id, location_dest_id, out)
        
        data['analytic_account_id'] = self.inventory_id.analytic_account_id.id
        data['analytic_tag_ids'] = [(6, 0, self.inventory_id.analytic_tag_ids.ids)]

        return data