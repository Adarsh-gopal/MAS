from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountAccount(models.Model):
    _inherit = 'account.account'

    z_payment = fields.Boolean(string="Payment",default=False)
    

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    name_sequence_id = fields.Many2one('ir.sequence')
    refund_sequence_id = fields.Many2one('ir.sequence')
    out_sequence_id = fields.Many2one('ir.sequence')
    in_sequence_id = fields.Many2one('ir.sequence')
    ceiling_limit = fields.Boolean(string="Ceiling Limit")
    ceiling_limit_value = fields.Float(string="Ceiling Limit Value")

    make_seq_mandetory = fields.Boolean(compute="_get_seq_mand")

    @api.depends('type')
    def _get_seq_mand(self):
        for rec in self:
            if rec.type in ('cash','bank'):
                rec.make_seq_mandetory = bool(self.env['ir.config_parameter'].sudo().get_param('account_base.enable_custom_sequence'))
            else:
                rec.make_seq_mandetory = False

class AccountMove(models.Model):
    _inherit = 'account.move'

    journal_type = fields.Selection(related = 'journal_id.type', readonly=False, string='JType')
    payment_type = fields.Selection(related = 'payment_id.payment_type', readonly=False, store=True)

    def action_post(self):
        for rec in self:
            if rec.move_type in ('in_invoice','in_refund','in_receipt'):
                if rec.date < rec.invoice_date:
                    raise UserError(_('Accounting Date should not less than Bill date !'))

            if rec.journal_type in ('cash','bank'):
                if rec.payment_type == 'inbound':
                    if rec.journal_id.in_sequence_id:
                        rec.write({'name':rec.journal_id.in_sequence_id.next_by_id()})
                elif rec.payment_type == 'outbound':
                    if rec.journal_id.out_sequence_id:
                        rec.write({'name':rec.journal_id.out_sequence_id.next_by_id()})
            if rec.move_type in ('in_refund','out_refund'):
                if rec.journal_id.refund_sequence_id:
                    rec.write({'name':rec.journal_id.refund_sequence_id.next_by_id()})
            elif rec.journal_id.name_sequence_id:
                rec.write({'name':rec.journal_id.name_sequence_id.next_by_id()})
            else:
                pass
                # raise ValidationError(_("""No sequence mapped to Journal {}""".format(rec.journal_id.name)))
        return super(AccountMove, self).action_post()

class AccountPayment(models.Model):
    _inherit = 'account.payment'


    destination_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Destination Account',
        store=True, readonly=False,
        compute='_compute_destination_account_id',
        domain="['|','&',('user_type_id.type', 'in', ('receivable', 'payable')), ('company_id', '=', company_id), ('z_payment','=',True)]",
        check_company=True)