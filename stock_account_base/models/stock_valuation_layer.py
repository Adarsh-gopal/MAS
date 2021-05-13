
from odoo import models, fields, api, _

class StockValuationLayer(models.Model):
	_inherit = "stock.valuation.layer"

	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None,orderby=False, lazy=True):
		result = super(StockValuationLayer, self).read_group(domain, fields,groupby, offset, limit, orderby, lazy)
		for res in result:
			if res.get('unit_cost'):
				res['unit_cost'] = (res['value']) / (res['quantity'] or 1)
			else:
				res['unit_cost'] = 0
		return result
	
	stock_landed_cost_ids = fields.Many2one('stock.landed.cost.lines',compute='_get_landed_costs',string="Landed Cost Name",store=True)


	@api.depends('stock_landed_cost_id')
	def _get_landed_costs(self):
		for rec in self:
			rec.stock_landed_cost_ids = rec.stock_landed_cost_id.cost_lines.filtered(lambda a:a.price_unit == rec.value).id





