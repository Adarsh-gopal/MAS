from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.fields import Date

class Lead(models.Model):
	_inherit = "crm.lead"

	project_id = fields.Many2one('project.project' ,string="Project Name")
	certification_type = fields.Many2one('hr.skill.type', string="Skill Type")
	certification = fields.Many2many('hr.skill', string="Skill")
	# experience_min_max = fields.Many2one('experience.range', string="Experience(min-max)")
	years_of_exp_min = fields.Selection([((str(r)), (str(r))) for r in range(1, 13)],'Years of Experience(Min)')
	years_of_exp_max = fields.Selection([((str(r)), (str(r))) for r in range(1, 13)],'Years of Experience(Max)')
	delivery_site = fields.Many2one('delivery.sites', string="Delivery Site")
	demand_closed_date = fields.Date()
	employee_assigned = fields.Many2one('hr.employee')
	employee_assigned_date = fields.Date()
	job_description = fields.Binary('Job Description')
	domain =  fields.Many2one('hr.employee.domain')
	is_demand =  fields.Boolean()
	product_id = fields.Many2one('product.product', domain=[('type', '=', 'service'), ('invoice_policy', '=', 'delivery'), ('service_type', '=', 'timesheet')], string="Service", help="Product of the sales order item. Must be a service invoiced based on timesheets on tasks.")
	demand_status = fields.Selection([('open','Open'),('close','Close')], compute="get_demand_status")

	#coneverting string to foloat for filter purpose

	exp_min_val_float =fields.Float(compute="get_float_value_exp", store=True)
	exp_max_val_float =fields.Float(compute="get_float_value_exp", store=True)


	#for calculation purpose
	is_employee_assigned = fields.Boolean(compute="change_employee_status", store=True)

	@api.depends('employee_assigned')
	def change_employee_status(self):
		for rec in self:
			if rec.employee_assigned:
				rec.is_employee_assigned = True
				emp = self.env['hr.employee'].search([('id', '=', rec.employee_assigned.id)])
				emp.write({'employee_status':2})

	@api.depends('years_of_exp_min','years_of_exp_max')
	def get_float_value_exp(self):
		for rec in self:
			rec.exp_min_val_float = float(rec.years_of_exp_min)
			rec.exp_max_val_float = float(rec.years_of_exp_max)



	@api.depends('demand_closed_date')
	def get_demand_status(self):
		for rec in self:
			if rec.demand_closed_date:
				if rec.demand_closed_date < Date.today():
					rec.demand_status = 'close'
				else:
					rec.demand_status = 'open'
			else:
				rec.demand_status = None
