# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.payment'

    alternative_gl = fields.Many2one('alternative.gl')

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        line_vals_list = super(AccountMove, self)._prepare_move_line_default_vals(write_off_line_vals)
        print('\n\n\n',line_vals_list[1],'\n\n\n')

        if self.partner_type == 'supplier' and self.partner_id.property_account_payable_id.id == line_vals_list[1]['account_id']:
            new_account = self.alternative_gl.gl_lines.filtered(lambda x: x.account_on_partner.id == line_vals_list[1]['account_id']).account_to_use_instead.id
            line_vals_list[1]['account_id'] = new_account or line_vals_list[1]['account_id']
        if self.partner_type == 'customer' and self.partner_id.property_account_receivable_id.id == line_vals_list[1]['account_id']:
            new_account = self.alternative_gl.gl_lines.filtered(lambda x: x.account_on_partner.id == line_vals_list[1]['account_id']).account_to_use_instead.id
            line_vals_list[1]['account_id'] = new_account or line_vals_list[1]['account_id']

        return line_vals_list