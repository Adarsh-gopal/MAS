from odoo.exceptions import UserError
from odoo import api, fields, models, _
from num2words import num2words
import pdb

class taxorder(models.Model):
	_inherit = 'account.move'
	no_of_copies = fields.Integer(default=1)
	po_date_inv = fields.Date(string='PO Date')
	po_no_inv = fields.Char(string='PO Number')


	def amount_words(self, amount):
		amount1=str(amount)
		amt= amount1.split(".")
		if int(amt[1]) > 0:
			second_part = ' and '+ num2words(int(amt[1]), lang='en_IN') + ' Paise only '
		else:
			second_part = ' Only '

		return ' Rupees ' + num2words(int(amt[0]), lang='en_IN') + second_part	
	 
	def email_split(self,email):
		esplit=email.split(",")
		if esplit:
			current_name= ''
			for each_email in esplit:
				current_name +=each_email
			if len(current_name) >1:
				name = current_name

		return current_name

	def get_orderdate(self,source):
		sale_id=self.env['sale.order'].search([('name','=',source)])

		return sale_id.date_order	

	
class taxamt(models.Model):
	_inherit = 'account.move.line'

	# def calculategst(self,tax):
	# 	cgst_amt =0.0
	# 	sgst_amt =0.0
	# 	tax_amount=0.0
	# 	for tax in self.tax_ids:
	# 		tax_amount = self.price_subtotal *(self.tax_ids.amount/2)/100
	# 		print("Tax",tax_amount)
		
	# 	return tax_amount

	def calculateigst(self,tax):
		cgst_amt =0.0
		tax_amount=0.0
		for tax in self.tax_ids:
			tax_amount = self.price_subtotal * (self.tax_ids.amount/100)
		# print("Tax",tax_amount)

		return tax_amount

	def calculategst(self,move_id):
		for line in self.move_id:
			tot_tax_amt=0.0
			acc_line_ids=self.env['account.move.line'].search([('move_id','=',self.move_id.id)])
			if acc_line_ids:
				for taxid in acc_line_ids:
					if taxid.tax_line_id:
						tot_tax_amt += taxid.price_subtotal/2
		# pdb.set_trace()
		return tot_tax_amt

	def calculaterate(self,tax):
		cgst_amt =0.0
		sgst_amt =0.0
		rate=0.0
		for tax in self.tax_ids:
			rate = (self.tax_ids.amount/2)
			# print("Tax",rate)

		return rate

	def calculateigstrate(self,tax):
		igstrate=0
		cgst_amt=0.0
		for tax in self.tax_ids:
			igstrate = (self.tax_ids.amount)
			# print("Tax",igstrate)

		return igstrate

class Sale_order(models.Model):
	_inherit = 'sale.order'

	po_date = fields.Date(string='PO Date')
	po_no = fields.Char(string='PO Number')


	def _prepare_invoice(self):
		self.ensure_one()
		journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
		if not journal:
			raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))
		invoice_vals = {
			'ref': self.client_order_ref or '',
			'move_type': 'out_invoice',
			'narration': self.note,
			'currency_id': self.pricelist_id.currency_id.id,
			'campaign_id': self.campaign_id.id,
			'medium_id': self.medium_id.id,
			'source_id': self.source_id.id,
			'invoice_user_id': self.user_id and self.user_id.id,
			'team_id': self.team_id.id,
			'partner_id': self.partner_invoice_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
			'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
			'journal_id': journal.id,  # company comes from the journal
			'invoice_origin': self.name,
			'invoice_payment_term_id': self.payment_term_id.id,
			'payment_reference': self.reference,
			'transaction_ids': [(6, 0, self.transaction_ids.ids)],
			'invoice_line_ids': [],
			'company_id': self.company_id.id,
			'po_date_inv': self.po_date,
			'po_no_inv': self.po_no,
		}
		return invoice_vals








 
		
 








