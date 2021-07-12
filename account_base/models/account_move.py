from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


    

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

    invoice_due_date = fields.Date(related='invoice_date_due')

    journal_type = fields.Selection(related = 'journal_id.type', readonly=False, string='JType')
    payment_type = fields.Selection(related = 'payment_id.payment_type', readonly=False, store=True)



    def action_post(self):
        for rec in self:
            if rec.move_type in ('in_invoice','in_refund','in_receipt'):
                if rec.date < rec.invoice_date:
                    raise UserError(_('Accounting Date should not less than Bill date !'))

            if rec.journal_type in ('cash','bank'):
                if rec.payment_type == 'inbound':
                    if rec.journal_id.in_sequence_id and not rec.posted_before:
                        rec.write({'name':rec.journal_id.in_sequence_id.with_context(ir_sequence_date=rec.date).next_by_id()})
                elif rec.payment_type == 'outbound':
                    if rec.journal_id.out_sequence_id and not rec.posted_before:
                        rec.write({'name':rec.journal_id.out_sequence_id.with_context(ir_sequence_date=rec.date).next_by_id()})
            if rec.move_type in ('in_refund','out_refund'):
                if rec.journal_id.refund_sequence_id and not rec.posted_before:
                    rec.write({'name':rec.journal_id.refund_sequence_id.with_context(ir_sequence_date=rec.date).next_by_id()})
            elif rec.journal_id.name_sequence_id and not rec.posted_before:
                rec.write({'name':rec.journal_id.name_sequence_id.with_context(ir_sequence_date=rec.date).next_by_id()})
            else:
                pass
                # raise ValidationError(_("""No sequence mapped to Journal {}""".format(rec.journal_id.name)))
        return super(AccountMove, self).action_post()



    @api.constrains('invoice_date')
    def check_invoice_date(self):
        for rec in self:
            if rec.move_type in ('in_invoice','in_refund','in_receipt'):
                if not rec.invoice_date:
                    raise UserError(_('Invoice/Bill Date Not updated '))


class StockMove(models.Model):
    _inherit = "account.move.line"

    product_category_id = fields.Many2one('product.category',related='product_id.product_tmpl_id.categ_id', store=True)
    item_group = fields.Many2one('item.group',related='product_id.product_tmpl_id.item_group', store=True)
    product_group_1 = fields.Many2one('product.group.1',related='product_id.product_tmpl_id.product_group_1',store=True)
    product_group_2 = fields.Many2one('product.group.2',related='product_id.product_tmpl_id.product_group_2',store=True)
    product_group_3 = fields.Many2one('product.group.3',related='product_id.product_tmpl_id.product_group_3',store=True)


