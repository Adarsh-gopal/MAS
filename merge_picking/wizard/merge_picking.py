# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError, Warning

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    merged = fields.Boolean(string='Merged')

    @api.depends('order_line.move_ids')
    def _compute_picking(self):
        for order in self:
            pickings = self.env['stock.picking']
            for line in order.order_line:
                moves = line.move_ids | line.move_ids.mapped('returned_move_ids')
                moves = moves.filtered(lambda r: r.state != 'cancel')
                pickings |= moves.mapped('picking_id')
            order.picking_ids = pickings
        for order in self:
            if order.merged:
                for a in self.env['stock.picking'].search([]):
                    if a.purchase_ids:
                        for b in a.purchase_ids:
                            if order.id == b.id:
                                order.picking_ids = [(4, a.id)]
        for order in self:
            order.picking_count = len(order.picking_ids)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_ids = fields.Many2many('sale.order',string = 'sale references')
    purchase_ids = fields.Many2many('purchase.order',string = 'Purchase references')

class SaleOrder(models.Model):
    _inherit = "sale.order"

    merged = fields.Boolean(string='Merged')

    @api.depends('procurement_group_id')
    def _compute_picking_ids(self):
        for order in self:
            order.picking_ids = self.env['stock.picking'].search([('group_id', '=', order.procurement_group_id.id)]) if order.procurement_group_id else []
            order.delivery_count = len(order.picking_ids)
        for order in self:
            if order.merged:
                for a in self.env['stock.picking'].search([]):
                    if a.sale_ids:
                        for b in a.sale_ids:
                            if order.id == b.id:
                                order.picking_ids = [(4, a.id)]
        for order in self:
            order.delivery_count = len(order.picking_ids)
            
            

    picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Picking associated to this sale')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    


