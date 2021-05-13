# -*- coding: utf-8 -*-

from odoo import models, fields, api
# import urllib.request as request
import requests
from datetime import datetime , date
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning

class employee(models.Model):
	_inherit = 'hr.employee'


	cosec_id = fields.Char(string="Cosec ID")

	