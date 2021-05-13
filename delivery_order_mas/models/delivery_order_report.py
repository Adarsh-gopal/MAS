from odoo.exceptions import UserError
from odoo import api, fields, models, _
from num2words import num2words
import pdb

class saleorderdelivery(models.Model):
	_inherit = 'sale.order'

	def amt_in_words_do(self, doamount):
		amount1=str(doamount)
		amt= amount1.split(".")
		print(amt[1],amt[0])
		if int(amt[1]) > 0:
			second_part = ' and '+ num2words(int(amt[1]), lang='en_IN') + ' Paise only '
			print(amt[1],'*****************************************************************')
		else:
			second_part = ' Only '

		return ' Rupees ' + num2words(int(amt[0]), lang='en_IN') + second_part

	# # 	elif pid == 2:

	# def amount_words(self, amount, pid):
	# 	if pid == 20:
	# 		return num2words(amount,lang='en_IN').title() + ' Rupees Only'

	# 	elif pid == 2:
	# 		return num2words(amount,lang='en_IN').title() + ' Dollars Only'

	# 	elif pid == 1:
	# 		return num2words(amount,lang='en_IN').title() + ' Euro\'s Only'
 
	def email_split(self,email):
		esplit=email.split(",")
		if esplit:
			current_name= ''
			for each_email in esplit:
				current_name +=each_email
			
		return current_name

class deliveryorder(models.Model):
	_inherit = 'stock.picking'

	def email_split(self,email):
		esplit=email.split(",")
		if esplit:
			current_name= ''
			for each_email in esplit:
				current_name +=each_email
			
		return current_name

	



	

