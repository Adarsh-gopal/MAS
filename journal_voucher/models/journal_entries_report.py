from odoo.exceptions import UserError
from odoo import api, fields, models, _
from num2words import num2words
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from functools import partial

class accountjournal(models.Model):
	_inherit = 'account.move'

	amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, compute='_amount_compute', track_visibility='onchange')
	
	@api.depends('line_ids.debit', 'line_ids.credit')
	def _amount_compute(self):
		for move in self:
			total = 0.0
			for line in move.line_ids:
				total += line.debit
			move.amount_untaxed = total

	def get_prepared_by(self):
		rec = self.env['mail.message'].sudo().search([('model','=','account.move'),('res_id','=',self.id),('subtype_id','=',self.env.ref('account.mt_invoice_validated').id)])
		if rec:
			return rec.create_uid.name
		else:
			return ''


	def email_split(self,email):
		esplit=email.split(",")
		if esplit:
			current_name= ''
			for each_email in esplit:
				current_name +=each_email
			if len(current_name) >1:
				name = current_name

		return current_name

	def amt_in_words(self, amount):
		amount1=str(amount)
		amt= amount1.split(".")
		print(amt[1],amt[0],amount)
		if int(amt[1]) > 0:
			second_part = ' and '+ num2words(int(amt[1]), lang='en_IN') + ' Paise only '
			print(amt[1],'*****************************************************************')
		else:
			second_part = ' Only '

		return ' Rupees ' + num2words(int(amt[0]), lang='en_IN') + second_part

class accountjournal(models.Model):
	_inherit = 'account.move.line'

	# def amt_in_words(self, amount):
	# 	amount1=str(amount)
	# 	amt= amount1.split(".")
	# 	print(amt[1],amt[0],amount)
	# 	if int(amt[1]) > 0:
	# 		second_part = ' and '+ num2words(int(amt[1]), lang='en_IN') + ' Paise only '
	# 		print(amt[1],'*****************************************************************')
	# 	else:
	# 		second_part = ' Only '

	# 	return ' Rupees ' + num2words(int(amt[0]), lang='en_IN') + second_part

	


