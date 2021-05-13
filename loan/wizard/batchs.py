from collections import defaultdict
from datetime import datetime, date, time
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def compute_sheet(self):
    	rec = super(HrPayslipEmployees, self).compute_sheet()
    	contract_obj = self.env['hr.contract']
    	lon_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_ids.ids), ('state', '=', 'approve')])
    	for loan in lon_obj:
    		for loan_line in loan.loan_lines:
    			var = self.env['hr.payslip'].search([('employee_id', '=', self.employee_ids.ids)])
    			for l in var:
    				# print('*******************************************************************',var)
    				if l.date_from <= loan_line.date <= l.date_to and not loan_line.paid:
    					# print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
    					for result in l.struct_id.input_line_type_ids:
    						if result.code == 'LO':
    							if loan.employee_id.id == l.employee_id.id:
	    							l.input_line_ids = [(0,0,
	    								{
	    								'name':result.name,
	    								'code':result.code,
	    								#'payslip_id':self.id,
	    								'amount':loan_line.amount,
	    								'contract_id':l.contract_id.id,
	    								'loan_line_id':loan_line.id,
	    								'input_type_id':result.id,})]
	    							# print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',l.input_line_ids)
    	return rec