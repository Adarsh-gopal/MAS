# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import itertools
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class ResPartner(models.Model):
    _inherit = 'res.partner'




    def approve_customer(self):
        self.message_post(body='Customer Approved')
        res = self.write({'customer':True})
        return res

    def approve_vendor(self):
        self.message_post(body='Vendor Approved')
        res = self.write({'vendor':True})
        return res

    # def reject_customer(self):
    #     res = self.write({'customer':False})
    #     return res

    # def reject_vendor(self):
    #     res = self.write({'vendor':False})
    #     return res