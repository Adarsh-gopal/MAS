# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BOM(models.Model):
    _inherit = 'mrp.bom'

    add_operation = fields.Many2one('mrp.routing.workcenter')

    @api.onchange('add_operation')
    def _add_new_operation(self):
        if self.add_operation:
            new_operation = self.add_operation.copy()
            new_operation.is_master = False
            self.operation_ids = [(4, new_operation.id, 0)]
            self.add_operation = False

class Operation(models.Model):
    _inherit = 'mrp.routing.workcenter'

    is_master = fields.Boolean()