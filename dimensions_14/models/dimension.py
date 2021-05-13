# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DimensionName(models.Model):
    _name = 'dimension.name'
    _description = 'Dimension Names'

    name = fields.Char("Dimension Name")
    dimension_value_ids = fields.Many2many('dimension.value',compute='_fetch_values')
    dimension_line_ids = fields.One2many('dimension.line','dimension_name_id')

    @api.depends('dimension_line_ids','dimension_line_ids.dimension_value_id')
    def _fetch_values(self):
        for rec in self:
            rec.dimension_value_ids = [(6, 0, rec.dimension_line_ids.mapped('dimension_value_id').ids)]

class DimensionLine(models.Model):
    _name = 'dimension.line'
    _description = 'Dimension Line'

    dimension_name_id = fields.Many2one('dimension.name')
    dimension_value_id = fields.Many2one('dimension.value')

class DimensionValue(models.Model):
    _name = 'dimension.value'
    _description = 'Dimension Value'

    name = fields.Char('Value')
