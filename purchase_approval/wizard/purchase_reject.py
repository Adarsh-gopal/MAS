# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context


class Purchaseremarks(models.TransientModel):
    _name = 'purchase.approval.remarks'
    _description = 'purchase.approval.remarks'

    remarks = fields.Char( string='Remaks', required=True)
    
   

    def reject_order(self):
        print("asbdjdbjk")
        active_id =self.env.context['active_id']
        current_id=self.env['purchase.order'].search([('id','=',active_id)])
        for each in  current_id.purchase_approval_line:
            if (self.env.user.id in each.user_ids.ids and  each.is_approve == False ) and current_id.amount_total< each.amount :
                each.remarks = self.remarks
                break
            else:

                raise UserError (_("You can't reject the order"))
                break

        