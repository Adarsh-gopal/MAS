from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError, Warning
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare



from werkzeug.urls import url_encode


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()

        if self.partner_id:
            if not self.partner_id.customer:
                raise AccessError('This customer is not approved. Kindly get the contact approved')


        return res



class PuchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PuchaseOrder,self).button_confirm()

        if self.partner_id:
            if not self.partner_id.vendor:
                raise AccessError('This vendor is not approved. Kindly get the contact approved')

        return res
