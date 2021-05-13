from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError

class HsnMaster(models.Model):
	_name = 'hsn.master'
	_description  = 'hsn master'

	name = fields.Char(string='HSN/SAC Code')
	hsn_description = fields.Char(string='HSN/SAC Description')
	vendor_taxes_ids = fields.Many2many('account.tax','vendor_taxes_rel','vend_id','tax_id',string='Vendor Taxes',domain=[('type_tax_use', '=', 'purchase')])
	customer_taxes_ids = fields.Many2many('account.tax','customer_taxes_rel','cust_id','tax_id',string='Customer Taxes',domain=[('type_tax_use', '=', 'sale')])
	

class ProductTemplate(models.Model):
	_inherit = "product.template"

	hsn_code_id = fields.Many2one('hsn.master',string="HSN SAC Code ",tracking=True)

	@api.onchange('hsn_code_id')
	def _Onchange_hsn(self):
		for line in self:
			line.l10n_in_hsn_code = line.hsn_code_id.name
			line.l10n_in_hsn_description = line.hsn_code_id.hsn_description
			line.taxes_id = line.hsn_code_id.customer_taxes_ids
			line.supplier_taxes_id = line.hsn_code_id.vendor_taxes_ids


	# @api.constrains('taxes_id')
	# def _check_taxes_id(self):
	# 	for each in self:
	# 		if each.taxes_id.ids !=  each.hsn_code_id.customer_taxes_ids.ids:
	# 			raise UserError(("Customer Taxes are mismatching as per the %s HSN master. ")%each.hsn_code_id.name)

	# @api.constrains('supplier_taxes_id')
	# def _check_supplier_taxes_id(self):
	# 	for each in self:
	# 		if each.supplier_taxes_id.ids !=  each.hsn_code_id.vendor_taxes_ids.ids:
	# 			raise UserError(("Vendor Taxes are mismatching as per the %s HSN master. ")%each.hsn_code_id.name)