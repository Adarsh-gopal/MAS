# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date,timedelta

# class StockMoveLine(models.Model):
#     _inherit = 'stock.move.line'

#     value = fields.Float()

# class StockMove(models.Model):
#     _inherit = 'stock.move'

#     value = fields.Float(compute='_compute_value',store=True,readonly=False)

#     @api.depends('stock_valuation_layer_ids','quantity_done')
#     def _compute_value(self):
#         for rec in self:
#             rec.value = sum([layer.value for layer in rec.stock_valuation_layer_ids])
#             for line in rec.move_line_ids:
#                 line.value = (rec.value / (rec.quantity_done/line.qty_done)) if rec.quantity_done and line.qty_done else 0

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    value = fields.Monetary(store=True)
    currency_id = fields.Many2one(store=True)
    usage = fields.Selection(related="location_id.usage", store=True)
    range1_qty = fields.Float()
    range1_val = fields.Float()
    range2_qty = fields.Float()
    range2_val = fields.Float()
    range3_qty = fields.Float()
    range3_val = fields.Float()
    range4_qty = fields.Float()
    range4_val = fields.Float()
    range5_qty = fields.Float()
    range5_val = fields.Float()
    range6_qty = fields.Float()
    range6_val = fields.Float()
    liquid_qty = fields.Float()

# class InvAgeBal(Model.model):
#     _name = 'inv.age.bal'
#     _description = 'Inventory Aging Balance'

#     product_id = fields.Many2one('product.product')

class InvAgeWiz(models.TransientModel):
    _name = 'inv.age.wiz'
    _description = 'Inventory Aging Wizard'

    range1 = fields.Char()
    range2 = fields.Char()
    range3 = fields.Char()
    range4 = fields.Char()
    range5 = fields.Char()
    # location_ids = fields.Many2many('stock.location')

    def action_open_report(self):
        today = date.today()
        r1_start = today - timedelta(days = int(self.range1.split('-')[0]))
        r1_stop = today - timedelta(days = int(self.range1.split('-')[1]))
        r2_start = today - timedelta(days = int(self.range2.split('-')[0]))
        r2_stop = today - timedelta(days = int(self.range2.split('-')[1]))
        r3_start = today - timedelta(days = int(self.range3.split('-')[0]))
        r3_stop = today - timedelta(days = int(self.range3.split('-')[1]))
        r4_start = today - timedelta(days = int(self.range4.split('-')[0]))
        r4_stop = today - timedelta(days = int(self.range4.split('-')[1]))
        r5_start = today - timedelta(days = int(self.range5.split('-')[0]))
        r5_stop = today - timedelta(days = int(self.range5.split('-')[1]))

        # query = """UPDATE stock_quant as sq SET
        # range1_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        #             -coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        # range2_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        #             -coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        # range3_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        #             -coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        # range4_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        #             -coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        # range5_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        #             -coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        # WHERE sq.usage = 'internal'""".format(r1_start,r1_stop,r1_start,r1_stop,r2_start,r2_stop,r2_start,r2_stop,r3_start,r3_stop,r3_start,r3_stop,r4_start,r4_stop,r4_start,r4_stop,r5_start,r5_stop,r5_start,r5_stop)
        # self.env.cr.execute(query)
        # print("\n\n{}\n\n",query)

        query = """UPDATE stock_quant as sq SET
        range1_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        range2_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        range3_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        range4_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        range5_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.date > '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        range6_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.date <= '{}' AND sml.location_dest_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0),
        liquid_qty = coalesce((SELECT SUM(sml.qty_done) FROM stock_move_line as sml WHERE sml.location_id = sq.location_id AND sml.product_id = sq.product_id AND coalesce(sml.lot_id,0) = coalesce(sq.lot_id,0)),0)
        WHERE sq.usage = 'internal'""".format(r1_start,r1_stop,r2_start,r2_stop,r3_start,r3_stop,r4_start,r4_stop,r5_start,r5_stop,r5_stop)
        self.env.cr.execute(query)
        # print("\n\n{}\n\n",query)

        for x in range(6,0,-1):
            query = """UPDATE stock_quant SET
            range{}_qty = range{}_qty - liquid_qty,
            liquid_qty = 0 WHERE liquid_qty <= range{}_qty
            """.format(x,x,x)
            self.env.cr.execute(query)
            query = """UPDATE stock_quant SET
            liquid_qty = liquid_qty - range{}_qty,
            range{}_qty = 0 WHERE liquid_qty > range{}_qty
            """.format(x,x,x)
            self.env.cr.execute(query)

        query = """UPDATE stock_quant SET
        range1_val = coalesce((SELECT range1_qty * value / nullif(quantity,0)),0),
        range2_val = coalesce((SELECT range2_qty * value / nullif(quantity,0)),0),
        range3_val = coalesce((SELECT range3_qty * value / nullif(quantity,0)),0),
        range4_val = coalesce((SELECT range4_qty * value / nullif(quantity,0)),0),
        range5_val = coalesce((SELECT range5_qty * value / nullif(quantity,0)),0),
        range6_val = coalesce((SELECT range6_qty * value / nullif(quantity,0)),0)
        WHERE usage = 'internal'"""
        self.env.cr.execute(query)

        tree_view_id = self.env.ref('inventory_ageing_report_14.inventory_ageing_summmary_tree_view').id

        return {
            'name': 'Inventory Ageing {}, {}, {}, {}, {}'.format(self.range1,self.range2,self.range3,self.range4,self.range5),
            'view_mode': 'tree,pivot',
            'views': [[tree_view_id, 'tree']],
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('company_id','=',self.env.company.id),('usage','=','internal'),('quantity','!=',0)]
            }