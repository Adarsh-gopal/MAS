# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class EquipmentMap(models.Model):
    _name = 'product.equipment.map'
    _description = 'product equipment mapping'


    name = fields.Char()
    product_id = fields.Many2one('product.product',required=True)
    equipment_ids = fields.Many2many('maintenance.equipment')

    @api.model
    def create(self,vals):
        res = super(EquipmentMap,self).create(vals)
        if res.product_id:
            res.name = res.product_id.name

        return res
