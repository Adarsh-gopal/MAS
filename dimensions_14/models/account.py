# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    name_system_filter = fields.Many2many(related='account_id.dimension_name_ids',string="Name Filter")
    dimension_name_id = fields.Many2one('dimension.name', string='Dimension')
    value_system_filter = fields.Many2many(related='dimension_name_id.dimension_value_ids',string="Value Filter")
    dimension_value_id = fields.Many2one('dimension.value')

    @api.onchange('account_id')
    def _onchange_of_ai(self):
        self.dimension_name_id = False

    @api.onchange('dimension_name_id')
    def _onchange_of_dn(self):
        self.dimension_value_id = False

class AccountAccount(models.Model):
    _inherit = "account.account"

    dimension_name_ids = fields.Many2many('dimension.name', string='Dimensions')