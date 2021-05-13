# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpEco(models.Model):
    _inherit = "mrp.eco"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_plm')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_plm')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')