from odoo import models, fields, api, _
from odoo import tools

class generateAssetE(models.Model):
    _inherit = "generate.asset.equipment"

    hsn_code_id = fields.Many2one('hsn.master',string="HSN SAC Code ",tracking=True)

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

class MaintenanceEquipmentH(models.Model):
    _inherit = "maintenance.equipment"

    hsn_code_id = fields.Many2one('hsn.master',string="HSN SAC Code ",tracking=True)

    def update_name(self):
        for rec in self:
            old_name = rec.name
            if rec.equipment_number:
                rec.name = old_name +'-'+ rec.equipment_number


    
