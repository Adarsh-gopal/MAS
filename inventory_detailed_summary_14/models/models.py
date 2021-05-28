# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    picking_type_code = fields.Selection(related='stock_move_id.picking_type_code',store = True)
    sale_line_id = fields.Many2one(related='stock_move_id.sale_line_id',store = True)
    purchase_line_id = fields.Many2one(related='stock_move_id.purchase_line_id',store = True)
    production_id = fields.Many2one(related='stock_move_id.production_id',store = True)
    raw_material_production_id = fields.Many2one(related='stock_move_id.raw_material_production_id',store = True)
    inventory_id = fields.Many2one(related='stock_move_id.inventory_id',store=True)

class InvBalSumWiz(models.Model):
    _inherit = 'inv.bal.sum'

    stock_purchase = fields.Float('Purchase(Qty)')
    value_purchase = fields.Float('Purchase(Value)')
    stock_sale = fields.Float('Sale(Qty)')
    value_sale = fields.Float('Sale(Value)')
    stock_purchase_return = fields.Float('Purchase Return(Qty)')
    value_purchase_return = fields.Float('Purchase Return(Value)')
    stock_sale_return = fields.Float('Sale Return(Qty)')
    value_sale_return = fields.Float('Sale Return(Value)')
    stock_production = fields.Float('Production(Qty)')
    value_production = fields.Float('Production(Value)')
    stock_consumption = fields.Float('Consumption(Qty)')
    value_consumption = fields.Float('Consumption(Value)')
    stock_positive = fields.Float('+ve Inv/Adj(Qty)')
    value_positive = fields.Float('+ve Inv/Adj(Value)')
    stock_negative = fields.Float('-ve Inv/Adj(Qty)')
    value_negative = fields.Float('-ve Inv/Adj(Value)')
    stock_transfer_in = fields.Float('Stock Transfer In(Qty)')
    value_transfer_in = fields.Float('Stock Transfer In(Value)')
    stock_transfer_out = fields.Float('Stock Transfer Out(Qty)')
    value_transfer_out = fields.Float('Stock Transfer Out(Value)')
    transfer_in = fields.Float('Internal Transfer In(Qty)')
    transfer_out = fields.Float('Internal Transfer Out(Qty)')
    stock_auto_pos = fields.Float('Auto Posted +ve(Qty)')
    value_auto_pos = fields.Float('Auto Posted +ve(Value)')
    stock_auto_neg = fields.Float('Auto Posted -ve(Qty)')
    value_auto_neg = fields.Float('Auto Posted -ve(Value)')

