# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "res.company"

    analytic_account_type = fields.Selection([('wh','Warehouse'),('pr','Project')],'Analytic Account Type')
