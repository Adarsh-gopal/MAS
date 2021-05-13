from datetime import datetime,timedelta

from odoo import api, models, fields, _, exceptions
from dateutil.relativedelta import relativedelta
from time import strptime
from odoo.exceptions import UserError, ValidationError,Warning


class HrEmployee(models.Model):
	_inherit = 'hr.employee'
	alternative_address = fields.Text('Alternative Address',store = True)
	age = fields.Char('Age',store = True,size=3, compute='_compute_age')
	z_age = fields.Char('Ages')
	# date_of_joining = fields.Date('Date of Joining',store = True)
	# date_of_relieving = fields.Date('Date of relieving',store = True)
	# date_of_resignation = fields.Date('Date of resignation',store = True)
	# one = fields.One2many('lang.employee','many')
	two = fields.One2many('family.details','bondage')
	# three = fields.One2many('educate.details','family')
	# four = fields.One2many('experience.details','experience')
	# five = fields.One2many('employee.transfer','transfer')
	#six = fields.One2many('lic.policy.details','policy')
	esi_applicable = fields.Boolean(string='ESI Applicable',store = True)
	# z_pf_no = fields.Char('PF No',store = True)
	# z_esi_no = fields.Char('ESI No',store = True)
	z_epf_uan_no = fields.Char('EPF UAN No',store = True)
	# z_blood_group = fields.Many2one('group.name', string='Blood Group')
	
	#
	@api.depends('birthday')
	def _compute_age(self):
		for rec in self:
			if rec.birthday:
				dt = str(rec.birthday)
				d1 = datetime.strptime(dt, "%Y-%m-%d").date()
				d2 = datetime.today()
				rd = relativedelta(d2, d1)
				rec.age = str(rd.years) + ' years' 
				rec.z_age = rec.age

class Contract(models.Model):
	_inherit = 'hr.contract'

	hra = fields.Float(string='HRA')
	conveyance_allowance = fields.Float(string='Conveyance Allowance',store=True)
	education_allowance = fields.Float(string='Education Allowance',store=True)
	washing_allowance = fields.Float(string='Washing Allowance',store=True)
	attendance_bonus = fields.Float(string='Attendance Bonus',store=True)
	medical_allowance = fields.Float(string='Medical Allowance',store=True)
	mobile_data_allowance = fields.Float(string='Mobile / Data Allowance',store=True)
	overtime_allowance = fields.Float(string='Overtime Allowance',store=True)
	meal_allowance = fields.Float(string='Meal Allowance',store=True)
	city_compensatory_allowance = fields.Float(string='City Compensatory Allowance (CCA)',store=True)
	interim_allowance = fields.Float(string='Interim Allowance',store=True)
	cash_allowance = fields.Float(string='Cash Allowance',store=True)
	servant_allowance = fields.Float(string='Servant Allowance',store=True)
	project_allowance = fields.Float(string='Project Allowance',store=True)
	# epf_employee = fields.Integer(string='EPF Employee',store=True)
	# epf_employeer = fields.Integer(string='EPF Employeer',store=True)
	# epf_allow_over = fields.Boolean(string='EPF Allow Over Employeer',store=True)
	# epf_allow_over_employee = fields.Boolean(string='EPF Allow Over Employee',store=True)
	# esi_management = fields.Integer(string='ESI Management',store=True)
	# esi_employee = fields.Integer(string='ESI Employee',store=True)
	professional_tax = fields.Integer(string='Professtional Tax',store=True)
	bonus = fields.Integer(string='Bonus',store=True)
	rate_hour = fields.Float(string='Charges/Hour',store=True)
	gratuity_month = fields.Integer(string='Gratuity/Month',store=True)
	gratuity_year = fields.Integer(string='Gratuity/Year',store=True)
	other_deduction = fields.Integer(string='Other Deduction',store=True)
	applicable_for_ot = fields.Boolean(string="Applicable for OT")
	# esi_allow_over = fields.Boolean(string='ESI Allow Over Employeer',store=True)
	# esi_allow_over_employee = fields.Boolean(string='ESI Allow Over Employee',store=True)

	# @api.onchange('wage','epf_allow_over','epf_allow_over_employee')
	# def percentage_of_wage(self):
	# 	for l in self:
	# 		var = 0
	# 		if l.wage >= 15000:
	# 			l.epf_employee = (l.wage * 13) / 100
	# 			if l.epf_allow_over == False:
	# 				l.epf_employeer = (15000 * 13) / 100
	# 				# print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
	# 		else:
	# 			l.epf_employee = (l.wage * 12) / 100
	# 			if l.epf_allow_over == False:
	# 				l.epf_employeer = (l.wage * 13) / 100
	# 		if l.epf_allow_over == True:
	# 			l.epf_employeer = 0
	# 		if l.conveyance_allowance != 0 or l.education_allowance != 0 or l.washing_allowance !=0 or l.medical_allowance != 0:
	# 			var = l.wage + l.conveyance_allowance + l.education_allowance + l.washing_allowance + l.medical_allowance
	# 			l.epf_employee = (var * 12) / 100
	# 		if l.epf_allow_over_employee == True:
	# 			l.epf_employee = 0


	# @api.onchange('wage','hra','esi_allow_over','esi_allow_over_employee','attendance_bonus','conveyance_allowance','education_allowance','washing_allowance','medical_allowance')
	# def percentage_of_esi(self):
	# 	for l in self:
	# 		# print('SSSSSSSSSSSSSSSSSSSSSSSSSSS')
	# 		var = 0
	# 		att = 0
	# 		var = l.wage + l.hra + l.attendance_bonus + l.conveyance_allowance + l.education_allowance + l.washing_allowance + l.medical_allowance
	# 		att = var - l.washing_allowance
	# 		if var >= 21000:
	# 			l.esi_employee = ((21000-l.washing_allowance) * 0.75) / 100
	# 			l.esi_management = ((21000-l.washing_allowance) * 3.75) / 100
	# 		else:
	# 			l.esi_employee = (att * 0.75) / 100
	# 			l.esi_management = (att * 3.75) / 100
	# 		if l.esi_allow_over == True:
	# 			l.esi_management = 0
	# 		if l.esi_allow_over_employee == True:
	# 			l.esi_employee = 0
class HrPayslip(models.Model):
	_inherit = "hr.payslip"

	applicable_for_ot = fields.Boolean(string="Applicable for OT")

	@api.onchange('employee_id')
	def get_apply_ot(self):
		get_employee = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
		if get_employee:
			if get_employee.applicable_for_ot == True:
				self.write({'applicable_for_ot':True})
			else:
				self.write({'applicable_for_ot':False})