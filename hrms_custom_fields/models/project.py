from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError

class Project(models.Model):
    _inherit = 'project.project'

    #projects star and end details
    date_start = fields.Date('Project Start Date')
    date_end = fields.Date('Project End Date')

    engagement_model = fields.Selection([('staff_augmentation', 'Staff Augmentation'), ('manage_services', 'Manage Services')], string="Engagement Model")
    project_extension = fields.Selection([('extendable', 'Extendable'), ('not_extendable', 'Not Extendable')], string="Project Extension")
    no_of_resource_in_the_project = fields.Integer()

    skills_rate_card_line_items = fields.One2many('skills.rate.card.lines', 'project_id', string="Rate Card Line Items")
    lead_count = fields.Integer(compute='_compute_lead_count', string="Lead Count")



    def _compute_lead_count(self):
        for rec in self:
            demand_data = self.env['crm.lead'].search([('project_id', '=', rec.id),('type','=','lead'),('is_demand','=',True)])
            rec.lead_count = len(demand_data)
        # lead_data = self.env['crm.lead'].read_group([('project_id', 'in', self.ids), ('type', '=', 'lead')], ['project_id'], ['project_id'])
        # # print('***********************************************',self.id,'********************************8')
        # result = dict((data['project_id'][0], data['project_id_count']) for data in lead_data)
        # for project in self:
        #     project.lead_count = result.get(project.id, 0)


class SillSetRateCard(models.Model):
    _name = 'skills.rate.card.lines'
    _description = "skills rate card lines"


    project_id = fields.Many2one('project.project', required=True)
    engagement_model = fields.Selection([('staff_augmentation', 'Staff Augmentation'), ('manage_services', 'Manage Services')], string="Engagement Model")
    delivery_site = fields.Many2one('delivery.sites')
    project_skill = fields.Many2one('hr.skill.type')
    duration_of_working = fields.Float()
    domain =  fields.Many2one('hr.employee.domain')
    rate_card_type = fields.Selection([('hourly','Hourly'),('daily','Daily'),('monthly','Monthly')])

    # no_of_years_of_exp_min = fields.Many2one('experience.range', 'No of Years of Experience (Min)')
    # no_of_years_of_exp_max = fields.Many2one('experience.range', 'No of Years of Experience (Max)')
    years_of_exp_min = fields.Selection([((str(r)), (str(r))) for r in range(1, 13)],'Years of Experience(Min)')
    years_of_exp_max = fields.Selection([((str(r)), (str(r))) for r in range(1, 13)],'years of Experience(Max)')
    currency = fields.Many2one('res.currency')
    rate = fields.Float()
    rate_start_date = fields.Date()
    rate_start_end_date =fields.Date()


        

