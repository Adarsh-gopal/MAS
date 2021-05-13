# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    maintenance_request = fields.Many2many('maintenance.request',domain=[('stage_id.job_work','=', True)])


    @api.onchange('requisition_id')
    def _onchange_requisition_id(self):
        res = super(PurchaseOrder,self)._onchange_requisition_id()
        self.maintenance_request = self.requisition_id.maintenance_request.ids

        return res

    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        if self.maintenance_request:
            for line in self.order_line:
                for each in self.maintenance_request:
                    if line.product_id.type == "service":
                        each.write({'purchase_order':self.id,'vendor':[(6, 0, self.partner_id.ids)]})
                    elif line.product_id.type == "consu" or line.product_id.type == "product":
                        each.write({'material_purchase_order':self.id,'vendor':[(6, 0, self.partner_id.ids)]})

        return res

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"
    
    maintenance_request = fields.Many2many('maintenance.request',domain=[('stage_id.job_work','=', True)])