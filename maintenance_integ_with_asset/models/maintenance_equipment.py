# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class AccountAssets(models.Model):
    _inherit = 'maintenance.equipment'

    account_assets_id = fields.Many2one('account.asset',string="Assets")
    cost = fields.Float('Cost',tracking=True) 


    def update_cost(self):
        if not self.account_assets_id:
            raise UserError(_("No Asset Found"))

        if self.account_assets_id and self.account_assets_id.quantity > 0.0:
            self.cost = self.account_assets_id.book_value / self.account_assets_id.quantity

