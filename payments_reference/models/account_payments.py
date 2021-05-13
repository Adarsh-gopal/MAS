# See LICENSE file for full copyright and licensing details.

from odoo import fields,api, models,_


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    extenal_ref = fields.Char('External Ref ')

