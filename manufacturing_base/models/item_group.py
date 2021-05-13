from odoo import models, fields, api, _
import itertools

class MrpProduction(models.Model):
	_inherit = 'mrp.production'

	item_group = fields.Many2one('item.group')
	product_group_1 = fields.Many2one('product.group.1')
	product_group_2 = fields.Many2one('product.group.2')
	product_group_3 = fields.Many2one('product.group.3')

	@api.onchange('product_id')
	def Onchange_product(self):
		for l in self:
			l.item_group = l.product_id.product_tmpl_id.item_group.id
			l.product_group_1 = l.product_id.product_tmpl_id.product_group_1.id
			l.product_group_2 = l.product_id.product_tmpl_id.product_group_2.id
			l.product_group_3 = l.product_id.product_tmpl_id.product_group_3.id