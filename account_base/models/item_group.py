from odoo import models, fields, api, _
import itertools

class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    item_group = fields.Many2one('item.group')
    product_group_1 = fields.Many2one('product.group.1')
    product_group_2 = fields.Many2one('product.group.2')
    product_group_3 = fields.Many2one('product.group.3')

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", template.item_group as item_group,template.product_group_1 as product_group_1,template.product_group_2 as product_group_2,template.product_group_3 as product_group_3"
    
    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ",template.item_group ,template.product_group_1,template.product_group_2 ,template.product_group_3"