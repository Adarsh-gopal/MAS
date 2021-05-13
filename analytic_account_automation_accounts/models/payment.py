# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_accounts')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_accounts')

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        line_vals_list = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals)

        for line in line_vals_list:
            line['analytic_account_id'] = self.analytic_account_id.id
            line['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return line_vals_list


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_accounts')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_accounts')

    def _create_payment_vals_from_wizard(self):
        payment = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()

        payment['analytic_account_id'] = self.analytic_account_id.id
        payment['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return payment

    def _create_payment_vals_from_batch(self, batch_result):
        payment = super(AccountPaymentRegister, self)._create_payment_vals_from_batch(batch_result)

        payment['analytic_account_id'] = self.analytic_account_id.id
        payment['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return payment