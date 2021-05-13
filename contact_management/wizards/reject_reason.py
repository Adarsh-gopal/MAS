import uuid

from odoo import api, fields, models, _
from odoo.fields import Date
from odoo.exceptions import ValidationError

from werkzeug.urls import url_encode


class ContactRejectReason(models.TransientModel):
    _name = 'contact.reject.reason'
    _description = 'get reasons for not approved'


    @api.model
    def default_get(self, fields):
        result = super(ContactRejectReason, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        cust_type = self.env.context.get('customer_type')
        result['customer_type'] = cust_type

        record = self.env['res.partner'].sudo().browse(active_id)
        if record:
            result['partner_id'] = record.id
            
        return result 

    customer_type = fields.Char()
    partner_id = fields.Many2one('res.partner')
    reasons = fields.Text('Reject Reason')



    def update_reason(self):
        if self.partner_id:
            if self.customer_type == 'customer':
                mesg = """ 
                    <p style="color:red;">%s</p>
                """%(self.reasons)
  
                self.partner_id.message_post(body=mesg)
                self.partner_id.write({'customer':False})
                # self.partner_id.write({'customer':False,'customer_reject_reason':self.reasons})
            if self.customer_type == 'vendor':
                mesg = """ 
                    <p style="color:red;">%s</p>
                """%(self.reasons)
    
                self.partner_id.message_post(body=mesg)
                self.partner_id.write({'vendor':False})
                # self.partner_id.write({'vendor':False,'vendor_reject_reason':self.reasons})

            return True
    