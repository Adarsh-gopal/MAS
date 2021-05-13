from odoo import models, fields, api, _


class AccConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    loan_approve = fields.Boolean(default=False, string="Approval from Accounting Department",
                                  help="Loan Approval from account manager")
    loan_amount = fields.Float(string='Loan Amount')

    @api.model
    def get_values(self):
        res = super(AccConfig, self).get_values()
        verify = self.env['ir.config_parameter'].sudo().get_param('account.loan_approve')
        amt = self.env['ir.config_parameter'].sudo().get_param('account.loan_amount')
        res.update(
            loan_approve=bool(verify),
            loan_amount=float(amt),
        )
        return res

    # @api.multi
    def set_values(self):
        super(AccConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account.loan_approve', self.loan_approve)
        self.env['ir.config_parameter'].sudo().set_param('account.loan_amount', self.loan_amount)

