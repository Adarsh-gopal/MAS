# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    rct_dir_selec = fields.Boolean('Restrict Direct Selection')