# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleDocType(models.Model):
    _name = 'sale.doc.type'
    _description = 'Sale Order Document Type'

    name = fields.Char()
    description = fields.Char()
    sequence_id = fields.Many2one('ir.sequence')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    revision_count = fields.Integer(default=0,copy=False)
    origin_order_id = fields.Many2one('sale.order',copy=False)
    restore_order_id = fields.Many2one('sale.order',copy=False)
    revision_order_ids = fields.One2many('sale.order', 'origin_order_id')
    doc_type_id = fields.Many2one('sale.doc.type', string="Document Type", ondelete="restrict")
    quotation_number = fields.Char(copy=False)
    state = fields.Selection(selection_add=[('revn','Revision')])

    def action_confirm(self):
        if not self.doc_type_id:
            raise ValidationError(_("""Mapping Document type is required to confirm a Sales Quotation"""))
        if self.restore_order_id:
            self.quotation_number = self.restore_order_id.name
        else:
            self.quotation_number = self.name
            self.revision_count += 1
            self.create_revision(self.name,'draft')
        self.name = self.doc_type_id.sequence_id.next_by_id()
        return super(SaleOrder, self).action_confirm()

    def unlink(self):
        for rec in self:
            if rec.origin_order_id:
                raise ValidationError(_("""Can not delete Sale Order Revision"""))
        return super(SaleOrder, self).unlink()

    def restore_revision(self):
        if self.origin_order_id.state != 'draft':
            raise ValidationError(_("""Can only restore to a draft Quotation"""))
        self.state = 'draft'
        old_origin = self.origin_order_id
        self.origin_order_id.create_revisions()
        new_origin = self.copy({
            'name':self.origin_order_id.name,
            'revision_count':self.origin_order_id.revision_count,
            'revision_order_ids':[(6, 0, self.origin_order_id.revision_order_ids.ids)],
            'restore_order_id':self.id
        })
        old_origin.unlink()
        return {
            'name': new_origin.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': new_origin.id
        }
    
    def create_revision(self,name,state):
        self.copy({
            'name': name,
            'state': state,
            'origin_order_id': self.id
            })

    def create_revisions(self):
        for rec in self:
            if rec.origin_order_id:
                raise ValidationError(_("""Can not revise Revisions"""))
            if rec.state in ("sale","done","cancel"):
                raise ValidationError(_("""Only draft Quotations can be revised"""))
            rec.revision_count += 1
            rec.create_revision("{}-{}".format(rec.name,rec.revision_count),'revn')
    
    def view_previous_versions(self):
        return {
            'name': 'Quotation/Revisions',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('origin_order_id', '=', self.id)],
            'context': dict(self._context, create=False, edit=False)
        }
    
    def action_quotation_sent(self):
        for order in self:
            if order.origin_order_id:
                raise ValidationError(_("""Can not mark a Revision and sent"""))
        return super(SaleOrder, self).action_quotation_sent()
    
    def action_draft(self):
        raise ValidationError(_("""Invalid Action"""))

class SalePaymentLink(models.TransientModel):
    _inherit = "payment.link.wizard"

    @api.model
    def default_get(self, fields):
        res = super(SalePaymentLink, self).default_get(fields)
        if res['res_id'] and res['res_model'] == 'sale.order':
            record = self.env[res['res_model']].browse(res['res_id'])
            if record.origin_order_id:
                raise ValidationError(_("""Can not Create Payment Link for a Revision"""))
        return res

class PortalMixin(models.AbstractModel):
    _inherit = "portal.mixin"

    @api.model
    def action_share(self):
        # print('\n\n',self.env.context['active_id'],'\n',self.env.context['active_model'],'\n\n')
        if self.env.context['active_model'] == 'sale.order':
            if self.env['sale.order'].browse(self.env.context['active_id']).origin_order_id:
                raise ValidationError(_("""Can not Share a Revision"""))
        return super(PortalMixin, self).action_share()




class SaleReport(models.Model):
    _inherit = "sale.report"

    item_group = fields.Many2one('item.group')
    product_group_1 = fields.Many2one('product.group.1')
    product_group_2 = fields.Many2one('product.group.2')
    product_group_3 = fields.Many2one('product.group.3')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['item_group'] = ",t.item_group as item_group"
        fields['product_group_1'] = ",t.product_group_1 as product_group_1"
        fields['product_group_2'] = ",t.product_group_2 as product_group_2"
        fields['product_group_3'] = ",t.product_group_2 as product_group_3"

        groupby += ', t.item_group'
        groupby += ', t.product_group_1'
        groupby += ', t.product_group_2'
        groupby += ', t.product_group_3'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

# class AccountInvoice(models.Model):
#     _inherit = 'account.move'

#     def action_post(self):
#         self.write({'name':"AAAABBBBCCC"})
#         print('\n\n\/\/\n\n')
#         return super(AccountInvoice, self).action_post()