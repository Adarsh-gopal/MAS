# -*- coding: utf-8 -*-

from odoo import models, fields, api
# import urllib.request as request
import requests
import pytz
from datetime import datetime , date , timedelta
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning


class CosecMonthly(models.Model):
    _name = 'cosec.month'
    _description = 'cosec.month'


    userid= fields.Char(string='USER ID')
    username = fields.Char(string='USER NAME')
    pyear = fields.Char(string="PROCESS YEAR")
    pmonth = fields.Integer(string="PROCESS MONTH")
    prdays = fields.Float(string="PRESENT DAYS")
    abdays = fields.Float(string="ABSENT DAYS")
    wodays = fields.Float(string="WEEK-OFF DAYS")
    phdays = fields.Float(string="PUBLIC HOLIDAY DAYS")
    pldays = fields.Float(string="PAID LEAVE DAYS")
    trdays = fields.Float(string="TOUR DAYS")
    uldays = fields.Float(string="UNPAID LEAVE DAYS")
    lodays = fields.Float(string="LAY OFF DAYS")
    work_time = fields.Integer(string="Working time")
    over_time = fields.Integer(string="Over time")



    """Function to fetch data from api and write datas on model"""

    def fetch_month_data(self):

        # url = 'http://150.129.62.191:8081/cosec/api.svc/v2/attendance-daily?action=get;field-name=userid,username,processdate,punch1,punch2,punch3,punch4,punch5,punch6,punch7,punch8,punch9,punch10,punch11,punch12,workingshift,latein,earlyout,overtime,worktime;format=json'
        userid = self.env['ir.config_parameter'].sudo().get_param('cosec.userid')
        url = self.env['ir.config_parameter'].sudo().get_param('cosec.url') + '/api.svc/v2/attendance-monthly?action=get;Field-name=USERID,USERNAME,PYEAR,PMONTH,PRDAYS,ABDAYS,WODAYS,PHDAYS,PLDAYS,TRDAYS,ULDAYS,LODAYS,OVERTIME,WORKTIME;format=json'
        password = self.env['ir.config_parameter'].sudo().get_param('cosec.password')
        response = requests.get(url,auth=(userid,password))
        json_response = response.json()
        print(json_response)
        
        for line in json_response['attendance-monthly']:
            checkval=self.env['cosec.month'].search([
                ('userid', '=', line['userid'])])
            print(checkval)

            if checkval:
                checkval.write({
                    'pyear':line['pyear'],
                    'pmonth':line['pmonth'],
                    'prdays':line['prdays'],
                    'abdays':line['abdays'],
                    'wodays':line['wodays'],
                    'phdays':line['phdays'],
                    'pldays':line['pldays'],
                    'trdays':line['trdays'],
                    'uldays':line['uldays'],
                    'lodays':line['lodays'],
                    'work_time':line['worktime'],
                    'over_time':line['overtime'],


                    })

            else:
                self.env['cosec.month'].create({                
                    'userid':line['userid'],
                    'username':line['username'],
                    'pyear':line['pyear'],
                    'pmonth':line['pmonth'],
                    'prdays':line['prdays'],
                    'abdays':line['abdays'],
                    'wodays':line['wodays'],
                    'phdays':line['phdays'],
                    'pldays':line['pldays'],
                    'trdays':line['trdays'],
                    'uldays':line['uldays'],
                    'lodays':line['lodays'],
                    'work_time':line['worktime'],
                    'over_time':line['overtime'],                    
                    })                    


    # """Function to validate the attendance and write on attendance"""

    # def validate_data(self):
    #     print(self)
    #     for rec in self:

    #         employid = self.env['hr.employee'].search([('cosec_id','=',rec.userid)])
    #         print(employid)

    #         self.env['hr.attendance'].create(
    #             {
    #             'employee_id':employid.id,
    #             'check_in':rec.punchin,
    #             'check_out':rec.punchout,
                
    #             })

                



        



