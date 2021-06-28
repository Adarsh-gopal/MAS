# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    purchase_order = fields.Many2one('purchase.order',string='Service Purchase Order')
    material_purchase_order = fields.Many2one('purchase.order',string='Material Purchase Order')
    vendor = fields.Many2many('res.partner')

    @api.onchange('stage_id')
    def onchange_stage_id_for_purchase(self):
        if self.purchase_order and self.stage_id:
            if self.stage_id.done:
                for each in self.purchase_order.order_line:
                    each.write({'qty_received':1})
        elif self.material_purchase_order and self.stage_id:
        	if self.stage_id.done:
        		for each in self.material_purchase_order.order_line:
        			each.write({'qty_received':1})


    #to add name and equipment_id
    def name_get(self):
        res = []
        for rec in self:
            if rec.equipment_id:
                res.append((rec.id, "%s - %s" % (rec.name, rec.equipment_id.display_name or " ")))
            else:
                res.append((rec.id, "%s" % rec.name))
        return res



