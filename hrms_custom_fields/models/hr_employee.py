from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import date ,datetime
from dateutil import relativedelta
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta
import math



class HrEmployee(models.Model):
	_inherit = "hr.employee"

	#personnel details block
	blood_group = fields.Selection([('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], string='Blood Group')
	father_name = fields.Char('Father Name')
	mother_name = fields.Char('Mother Name')
	skype_id = fields.Char()
	employee_status= fields.Many2one('employee.status')

	#empoyment offered details
	offer_date = fields.Date()
	date_of_joining = fields.Date()
	
	offered_salary = fields.Float()
	remarks = fields.Text()
	hire_type = fields.Selection([('internal','Internal'),('external','External')])
	title = fields.Many2one('res.partner.title')

	#field will store Employee photo for thier Employee ID card
	photo_for_id =fields.Binary(string="Photo for ID")
	universal_account_number = fields.Char(string="UAN")
	provident_fund = fields.Char(string="PF Number")
	esi_number = fields.Char(string="ESI Number")

	#pan details of the employee
	pan_no = fields.Char(string="Pancard Number")
	pan_doc = fields.Binary(string="PAN Doc")

	aadhar_doc = fields.Binary(string="Aadhar Doc")
	aadhar_number = fields.Char(string="Aadhar Number")
	driving_licence_number = fields.Char('Driving Licence Number') 

	certificate_of_fitness = fields.Binary(string="Certificate of Fitness")

	#Education related fields
	employee_degree = fields.Many2many('hr.employee.degree')
	degree_type = fields.Many2one('hr.employee.degree.type', "Degree Type")
	division = fields.Many2one('hr.employee.degree.division', "Division")
	year_of_pass = fields.Selection([((str(num)), (str(num))) for num in range(1900, (datetime.now().year)+1)], 'Year of Pass')
	# year_of_pass = fields.Date("Year of Pass")
	university_name = fields.Char("University Name")
	percentage = fields.Float("Percentage %")
	qualification = fields.Char("Qualification")
	religion = fields.Many2one('hr.religion',string='Religion')

	#emergency contact details
	relation_with_employee = fields.Char(string="Relation")
	emergency_contact_city = fields.Char(string="City")
	emergency_contact_state = fields.Many2one("res.country.state")
	emergency_contact_country = fields.Many2one("res.country")

	#skills management
	# fresher = fields.Boolean('Fresher')
	# experienced = fields.Boolean('Experienced')
	experience_level = fields.Selection([('fresher', 'Fresher'), ('experienced', 'Experienced')], string="Experience Level",default='fresher')
	domain = fields.Many2one('hr.employee.domain')
	last_working_company = fields.Many2one('res.partner')
	last_drawn_salary = fields.Integer("Last Drawn Salary")
	last_company_department = fields.Char("Last Company Department")
	last_company_designation = fields.Char("Last Company Designation")
	last_working_day = fields.Date("Last Working Day")
	start_date_of_career = fields.Date("Start Date of Career") 
	last_company_employeed_code = fields.Char("Last Company Employee Code")
	reason_for_leaving = fields.Text("Reason for Leaving")
	total_years_of_experience = fields.Float("Total Years of Experience")
	relevant_years_of_experience = fields.Float("Relevant Years of Experience")
	relevant_yrs_of_exp_till_date = fields.Float("Relevant Years of Experience Till Date",compute="get_relavant_yrs_till_date", store=True)



	#experienced documents
	previous_company_salary_slip = fields.Binary("Previous Company Salary Slip (3 Months)")
	last_company_releiving_letter =fields.Binary("Last Company releiving letter")
	last_company_experience_letter =fields.Binary("Last Company experience letter")
	last_company_offer_letter =fields.Binary("Last Company offer letter")


	#present and permanent address

	street_present = fields.Char(compute='getaddress',store=True)
	street2_present = fields.Char(compute='getaddress',store=True)
	zip_present = fields.Char(compute='getaddress',store=True, change_default=True)
	city_present = fields.Char(compute='getaddress',store=True)
	state_id_present = fields.Many2one("res.country.state",compute='getaddress',store=True,  ondelete='restrict', domain="[('country_id', '=?', country_id)]")
	country_id_present = fields.Many2one('res.country', compute='getaddress',store=True,  ondelete='restrict')


	street_permanent = fields.Char(compute='getaddress',store=True)
	street2_permanent = fields.Char(compute='getaddress',store=True)
	zip_permanent = fields.Char(compute='getaddress',store=True, change_default=True)
	city_permanent = fields.Char(compute='getaddress',store=True)
	state_id_permanent = fields.Many2one("res.country.state",compute='getaddress',store=True, ondelete='restrict', domain="[('country_id', '=?', country_id)]")
	country_id_permanent = fields.Many2one('res.country',compute='getaddress',store=True, ondelete='restrict')

	#off board 
	offboarding_type = fields.Selection([('exit_from_company', 'Exit From Company')], string="Select Type")
	resigned_date = fields.Date()
	get_last_working_day = fields.Selection([('system', 'System'),('custom', 'Custom')], string="Get Last Working Day")
	notice_period = fields.Date(string="Notice Period(System Generate 2 months)",compute='get_notice_period')
	reason_for_resigning = fields.Many2one('hr.resign.reason')
	informed_client = fields.Selection([('yes','Yes'),('no','No')])
	notice_period_adjustable = fields.Char()
	job_category = fields.Many2one('hr.job.category',string='Job Category')

	#offboard_from project
	#offboard_date_from_current_project = fields.Date()
	reasons_for_offboarding = fields.Many2one('hr.offboarding.reason')
	number_of_months_served = fields.Float(string='Number of Months Served',store=True,tracking=True,compute='get_months_served')
	# off_board_type = fields.Selection([('bench', 'Bench')], string="Off Board Type")



	#off boarding details
	off_board = fields.Boolean()
	registration_number = fields.Char("	Registration Number of the Employee",copy=False, default=lambda self: _('New'))

	#probation and confirmation fields
	confirmation_types = fields.Selection([('probation', 'Probation'),('pip', 'PIP'),('confirmed', 'Confirmed')], string="Confirmation Type")
	pip_duration = fields.Selection([('1_month', '1 Month'),('2_month', '2 Month'),('3_month', '3 Month')], string="PIP Duration")
	confirmation_date = fields.Date(string='Confirmation Date',compute="get_confirmation_date",store=True)

	@api.depends('date_of_joining','confirmation_types')
	def get_confirmation_date(self):
		for rec in self:
			if rec.date_of_joining and rec.confirmation_types == 'confirmed':
				rec.confirmation_date = rec.date_of_joining + relativedelta.relativedelta(months=3)
			else:
				rec.confirmation_date = False

	@api.model
	def create(self, vals):
		if 'nameregistration_number' not in vals or vals['registration_number'] == _('New'):		
			if self.env.company.id == 1:
				vals['registration_number'] = self.env['ir.sequence'].next_by_code('hr.employee.india')
			else:
				vals['registration_number'] = self.env['ir.sequence'].next_by_code('hr.employee.singapore')
		result = super(HrEmployee, self).create(vals)
		return result


	@api.depends('date_of_joining')
	def get_relavant_yrs_till_date(self):
		for rec in self:
			if rec.date_of_joining:
				start_date = rec.date_of_joining
				today = date.today() 

				diff = relativedelta.relativedelta(today, start_date)

				years = diff.years
				months = diff.months
				days = diff.days
				total_years_string = str(years) +"."+str("{:02d}".format(months))
				total_years_exp = rec.relevant_years_of_experience + float(total_years_string)
				exp_split = str(total_years_exp).split('.')
				if int(exp_split[1])>12:
					exp_split[0] = int(exp_split[0]) + 1 
					exp_split[1] = int(exp_split[1]) - 12
					total_years_exp = str(exp_split[0]) +"."+str("{:02d}".format(exp_split[1]))
				
				rec.relevant_yrs_of_exp_till_date = total_years_exp
			else:
				rec.relevant_yrs_of_exp_till_date = rec.relevant_years_of_experience




	@api.depends('get_last_working_day','resigned_date','notice_period_adjustable')
	def get_notice_period(self):
		for rec in self:
			if rec.get_last_working_day == 'system' and rec.resigned_date:
				start_date = rec.resigned_date
				# today = date.today() 
				two_months = start_date + relativedelta.relativedelta(months=1)
				rec.notice_period = two_months
			elif rec.get_last_working_day == 'custom' and rec.notice_period_adjustable:
				start_date = rec.resigned_date
				np_date= start_date + relativedelta.relativedelta(days=int(rec.notice_period_adjustable))
				rec.notice_period = np_date
			else:
				rec.notice_period = rec.notice_period

	@api.depends('notice_period')
	def get_months_served(self):
		for rec in self:
			var = self.env['hr.contract'].search([('employee_id','=',rec.id)])
			if rec.notice_period:
				for l in var:
					s = (l.date_start)
					r = (rec.notice_period)
					print(s,r,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
					d1 = datetime.strptime(str(s), "%Y-%m-%d").date()
					d2 = datetime.strptime(str(r), "%Y-%m-%d").date()
					rd = (d2 - d1).days
					rec.number_of_months_served = (rd / 30)

	# @api.depends('get_last_working_day','resigned_date','notice_period_adjustable')
	# def get_custom_np(self):
	# 	for rec in self:
	# 		if rec.get_last_working_day == 'custom' and rec.notice_period_adjustable:
	# 			start_date = rec.resigned_date
	# 			np_date= start_date + relativedelta.relativedelta(days=int(rec.notice_period_adjustable))
	# 			rec.notice_period = np_date
	# 		else:
	# 			rec.notice_period = rec.notice_period
	@api.model
	def send_birthday_wish(self):
		today_date = datetime.today().date()
		for employee in self.env['hr.employee'].search([]):
			if employee.birthday:
				if today_date.day == employee.birthday.day and today_date.month == employee.birthday.month:
					template_id = self.env.ref('hrms_custom_fields.email_birthday_wishes_employee_template')
					template_id.send_mail(employee.id, force_send=True)



	@api.depends('address_home_id')
	def getaddress(self):
		for address in self:
			address.street_present = address.address_home_id.street_present
			address.street2_present = address.address_home_id.street2_present
			address.zip_present = address.address_home_id.zip_present
			address.city_present = address.address_home_id.city_present
			address.state_id_present = address.address_home_id.state_id_present
			address.country_id_present = address.address_home_id.country_id_present
			address.street_permanent = address.address_home_id.street_permanent
			address.street2_permanent = address.address_home_id.street2_permanent
			address.zip_permanent = address.address_home_id.zip_permanent
			address.city_permanent = address.address_home_id.city_permanent
			address.state_id_permanent = address.address_home_id.state_id_permanent
			address.country_id_permanent = address.address_home_id.country_id_permanent

	def activate_offboard(self):
		if self.off_board:
			self.write({'off_board': False})
		else:
			self.write({'off_board': True})


	def send_docs_by_mail(self):
		# template = self.env.ref('instellars_offer_release.offer_letter_template', False)
		compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
		ctx = dict(
		    default_model="hr.employee",
		    default_res_id=self.id,
		    # default_use_template=bool(template),
		    # default_template_id=template.id,
		    default_composition_mode='comment',
		    mail_post_autofollow = False,
		    custom_layout='mail.mail_notification_light',
		)
		return {
		    
		    'type': 'ir.actions.act_window',
		    'view_mode': 'form',
		    'res_model': 'mail.compose.message',
		    'views': [(compose_form.id, 'form')],
		    'view_id': compose_form.id,
		    'target': 'new',
		    'context': ctx,
		}



class Bank(models.Model):
    _inherit = 'res.bank'

    bank_branch = fields.Char('Branch')
    bank_ifsc_code = fields.Char('Bank IFSC Code')

class HRReligion(models.Model):
    _name = 'hr.religion'
    _description = 'Religion'

    name = fields.Char('Name')

class HRJobCategory(models.Model):
    _name = 'hr.job.category'
    _description = 'Job Category'

    name = fields.Char('Name')


# class ResumeLine(models.Model):
#     _inherit = 'hr.resume.line'






