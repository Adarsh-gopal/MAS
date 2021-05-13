from odoo import api, fields, models, SUPERUSER_ID, _

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    purchase_order_ids = fields.Many2many('purchase.order',string='Purchase Orders')
    
    @api.onchange('picking_ids')
    def _onchange_picking_ids(self):
        self.purchase_order_ids = [(6, 0, self.picking_ids.mapped('purchase_id').ids)]
    
    @api.onchange('purchase_order_ids')
    def _onchange_purchase_order_ids(self):
        self.cost_lines = [(2, line.id, 0) for line in self.cost_lines]
        self.cost_lines = [(0, 0, {
            'product_id':line.product_id.id,
            'split_method':line.product_id.split_method_landed_cost,
            'price_unit':line.price_unit
        })for line in self.purchase_order_ids.mapped('order_line').filtered(lambda l: l.product_id.landed_cost_ok)]