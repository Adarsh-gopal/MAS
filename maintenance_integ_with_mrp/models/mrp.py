# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    equipment_ids = fields.Many2many('maintenance.equipment')
    filter_equipment_ids = fields.Many2many('maintenance.equipment',relation='filter_equipment',compute='compute_equipment')

    @api.depends('workcenter_id')
    def compute_equipment(self):
        self.filter_equipment_ids = False
        for l in self.workcenter_id:
            if self.workcenter_id:
                self.filter_equipment_ids = l.equipment_ids.ids
            else:
                self.filter_equipment_ids = False

    @api.onchange('equipment_ids')
    def check_related_product(self):
        if self.equipment_ids:
            equip_ids = self.env['product.equipment.map'].search([('product_id','=',self.production_id.product_id.id)])[0]
            if equip_ids:
                if not (set(self.equipment_ids.ids).issubset(set(equip_ids.equipment_ids.ids))):
                    raise UserError(_("Please map the right equipment"))






    def button_start(self):
        res = super(MrpWorkOrder, self).button_start()
        for l in self.production_id:
            var = self.env['maintenance.equipment'].search([('workcenter_id','=',self.workcenter_id.id),('id','in',self.equipment_ids.ids)])
            for line in var:
                if l.state in ['progress','to_close']:
                    line.state ='inuse'
        return res


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for l in self.workorder_ids:
            var = self.env['maintenance.equipment'].search([('workcenter_id','=',l.workcenter_id.id),('id','in',l.equipment_ids.ids)])
            for line in var:
                if self.state == 'confirmed':
                    line.state ='inuse'
        return res

    def action_cancel(self):
        res = super(MrpProduction, self).action_cancel()
        for l in self.workorder_ids:
            var = self.env['maintenance.equipment'].search([('workcenter_id','=',l.workcenter_id.id),('id','in',l.equipment_ids.ids)])
            for line in var:
                if self.state == 'cancel':
                    line.state ='available'
        return res

class Mrpprocess(models.TransientModel):
    _inherit = 'mrp.immediate.production'

    def process(self):
        res = super(Mrpprocess, self).process()
        mrp = self.env['mrp.production'].search([('id','=',self.env.context.get('active_id'))])
        for m in mrp:
            for l in m.workorder_ids:
                var = self.env['maintenance.equipment'].search([('workcenter_id','=',l.workcenter_id.id),('id','in',l.equipment_ids.ids)])
                for line in var:
                    if m.state == 'done':
                        line.state ='available'
        return res