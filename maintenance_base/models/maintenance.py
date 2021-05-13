# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    sequence = fields.Many2one('ir.sequence')

class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    equipment_number = fields.Char()
    state = fields.Selection([
        ('available', 'Available'),
        ('inuse', 'In Use'),
        ('under_maintenance', 'Under Manintenance'),
        ('scrap', 'Scrap'),
        ],string='Status',tracking=True,default='available')

    sub_category_1 = fields.Many2one('sub.equipment.categ.1', string="Sub-Category 1")
    sub_category_2 = fields.Many2one('sub.equipment.categ.2', string=" Sub-Category 2")
    sub_category_3 = fields.Many2one('sub.equipment.categ.3', string="Sub-Category 3")

    dimension = fields.Char()

    # @api.onchange('category_id')
    # def _onchange_equipment(self):
    #     if self.category_id:
    #         self.equipment_number = self.category_id.sequence.next_by_id()

    @api.model
    def create(self, vals):
        if vals.get('category_id'):
            categ = self.env['maintenance.equipment.category'].browse(vals['category_id'])
            if categ.sequence:
                vals['equipment_number'] = categ.sequence.next_by_id()
            else:
                raise UserError(_("Sequence Not Found For the Category %s")%(categ.name))

        return super(MaintenanceEquipment, self).create(vals)


        


class MaintenanceStage(models.Model):
    _inherit = "maintenance.stage"

    job_work = fields.Boolean('Job Work/Purchase')

class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    sequence_id = fields.Many2one('ir.sequence')

class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    mr_number = fields.Char(default='New',readonly=True)
    jobwork_challan_no = fields.Char(default="/", readonly=True)

    maintenance_type = fields.Selection(selection_add=
        [('breakdown', 'Break Down')])


    @api.model
    def create(self, vals):
        # if ('mr_number' in vals and vals.get('mr_number') == 'New'):
        #     if self.maintenance_team_id and self.maintenance_team_id.sequence_id: 
        #         vals['mr_number'] = self.maintenance_team_id.sequence_id.next_by_id()

        request = super(MaintenanceRequest, self).create(vals)
        if request.maintenance_team_id and request.maintenance_team_id.sequence_id:
            request.mr_number = request.maintenance_team_id.sequence_id.next_by_id()
        if request.equipment_id:
            request.equipment_id.state = 'under_maintenance'

        return request


    @api.onchange('stage_id')
    def change_equipment_state(self):
        if self.equipment_id:
            if self.stage_id.done == True:
                self.equipment_id.state = 'available'
            else:
                self.equipment_id.state = 'under_maintenance'
