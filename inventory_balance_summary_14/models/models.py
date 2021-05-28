# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    warehouse_id = fields.Many2one('stock.location',compute='_get_warehouse',store=True)

    @api.depends('parent_path')
    def _get_warehouse(self):
        for rec in self:
            parent_path = rec.parent_path.split('/')
            if len(parent_path) > 2:
                rec.warehouse_id = int(rec.parent_path.split('/')[1])

class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_type_code = fields.Selection(related='picking_type_id.code',store=True,string='Operation Type Code')

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    src_loc_id = fields.Many2one(related = 'stock_move_id.location_id',store = True)
    dest_loc_id = fields.Many2one(related = 'stock_move_id.location_dest_id',store = True)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    inv_bal_sum_id = fields.Many2one('inv.bal.sum',compute='_create_inv_bal_sum_rec',store=True)

    @api.depends('type','active')
    def _create_inv_bal_sum_rec(self):
        for rec in self:
            if rec.type == 'product' and rec.active:
                rec.inv_bal_sum_id = self.env['inv.bal.sum'].create({'product_id':rec.id})
            else:
                wrong_prod = rec.inv_bal_sum_id.id
                rec.inv_bal_sum_id = False
                self.env['inv.bal.sum'].browse(wrong_prod).unlink()

class InvBalSumWiz(models.Model):
    _name = 'inv.bal.sum'
    _description = 'Inventory Summary'

    product_id = fields.Many2one('product.product')
    company_id = fields.Many2one('res.company',related='product_id.product_tmpl_id.company_id',store=True)
    uom_id = fields.Many2one(related = 'product_id.uom_id', store=True, string="UOM")
    categ_id = fields.Many2one(related = 'product_id.categ_id', store=True)
    default_code = fields.Char(related = 'product_id.default_code', store=True, string="Code")
    item_group = fields.Many2one(related = 'product_id.item_group', store=True)
    product_group_1 = fields.Many2one(related = 'product_id.product_group_1', store=True)
    product_group_2 = fields.Many2one(related = 'product_id.product_group_2', store=True)
    product_group_3 = fields.Many2one(related = 'product_id.product_group_3', store=True)
    opening_stock = fields.Float('Opening(Qty)')
    opening_value = fields.Float('Opening(Value)')
    stock_increase = fields.Float('Inward(Qty)')
    value_increase = fields.Float('Inward(Value)')
    stock_decrease = fields.Float('Outward(Qty)')
    value_decrease = fields.Float('Outward(Value)')
    closing_stock = fields.Float('Closing(Qty)')
    closing_value = fields.Float('Closing(Value)')
    warehouses = fields.Char()
    locations = fields.Char()
    

class InvBalSumWiz(models.TransientModel):
    _name = 'inv.bal.sum.wiz'
    _description = 'Inventory Summary Wizard'

    open_date = fields.Datetime(string='Start Date')
    close_date = fields.Datetime(string='End Date')
    location_ids = fields.Many2many('stock.location')
    warehouse_id = fields.Many2one('stock.location')
    
    @api.onchange('close_date')
    def _onchange_close_date(self):
        if self.close_date < self.open_date:
            raise ValidationError(_("""End Date should not be less than Start Date"""))

    def action_open_report(self):
        open_date = str(self.open_date)
        close_date = str(self.close_date)
        warehouses = ""

        if not len(self.location_ids):
            raise ValidationError(_("""Please select Location(s)"""))
            query = """UPDATE inv_bal_sum as ibs SET 
            opening_stock = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id),0),
            stock_increase = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity > 0 AND svl.product_id = ibs.product_id),0),
            stock_decrease = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity < 0 AND svl.product_id = ibs.product_id),0),
            opening_value = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id),0),
            value_increase = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value > 0 AND svl.product_id = ibs.product_id),0),
            value_decrease = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value < 0 AND svl.product_id = ibs.product_id),0)
            """.format(open_date,open_date,close_date,open_date,close_date,open_date,open_date,close_date,open_date,close_date)
            self.env.cr.execute(query)
        
        else:
            locations = str(tuple(self.location_ids.ids)+(0,))
            query = """UPDATE inv_bal_sum as ibs SET
            opening_stock = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0)
            + coalesce((SELECT SUM(sml.qty_done) FROM stock_move as sm INNER JOIN stock_move_line as sml on sml.move_id = sm.id WHERE sm.date < '{}' AND sm.product_id = ibs.product_id AND sm.location_dest_id in {} AND sm.picking_type_code = 'internal'),0)
            - coalesce((SELECT SUM(sml.qty_done) FROM stock_move as sm INNER JOIN stock_move_line as sml on sml.move_id = sm.id WHERE sm.date < '{}' AND sm.product_id = ibs.product_id AND sm.location_id in {} AND sm.picking_type_code = 'internal'),0),
            stock_increase = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity > 0 AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0),
            stock_decrease = coalesce((SELECT SUM(quantity) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.quantity < 0 AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0),
            opening_value = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date < '{}' AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0),
            value_increase = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value > 0 AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0),
            value_decrease = coalesce((SELECT SUM(value) FROM stock_valuation_layer as svl WHERE svl.create_date >= '{}' AND svl.create_date <= '{}' AND svl.value < 0 AND svl.product_id = ibs.product_id AND (svl.src_loc_id in {} OR svl.dest_loc_id in {})),0)
            """.format(open_date,locations,locations,open_date,locations,open_date,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations,open_date,locations,locations,open_date,close_date,locations,locations,open_date,close_date,locations,locations)
            self.env.cr.execute(query)

            query = """UPDATE inv_bal_sum as ibs SET
            stock_increase = ibs.stock_increase + coalesce((SELECT SUM(sml.qty_done) FROM stock_move as sm INNER JOIN stock_move_line as sml on sml.move_id = sm.id WHERE sm.date >= '{}' AND sm.date <= '{}' AND sm.product_id = ibs.product_id AND sm.location_dest_id in {} AND sm.picking_type_code = 'internal'),0),
            stock_decrease = ibs.stock_decrease - coalesce((SELECT SUM(sml.qty_done) FROM stock_move as sm INNER JOIN stock_move_line as sml on sml.move_id = sm.id WHERE sm.date >= '{}' AND sm.date <= '{}' AND sm.product_id = ibs.product_id AND sm.location_id in {} AND sm.picking_type_code = 'internal'),0)
            """.format(open_date,close_date,locations,open_date,close_date,locations)
            self.env.cr.execute(query)

            locations = self.location_ids.mapped('complete_name')
            warehouses = str(tuple(set([name.split('/')[0] for name in locations]))).replace("'","")
            locations = str(tuple(locations)).replace("'","")
            if locations[-2] == ',':
                locations = locations[:-2]+')'
            if warehouses[-2] == ',':
                warehouses = warehouses[:-2]+')'

            query = """UPDATE inv_bal_sum SET
            warehouses = '{}',
            locations = '{}'
            """.format(warehouses,locations)
            self.env.cr.execute(query)
        
        
        query = """UPDATE inv_bal_sum SET
        closing_stock = opening_stock + stock_increase + stock_decrease,
        closing_value = opening_value + value_increase + value_decrease"""
        self.env.cr.execute(query)

        tree_view_id = self.env.ref('inventory_balance_summary_14.inventory_balance_summmary_tree_view').id

        return {
            'name': 'Inventory Summary {}'.format(warehouses),
            'view_mode': 'tree,pivot',
            'views': [[tree_view_id, 'tree']],
            'res_model': 'inv.bal.sum',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('company_id','=',self.env.company.id)]
            }