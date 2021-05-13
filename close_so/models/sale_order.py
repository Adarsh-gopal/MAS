# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models, tools, _

from odoo.exceptions import ValidationError, RedirectWarning, except_orm, UserError, AccessError, Warning
import datetime
from datetime import datetime

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	open_close_mo = fields.Selection([ ('open_so', 'OPEN SO'),('close_so', 'CLOSE SO'),],'SO Status', default='open_so',readonly="1")
	sale_order_close = fields.Boolean( compute="check_gate_entry_check",store=True, copy=False)

	@api.depends('order_line.open_close_done')
	def check_gate_entry_check(self):
		for rec in self:
			if rec.order_line:
				if any(rec.order_line.filtered(lambda e:e.open_close_done == False)):
					rec.sale_order_close = False
					rec.open_close_mo = 'open_so'
					# rec.order_line.open_close_done = False
				else:
					rec.sale_order_close = True
					rec.open_close_mo = 'close_so'
					# rec.order_line.open_close_done = True
			else:
				rec.sale_order_close = False

	def close_sale_order(self):
		self.write({'open_close_mo':"close_so"})
		for line in self.order_line:
			line.update({'open_close_done':True})


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	open_close_done = fields.Boolean(store=True,string="SO Done",compute='get_open_close',inverse='get_close_open')

	@api.depends('qty_delivered')
	def get_open_close(self):
		for line in self:
			if line.qty_delivered:
				if line.qty_delivered >= line.product_uom_qty:
					line.update({'open_close_done':True,})
				else:
					line.update({'open_close_done':False,})

			else:
				line.update({'open_close_done':False,})

	def get_close_open(self):
		pass








  





	