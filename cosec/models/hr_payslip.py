from odoo import models, fields, api
# import urllib.request as request
import requests
import pytz
from datetime import datetime , date , timedelta
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning
import math

class HrPayslip(models.Model):
	_inherit = 'hr.payslip'
	_description = 'hr.payslip'

	unpaid_leaves = fields.Float(string="No of Unpaid leaves")
	paid_leaves = fields.Float(string="No of paid leaves")
	process_month = fields.Integer(string="Process month" ,default=1)
	present_days = fields.Float(string="Present days")
	working_time = fields.Float(string="Working time")
	over_time = fields.Float(string="Over time")
	salary_over_hour= fields.Integer(string="Salary Over time -Hours")
	salary_over_minute = fields.Integer(string="Salary Over time -Minutes")

	@api.onchange('employee_id','process_month')
	def set_paid_unpaid(self):
		attend_dtls = self.env['cosec.month'].search([('userid','=',self.employee_id.cosec_id),('pmonth','=',self.process_month)])
		if attend_dtls:
			self.unpaid_leaves = attend_dtls.uldays + attend_dtls.abdays
			self.paid_leaves = attend_dtls.pldays
			self.present_days = attend_dtls.prdays + attend_dtls.trdays
			self.working_time = attend_dtls.work_time/60
			self.salary_over_hour = (attend_dtls.over_time/60)
			self.salary_over_minute = attend_dtls.over_time % 60


			if self.salary_over_minute in range(0,24):
				self.over_time = self.salary_over_hour	
			
			elif self.salary_over_minute in range(24,54):
				self.over_time = self.salary_over_hour + 0.5

			elif self.salary_over_minute > 55:
				self.salary_over_hour = self.salary_over_hour + 1






