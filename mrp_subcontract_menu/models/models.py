#-*- coding: utf-8 -*-

from odoo import models, fields, api


class manufacturing_subcontract(models.Model):
    '''
        Added `parent_picking_id` to store the reference of the stock.picking
        Both the models [ mrp.production and stock.picking ] has the related field in the procurement.group
        So in the compute function for the above field, the Sub-con order is picked up by comparing the names[stock.picking and procurement.group]
    '''
    _inherit = 'mrp.production'

    operation_type_name = fields.Char(compute="_compute_elements", store=True)
    parent_picking_id = fields.Many2one('stock.picking', compute = "_subcon_order", store=True)

    @api.depends('procurement_group_id')
    def _subcon_order(self):
        for r in self:
            print(r.procurement_group_id.name)
            r.parent_picking_id = self.env['stock.picking'].search([('name', '=', r.procurement_group_id.name)]).id or False

    @api.depends('picking_type_id')
    def _compute_elements(self):
        for r in self:
            if r.picking_type_id.name == "Subcontracting":
                r.operation_type_name = "Subcontracting"


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    subcontract_track = fields.Boolean("subcontract track",store=True,compute = "subcon_track")

    @api.depends('move_line_ids_without_package.product_id')
    def subcon_track(self):
        for line in self.move_line_ids_without_package:
            for bom_type in self.env['mrp.bom'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id)]):
                if bom_type.type == 'subcontract':
                    self.update({'subcontract_track':True})
        




    def view_sub_con(self):
        self.ensure_one()
        picking_ids=[]
        new_mrp_id=[]
        # new_mrp_rec =self.move_lines.filtered(lambda m: m.delay_alert_date).move_orig_ids._delay_alert_get_documents()


        return {
            'name': ("Sub Con"),
        	'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'domain': [('parent_picking_id', '=', self.id)],
            'view_mode': 'tree,form'
            }
