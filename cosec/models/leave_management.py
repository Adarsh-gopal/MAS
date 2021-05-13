# -*- coding: utf-8 -*-

from odoo import models, fields, api
# import urllib.request as request
import requests
import pytz
from datetime import datetime , date , timedelta
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning


class LeaveManagement(models.TransientModel):
    _name = 'leave.management'
    _description = 'leave.management'


    userid= fields.Char(string='USER ID')
    username = fields.Char(string='USER NAME')
    leave_code = fields.Char(string="Leave Code")
    leave_name = fields.Char(string="Leave Name")
    leave_period = fields.Char(string="Period" )
    opening_balance = fields.Float(string="Opening balance")
    closing_balance = fields.Float(string="Closing balance")
    leave_credit = fields.Float(string="Credit")
    leave_debit = fields.Float(string="Debit")
    leave_encashed = fields.Float(string="Encashed")
    leave_availed = fields.Float(string="Availed")
    leave_overflow = fields.Float(string="Overflow")



    """Function to fetch data from api and write datas on model"""

    def fetch_leave_data(self):

        # url = 'http://150.129.62.191:8081/cosec/api.svc/v2/attendance-daily?action=get;field-name=userid,username,processdate,punch1,punch2,punch3,punch4,punch5,punch6,punch7,punch8,punch9,punch10,punch11,punch12,workingshift,latein,earlyout,overtime,worktime;format=json'
        # url = 'http://150.129.62.191:8081/cosec/api.svc/v2/attendance-monthly?action=get;Field-name=USERID,USERNAME,PYEAR,PMONTH,PRDAYS,ABDAYS,WODAYS,PHDAYS,PLDAYS,TRDAYS,ULDAYS,LODAYS;format=json'
        get_cosec_id = self.env['hr.employee'].search([('cosec_id','!=',None)])
        # print(get_cosec_id.cosec_id,"###############!!!!!!!!!!!!!!")

        for each_cosec in get_cosec_id:

            userid = self.env['ir.config_parameter'].sudo().get_param('cosec.userid')
            url = self.env['ir.config_parameter'].sudo().get_param('cosec.url') + '/api.svc/v2/leave-balance?action=get;format=json;userid={}'.format(each_cosec.cosec_id)
            print(url)
            password = self.env['ir.config_parameter'].sudo().get_param('cosec.password')
            response = requests.get(url,auth=(userid,password))
            json_response = response.json()
            print(json_response)
        
            
            for line in json_response['leave-balance']:
                checkval=self.env['leave.management'].search([
                    ('userid', '=', line['user-id']),('leave_code','=',line['leave-code'])])
                print(checkval)

                if checkval:
                    checkval.write({
                        'leave_code':line['leave-code'],
                        'leave_name':line['leave-name'],
                        'leave_period':line['period'],
                        'opening_balance':line['opening-balance'],
                        'closing_balance':line['closing-balance'],
                        'leave_credit':line['credit'],
                        'leave_debit':line['debit'],
                        'leave_encashed':line['encashed'],
                        'leave_availed':line['availed'],
                        'leave_overflow':line['overflow'],


                        })

                else:
                    self.env['leave.management'].create({                
                        'userid':line['user-id'],
                        'username':line['user-name'],
                        'leave_code':line['leave-code'],
                        'leave_name':line['leave-name'],                    
                        'leave_period':line['period'],
                        'opening_balance':line['opening-balance'],
                        'closing_balance':line['closing-balance'],
                        'leave_credit':line['credit'],
                        'leave_debit':line['debit'],
                        'leave_encashed':line['encashed'],
                        'leave_availed':line['availed'],
                        'leave_overflow':line['overflow'],
                        })    

        



