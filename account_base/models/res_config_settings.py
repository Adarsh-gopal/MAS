#-*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_custom_sequence = fields.Boolean()
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            enable_custom_sequence = bool(params.get_param('account_base.enable_custom_sequence')),
        )
        return res

    def set_values(self):
        super(ResConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account_base.enable_custom_sequence',self.enable_custom_sequence)