class MergePicking(models.TransientModel):
    _name = "merge.picking"
    _description = "merge pickings"
    

    @api.model
    def default_get(self, fields):
        rec = super(MergePicking, self).default_get(fields)
        context = dict(self._context or {})
        active_ids = context.get('active_ids')
        
        if active_ids:
            pick_ids = []
            picks = self.env['stock.picking'].browse(active_ids)
            
            if any(pick.state == 'done' for pick in picks):
                raise Warning ('Merging is Not allowed on Done Pickings.')
                    
            pick_ids = [pick.id for pick in picks if pick.state in ('draft', 'confirmed', 'assigned')]
                 
            if 'pickings_ids' in fields:
                rec.update({'pickings_ids': [(6,0,pick_ids)]})
        return rec
            
    
    pickings_ids = fields.Many2many('stock.picking',  'merge_picking_rel', 'merge_id', 'picking_id', 'Pickings',  domain=[('state', '!=', 'done')])



    def validate_pickings(self,pickings,pick_type):
        if len(pickings) < 2:
            raise Warning ('Please select multiple picking to merge in the list view.')

        if any(pick.state == 'done' for pick in pickings):
            raise Warning ('Merging is Not allowed on Done Pickings.')

        vals = False
        for pick in pickings:
            pick_type.append(pick.picking_type_id)

            if not pick_type[1:] == pick_type[:-1]:
                raise Warning ('Merging is only allowed on Pickings of same Types.')

            else:
                vals = {
                        'type_new_pick':pick.picking_type_id.id,
                        'location_dest_id':pick.location_dest_id.id,
                        'location_id':pick.location_id.id
                        }
        return vals,pick_type



    def prepare_picking(self,vals):
        return {
                'picking_type_id':vals['type_new_pick'],
                'location_dest_id':vals['location_dest_id'],
                'location_id':vals['location_id'],
                'state': 'draft'
                }


    def prepare_move(self,move,new_pick):
        return {
                'name': move.name or '',
                'product_id': move.product_id and move.product_id.id or False,
                'product_uom_qty': move.product_qty,
                'product_uom': move.product_uom and move.product_uom.id or False,
                'date': move.date,
                'forecast_expected_date': move.forecast_expected_date,
                'location_id':move.location_id and move.location_id.id or False,
                'location_dest_id':move.location_dest_id and move.location_dest_id.id or False,
                'picking_id': new_pick.id,
                'partner_id': move.partner_id and move.partner_id.id or False,
                'move_dest_ids': [(6,0,move.move_dest_ids.ids)] or False,
                'state': move.state,
                'company_id': move.company_id.id,
                'price_unit': move.price_unit,
                'group_id':move.group_id.id,
                'picking_type_id' : move.picking_type_id.id,
                }



    def merge_pickings(self):
        for res in self:
            pick_obj = self.env['stock.picking']
            move_obj = self.env['stock.move']
            pickings = res.pickings_ids
            invoice_status = []
            pick_state = []
            pick_ids = []
            pick_partner = []
            moves_product = []
            pick_type = []
            origin = []
            custom_sale_list = []
            custom_purchase_list = []
            cancel_list = []


            vals, pick_type = res.validate_pickings(pickings,pick_type)

            new_pick = pick_obj.create(res.prepare_picking(vals))
            for pick in pickings:
                if pick.purchase_id:
                    origin.append(pick.purchase_id.name)
                else:
                    origin.append(pick.name)
                pick_state.append(pick.state)
                pick_partner.append(pick.partner_id)
                pick_type.append(pick.picking_type_id)
                invoice_status.append(pick.sale_id.invoice_status)
                if not pick_type[1:] == pick_type[:-1]:
                    raise Warning ('Merging is only allowed on Pickings of same Types.')

                if not pick_state[1:] == pick_state[:-1]:
                    raise Warning ('Merging is only allowed on Pickings of same State.')


                if not pick_partner[1:] == pick_partner[:-1]:
                    raise Warning ('Merging is only allowed on Pickings of same Partner.')

                else:
                    cancel_list.append(pick)
                    merge_ids = move_obj.search([('picking_id', '=', pick.id)])
                    for line in merge_ids:
                        vals = {
                            'product_id': line.product_id.id or False,
                            'product_uom_qty': line.product_qty,
                            'product_uom': line.product_uom and line.product_uom.id or False,
                            'date': line.date,
                            'forecast_expected_date': line.forecast_expected_date,
                            'location_id': line.location_id and line.location_id.id or False,
                            'location_dest_id': line.location_dest_id and line.location_dest_id.id or False,
                            'price_unit': line.price_unit or False,
                            'picking_id': new_pick.id,
                            'name': line.product_id.default_code and '[' + line.product_id.default_code + '[' + line.product_id.name,
                        }
                        move_obj.update(vals)


                if not invoice_status[1:] == invoice_status[:-1]:
                    raise Warning ('Merging is only allowed on Pickings of same Invoice Status.')
                msg_origin = ""
                origin_list = []
                for i in range(len(origin_list)):
                    if i == len(origin_list) - 1:
                        msg_origin = msg_origin + origin_list[i] + "."
                    else :
                        msg_origin = msg_origin + origin_list[i] + ","
                for move in pick.move_lines:
                    new_move = move_obj.create(res.prepare_move(move,new_pick))
                    moves_product.append(move.product_id.id)
                    if move.purchase_line_id:
                        new_move.purchase_line_id = move.purchase_line_id
                    if move.sale_line_id:
                        new_move.sale_line_id = move.sale_line_id
                if pick.sale_id:
                    custom_sale_list.append(pick.sale_id.id)
                    pick.sale_id.merged = True
                if pick.purchase_id:
                    custom_purchase_list.append(pick.purchase_id.id)
                    if pick.purchase_id:
                        pick.purchase_id.merged = True

                new_pick.write({'state': pick.state, 'partner_id': pick.partner_id and pick.partner_id.id or False,
                                'origin':str(origin).replace("'","").replace("[","").replace("]","")})

                if pick_ids:
                    new_id = pick.id
                    pick_ids.append(new_id)
                else:
                    pick_ids.append(pick.id)
                if new_pick.picking_type_id.code != 'incoming' :
                    for package in new_pick.move_ids_without_package:
                        if package.product_id.qty_available <= 0.0:
                            new_pick.action_confirm()
                        else:
                            new_pick.action_confirm()
                            new_pick.action_assign()
                else:
                    new_pick.mapped('move_lines')._action_confirm()
                    
                    new_pick.mapped('move_lines')._action_assign()

                pick.action_cancel()
            if new_pick.picking_type_id.code == 'incoming' :
                msg_body = _("This transfer has been created from: <b>%s</b>") % (origin)
            else:
                msg_body = _("This delivery order has been created from: <b>%s</b>") % (origin)
            new_pick.message_post(body=msg_body)
            new_pick.sale_ids = [(6,0,custom_sale_list)]
            new_pick.purchase_ids = [(6,0,custom_purchase_list)]

            result =  {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_mode': 'form',
                'res_id': new_pick.id,
                'views': [(False, 'form')],
            }
            return result