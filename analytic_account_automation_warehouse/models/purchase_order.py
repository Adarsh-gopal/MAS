# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    
    @api.onchange('picking_type_id')
    def _onchange_of_warehouse_aa(self):
        if  self.picking_type_id:
            self.analytic_account_id = self.picking_type_id.warehouse_id.analytic_account_id.id


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    warehouse_id = fields.Many2one('stock.warehouse')

class StockWarehouseL(models.Model):
    _inherit = 'stock.warehouse'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    # @api.onchange('analytic_account_id')
    # def _onchange_analytic_account(self):
    #     if self.analytic_account_id:
    #         self.analytic_account_id.warehouse_id = self.id

   
class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.onchange('warehouse_id')
    def _onchange_(self):
        if  self.warehouse_id:
            self.analytic_account_id = self.warehouse_id.analytic_account_id.id



