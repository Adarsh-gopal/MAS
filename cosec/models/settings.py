# -*- coding: utf-8 -*-
from odoo import models, fields,api

class CosecSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # userid = fields.Char(default=lambda self: self.env['ir.config_parameter'].sudo().set_param('cosec.userid'))
    # url = fields.Char(default=lambda self: self.env['ir.config_parameter'].sudo().set_param('cosec.url'))
    # response = fields.Char(default=lambda self: self.env['ir.config_parameter'].sudo().set_param('cosec.response'))

    userid = fields.Char()
    url = fields.Char()
    password = fields.Char()

    def set_values(self):
        super(CosecSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('cosec.userid',self.userid)
        self.env['ir.config_parameter'].sudo().set_param('cosec.url',self.url)
        self.env['ir.config_parameter'].sudo().set_param('cosec.password',self.password)


    @api.model
    def get_values(self):
        res = super(CosecSettings,self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            userid = params.get_param('cosec.userid')
            )
        res.update(
            url = params.get_param('cosec.url')
            )
        res.update(
            password = params.get_param('cosec.password')
            )
        return res

        # url = self.env['ir.config_parameter'].sudo().get_param('cosec.url')
        # response = self.env['ir.config_parameter'].sudo().get_param('cosec.response')
        # API_endPOINT = self.env['ir.config_parameter'].sudo().get_param('cosec.url')






    # @api.model
    # def set_values(self):
    #     res = super(HospitalSettings, self).set_values()
    #     self.env['ir.config_parameter'].set_param('cosec.userid',self.userid)
    #     return res

    #  def get_values(self):
    #     res = super(HospitalSettings, self).get_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
    #     userids = ICPSudo.get_param('cosec.userid')
    #     res.update(
    #         userid=userids
    #         )
    #     return res


    # @api.model
    # def set_values(self):
    #     res = super(CosecSettings, self).set_values()
    #     self.env['ir.config_parameter'].set_param('cosec.userid',self.userid)
    #     return res
    
    # def get_values(self):
    #     res = super(CosecSettings, self).get_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
    #     userids = ICPSudo.get_param('cosec.userid')
    #     res.update(
    #         userid=userids
    #         )
    #     return res