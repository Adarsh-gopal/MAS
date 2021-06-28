from odoo.exceptions import UserError
from odoo import api, fields, models, _
from num2words import num2words
from odoo.exceptions import UserError, AccessError
import pdb

class saleorderdelivery(models.Model):
	_inherit = 'maintenance.request'

	# def amount_words(self, amount):
 #        return num2words(amount,lang='en_IN').title() + " " + 'Rupees Only '

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
	_inherit = 'maintenance.request'

	vehicle_no=fields.Char(string="Vehicle No")
	transporter=fields.Char(string="Transporter")
	customer_name=fields.Many2one('res.partner',string="Customer Name",store=True)
	# vendor_name=fields.Many2one('res.partner',string="Vendor Name",store=True)

	def email_split(self,email):
		esplit=email.split(",")
		if esplit:
			current_name= ''
			for each_email in esplit:
				current_name +=each_email
			
		return current_name

class JobWorkChallanReport(models.AbstractModel):
    _name = 'report.job_work_challan_mas.jobwork_challan_report'
    _description = 'jobwork_challan_report'

    def _get_report_values(self, docids, data):
        docs = self.env['maintenance.request'].browse(docids)
        for each in docs:
            if each.stage_id.job_work != True:
                raise UserError('You are not allowed to print this document at this state')
        
        return {
            'docs': docs,
        }

	



	

