# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class GenerateEquipmentWiz(models.Model):
    _name = 'generate.asset.equipment'
    _description = 'generate equiments based on the assets'

    asset_id = fields.Many2one('account.asset',required=True)
    category_id = fields.Many2one('maintenance.equipment.category',string="Equipment Category")
    number_of_equiments = fields.Float('Number of Equipments')
    hsn_code_id = fields.Many2one('hsn.master',string="HSN SAC Code ",tracking=True)

    @api.onchange('asset_id')
    def update_number_of_equipements(self):
        if self.asset_id:
            self.number_of_equiments = self.asset_id.quantity

    def generate_equipments(self):
        if self.asset_id and self.number_of_equiments > 0.0:
            equipments_count =self.env['maintenance.equipment'].search_count([('account_assets_id', '=', self.asset_id.id)])
            if (equipments_count + self.number_of_equiments) > self.asset_id.quantity:
                raise UserError(_("Number of Equipments should not be greater than quantities of assets"))
            else:
                for each in range(int(self.number_of_equiments)):
                    self.env['maintenance.equipment'].create({
                            'name': self.asset_id.name,
                            'category_id': self.category_id.id,
                            'account_assets_id': self.asset_id.id,
                            'cost':self.asset_id.value_residual/self.asset_id.quantity,
                             'hsn_code_id': self.hsn_code_id.id,
                        })
                return True

