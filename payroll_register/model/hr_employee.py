	# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
import pytz
from odoo.exceptions import AccessError, UserError, ValidationError

class HrEmployee(models.Model):
	_inherit = "hr.employee"


	pf_no = fields.Char(string="PF No")
	esi_no = fields.Char(string="ESI No")

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'


    related_job_title = fields.Char(related="employee_id.job_id.name",readonly=True)
    related_pf_no = fields.Char(related='employee_id.pf_no', readonly=True)
    related_registered_id = fields.Char(related='employee_id.registration_number', readonly=True)
    related_identify_id = fields.Char(related='employee_id.identification_id', readonly=True)
    # job_id = fields.Many2one('hr.job')