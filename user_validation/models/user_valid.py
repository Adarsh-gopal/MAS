# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models, tools, _

from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError, RedirectWarning, except_orm, UserError, AccessError, Warning
import json
import re
import uuid
from functools import partial
import itertools 
from itertools import groupby
import operator
from operator import itemgetter
import psycopg2
from odoo.tools import pycompat
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime
from datetime import datetime


from odoo.addons import decimal_precision as dp


from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode
from collections import namedtuple
import time

from odoo.tools.float_utils import float_compare, float_round

from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.tools.misc import formatLang


import logging

class ResUsers(models.Model):
  _inherit = ['res.users']
  sale_order = fields.Boolean('Sale Order',store = True)
  purchase_order = fields.Boolean(' Purchase Order',store = True)
  invoice_id = fields.Boolean('Account Invoice',store = True)
  payment_id = fields.Boolean('Payments',store= True)
  product_id = fields.Boolean('Products',store = True)
  customer_id = fields.Boolean('Customers',store = True)
  # material_id = fields.Boolean('Approve Requisition',store = True)
  confirm_id = fields.Boolean('Confirm Transfer',store = True)
  journal_id = fields.Boolean('Journal Entry',store = True)

# class AccountJournal(models.Model):
# 	_inherit = ['account.journal']
# 	approved_on_ceiling = fields.Boolean('Approval On Ceiling',store = True)
# 	allowed_limit = fields.Monetary('Allowed Limit',store = True)
# 	enable_jentry_posting = fields.Boolean('Enable Journal Entry Posting',store = True)


class JournalEntries(models.Model):
	_inherit = ['account.move']
	current_user = fields.Many2one('res.users','Current User')

	def action_post(self):

		user = self.env.user
		# if not self.journal_id.enable_jentry_posting:
		if not user.journal_id:
			raise UserError(_('You are not authorized to post the document'))

		return super(JournalEntries, self).action_post()
	

class AccountPayment(models.Model):
	_inherit = ['account.payment']
	# allowed_limit = fields.Monetary('Approved On Ceiling',store = True,related = 'journal_id.allowed_limit')
	# approved_on_ceiling = fields.Boolean('Approval On Ceiling',store = True,related = 'journal_id.approved_on_ceiling')
	current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
	check_payment= fields.Boolean('Allow Payment',store =True,related = "current_user.payment_id",readonly=False)

	def action_post(self):

		user = self.env.user
		if not user.payment_id:
			raise UserError(_('You are not authorized to post the document'))

		# if self.journal_id.approved_on_ceiling == True:
		# 	if self.amount >= self.allowed_limit:
		# 		raise UserError('Payment limit exceeded, you are not authorized')

		return super(AccountPayment, self).action_post()



class SaleOrder(models.Model):
	_inherit = ['sale.order']

	def action_confirm(self):

		user = self.env.user
		if not user.sale_order:
			# import pdb
			# pdb.set_trace()
			raise UserError(_('You are not authorized to post the document'))

		return super(SaleOrder, self).action_confirm()


	current_user = fields.Many2one('res.users','Current User')
	check_sale = fields.Boolean('Check')

class PurchaseOrder(models.Model):
	_inherit = ['purchase.order']

	def button_confirm(self):

		user = self.env.user
		if not user.purchase_order:
			raise UserError(_('You are not authorized to post the document'))

		# if self.state != 'approved':
		# 	raise UserError(_('Please Approved the document'))

		return super(PurchaseOrder, self).button_confirm()

	current_user = fields.Many2one('res.users','Current User')
	check_sale = fields.Boolean('Check')



class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
    	user = self.env.user
    	if not user.confirm_id:
    		raise UserError(_('You are not authorized to vallidate the document'))
    	return super(Picking, self).button_validate()





	