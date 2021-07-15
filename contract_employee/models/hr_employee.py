from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError, Warning
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

from werkzeug.urls import url_encode

class ContractEmployee(models.Model):
    _inherit = "hr.employee"

    is_contract=fields.Boolean('Contract Employee', default=False,store=True)

    # def action_confirm(self):
    #     res = super(Employee,self).action_confirm()

    #     if self.employee_id:
    #         if not self.employee_id.is_contract:
    #             raise AccessError('This employee is not approved. Kindly get the employee approved')

    #     return res