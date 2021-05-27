from odoo.exceptions import UserError
from odoo import api, fields, models, _
from num2words import num2words
import pdb

class taxorder(models.Model):
	_inherit = 'account.move'

	report_type= fields.Selection([('original','original'),('duplicate','duplicate'),('triplicate','triplicate'),('extra_copy','extra_copy')],'Report Type')
	 
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

	def get_ref(self,reference):
		refsplit=reference.split(" ")
		# print(refsplit[2])
		refspt=refsplit[2].split(",")
		print(refspt[0])

		return refspt[0]

	def get_refdebit(self,reference):
		refsplitd=reference.split(" ")
		return refsplitd[2]

	
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









 
		
 