class InvBalSumWiz(models.TransientModel):
    _inherit = 'inv.bal.sum.wiz'
    
    @api.onchange('close_date')
    def _onchange_close_date(self):
        if self.close_date < self.open_date:
            raise ValidationError(_("""End Date should not be less than Start Date"""))

    def action_open_detailed_report(self):
        open_date = str(self.open_date)
        close_date = str(self.close_date)

        if not len(self.location_ids):
            raise ValidationError(_("""Please select Location(s)"""))
            query = """UPDATE inv_bal_sum as ibs SET
            stock_purchase = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NOT NULL),0),
            value_purchase = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NOT NULL),0),
            stock_purchase_return = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NOT NULL),0),
            value_purchase_return = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NOT NULL),0),
            stock_sale = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'outgoing' AND svl.sale_line_id IS NOT NULL),0),
            value_sale = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'outgoing' AND svl.sale_line_id IS NOT NULL),0),
            stock_sale_return = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'incoming' AND svl.sale_line_id IS NOT NULL),0),
            value_sale_return = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'incoming' AND svl.sale_line_id IS NOT NULL),0),
            stock_production = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'mrp_operation' AND svl.production_id IS NOT NULL),0),
            value_production = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'mrp_operation' AND svl.production_id IS NOT NULL),0),
            stock_consumption = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'mrp_operation' AND svl.raw_material_production_id IS NOT NULL),0),
            value_consumption = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code = 'mrp_operation' AND svl.raw_material_production_id IS NOT NULL),0),
            stock_positive = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.inventory_id IS NOT NULL AND svl.quantity > 0),0),
            value_positive = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.inventory_id IS NOT NULL AND svl.value > 0),0),
            stock_negative = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.inventory_id IS NOT NULL AND svl.quantity < 0),0),
            value_negative = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.inventory_id IS NOT NULL AND svl.value < 0),0)
            """.format(open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date)
            self.env.cr.execute(query)
        
        else:
            locations = str(tuple(self.location_ids.ids)+(0,))
            
            query = """UPDATE inv_bal_sum as ibs SET
            stock_purchase = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NOT NULL),0),
            value_purchase = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NOT NULL),0),
            stock_purchase_return = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NOT NULL),0),
            value_purchase_return = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NOT NULL),0),
            stock_sale = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'outgoing' AND svl.sale_line_id IS NOT NULL),0),
            value_sale = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'outgoing' AND svl.sale_line_id IS NOT NULL),0),
            stock_sale_return = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'incoming' AND svl.sale_line_id IS NOT NULL),0),
            value_sale_return = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'incoming' AND svl.sale_line_id IS NOT NULL),0),
            stock_production = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'mrp_operation' AND svl.production_id IS NOT NULL),0),
            value_production = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'mrp_operation' AND svl.production_id IS NOT NULL),0),
            stock_consumption = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'mrp_operation' AND svl.raw_material_production_id IS NOT NULL),0),
            value_consumption = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.picking_type_code = 'mrp_operation' AND svl.raw_material_production_id IS NOT NULL),0),
            stock_positive = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.inventory_id IS NOT NULL AND svl.quantity > 0),0),
            value_positive = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.inventory_id IS NOT NULL AND svl.value > 0),0),
            stock_negative = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.inventory_id IS NOT NULL AND svl.quantity < 0),0),
            value_negative = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {}) AND svl.inventory_id IS NOT NULL AND svl.value < 0),0),
            stock_transfer_in = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.dest_loc_id in {} AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
            value_transfer_in = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.dest_loc_id in {} AND svl.picking_type_code = 'incoming' AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
            stock_transfer_out = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.src_loc_id in {} AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
            value_transfer_out = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.product_id = ibs.product_id AND svl.src_loc_id in {} AND svl.picking_type_code = 'outgoing' AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
            transfer_in = coalesce((SELECT SUM(product_qty) FROM stock_move as sm WHERE sm.date >= '{}' AND sm.date <= '{}' AND sm.product_id = ibs.product_id AND sm.location_dest_id in {} AND (sm.picking_type_code = 'internal')),0),
            transfer_out = coalesce((SELECT SUM(product_qty) FROM stock_move as sm WHERE sm.date >= '{}' AND sm.date <= '{}' AND sm.product_id = ibs.product_id AND sm.location_id in {} AND (sm.picking_type_code = 'internal')),0) * -1
            """.format(open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,open_date,close_date,locations,open_date,close_date,locations,open_date,close_date,locations,open_date,close_date,locations,open_date,close_date,locations)
            self.env.cr.execute(query)
        
        query = """UPDATE inv_bal_sum as ibs SET
        stock_auto_pos = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity > 0 AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
        value_auto_pos = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value > 0 AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
        stock_auto_neg = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity < 0 AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
        value_auto_neg = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value < 0 AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0)
        """.format(open_date,close_date,open_date,close_date,open_date,close_date,open_date,close_date)
        self.env.cr.execute(query)

        tree_view_id = self.env.ref('inventory_detailed_summary_14.inventory_detailed_summmary_tree_view').id
        res = self.action_open_report()

        query = """UPDATE inv_bal_sum SET
        opening_stock = opening_stock + coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0),
        opening_value = opening_value + coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id AND svl.picking_type_code IS NULL AND svl.purchase_line_id IS NULL AND svl.sale_line_id IS NULL AND svl.production_id IS NULL AND svl.raw_material_production_id IS NULL AND svl.inventory_id IS NULL),0)
        """.format(open_date,open_date)
        self.env.cr.execute(query)

        query = """UPDATE inv_bal_sum SET
        stock_increase = stock_increase + stock_auto_pos,
        value_increase = value_increase + value_auto_pos,
        stock_decrease = stock_decrease + stock_auto_neg,
        value_decrease = value_decrease + value_auto_neg
        """
        self.env.cr.execute(query)

        query = """UPDATE inv_bal_sum SET
        closing_stock = closing_stock + stock_auto_pos + stock_auto_neg,
        closing_value = closing_value + value_auto_pos + value_auto_neg"""
        self.env.cr.execute(query)
        
        # if not len(self.location_ids):
        #     query = """UPDATE inv_bal_sum SET 
        #     warehouses = NULL,
        #     locations = NULL,
        #     transfer_in = NULL,
        #     transfer_out = NULL"""
        #     self.env.cr.execute(query)
        
        res['views'][0][0] = tree_view_id
        
        return res