# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
import pdb

class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"


    revision_number = fields.Integer("Revision Number",default=1)
    revision_lines  = fields.One2many('maintenance.revision.lines','maintenance_id')
    current_revision_id = fields.Many2one('maintenance.equipment')
    # parent_id = fields.Many2one('maintenance.equipment',index=True,ondelete='cascade')
    # revision_lines = fields.One2many('maintenance.equipment','parent_id',readonly=True )



    def equipment_revision(self):
        for each in self:
            res=self.copy()
            res.revision_number = self.revision_number+1
            res.account_assets_id = False
            if each.revision_lines:
                for each_line in each.revision_lines:
                    vals={
                        'revision_number': each_line.revision_number,
                        'name': each_line.name,
                        'equipment_number': each_line.equipment_number,
                        'updated_date': each_line.updated_date,
                        'updated_user_id': each_line.updated_user_id.id,
                        'maintenance_id':res.id, 
                        }
                    self.env['maintenance.revision.lines'].create(vals)
            
            vals={
                    'revision_number': each.revision_number,
                    'name': each.name,
                    'equipment_number': each.equipment_number,
                    'updated_date': fields.Datetime.now(),
                    'updated_user_id': self.env.uid,
                    'maintenance_id':res.id, 
                    }
            self.env['maintenance.revision.lines'].create(vals)
            each.active = False


  
class MaintenanceEquipmentLines(models.Model):
    _name = "maintenance.revision.lines"
    _description = "maintenance.revision.lines" 

    maintenance_id = fields.Many2one("maintenance.equipment" )

    revision_number = fields.Integer("Revision Number")
    name = fields.Char('Equipment Name')
    equipment_number = fields.Char("Equipment Number")
    updated_date = fields.Datetime(string='Revised Date', default=fields.Datetime.now)
    updated_user_id = fields.Many2one('res.users',"Revised By")

