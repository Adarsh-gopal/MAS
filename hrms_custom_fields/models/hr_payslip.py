from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError


class Hrpayslip(models.Model):
    _inherit = 'hr.payslip'

    final_settlement_information = fields.Boolean(string="F&F Payslip")

    #fields for F&F Settlement
    last_working_day= fields.Date()
    submission_date_of_resignation = fields.Date()
    date_of_relieving= fields.Date()
    last_salary_paid_date =fields.Date()
    notice_period_as_per_application = fields.Char()
    notice_period_adjustable = fields.Char()
    informed_client = fields.Selection([('yes','Yes'),('no','No')])
    number_of_months_served = fields.Float()

    def action_payslip_done(self):
        for l in self:
            con = super(Hrpayslip,self).action_payslip_done()
            contract = self.env['hr.contract'].search([('employee_id','=',l.employee_id.id)])
            for r in contract:
                if l.final_settlement_information == True:
                    if r.state == 'draft' or r.state == 'open':
                        r.state = 'close'
        return con


    @api.onchange('date_to')
    def update_salarydate_to_employee(self):
        if self.final_settlement_information == False:
            employee = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
            self.write({'last_salary_paid_date':self.date_to})


    @api.onchange('final_settlement_information','employee_id')
    def get_fandf_informations(self):
        if self.final_settlement_information and self.employee_id:
            self.last_working_day = self.employee_id.notice_period
            self.submission_date_of_resignation = self.employee_id.resigned_date
            self.date_of_relieving = self.employee_id.notice_period
            # self.last_salary_paid_date = self.employee_id.last_salary_paid_date
            # self.notice_period_as_per_application = self.employee_id.notice_period_as_per_application
            self.notice_period_adjustable = self.employee_id.notice_period_adjustable
            self.informed_client = self.employee_id.informed_client
            self.number_of_months_served = self.employee_id.number_of_months_served
