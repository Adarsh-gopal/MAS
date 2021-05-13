# -*- coding: utf-8 -*-

from odoo import models, fields, api
# import urllib.request as request
import requests
from datetime import datetime , date , timedelta
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning


class cosec(models.Model):
    _name = 'cosec.data'
    _description = 'cosec.data'


    userid = fields.Char(string='USER ID')
    username = fields.Char(string='USER NAME')
    processdate = fields.Date(string="processdate")
    punch1 = fields.Datetime(string="Punch 1")
    punch2 = fields.Datetime(string="punch2")
    punch3 = fields.Datetime(string="punch3")
    punch4 = fields.Datetime(string="punch4")
    punch5 = fields.Datetime(string="punch5")
    punch6 = fields.Datetime(string="punch6")
    punch7 = fields.Datetime(string="punch7")
    punch8 = fields.Datetime(string="punch8")
    punch9 = fields.Datetime(string="punch9")
    punch10 = fields.Datetime(string="punch10")
    punch11 = fields.Datetime(string="punch11")
    punch12 = fields.Datetime(string="punch12")
    workingshift = fields.Char(string="Working shift")
    latein = fields.Integer(string="Latein")
    earlyout = fields.Integer(string="Earlyout")
    overtime = fields.Integer(string="Overtime")
    worktime = fields.Integer(string="Work time")
    fun_one = fields.Char(string="Function1")
    fun_two = fields.Char(string="Function2")
    fun_three = fields.Char(string="Function3")
    fun_four = fields.Char(string="Function4")
    fun_five = fields.Char(string="Function5")
    fun_six = fields.Char(string="Function6")
    fun_seven = fields.Char(string="Function7")
    fun_eigth = fields.Char(string="Function8")
    fun_nine = fields.Char(string="Function9")
    fun_ten = fields.Char(string="Function10")
    fun_eleven = fields.Char(string="Function11")
    fun_twelve = fields.Char(string="Function12")
    first_half = fields.Char(string="First Half")
    second_half = fields.Char(string="Second Half")
    missed_punch = fields.Boolean(string="Missed Punch" ,store=True)
    missed_punchtwo = fields.Boolean(string="Missed Punch2" , store=True) 


    def fetch_data(self):

        # url = 'http://150.129.62.191:8081/cosec/api.svc/v2/attendance-daily?action=get;format=json'
        userid = self.env['ir.config_parameter'].sudo().get_param('cosec.userid')
        url = self.env['ir.config_parameter'].sudo().get_param('cosec.url') + '/api.svc/v2/attendance-daily?action=get;Field-name=USERID,USERNAME,PROCESSDATE,PUNCH1,PUNCH2,PUNCH3,PUNCH4,PUNCH5,PUNCH6,PUNCH7,PUNCH8,PUNCH9,PUNCH10,PUNCH11,PUNCH12,WORKINGSHIFT,LATEIN,EARLYOUT,OVERTIME,WORKTIME,SPFID1,SPFID2,SPFID3,SPFID4,SPFID5,SPFID6,SPFID7,SPFID8,SPFID9,SPFID10,SPFID11,SPFID12,FIRSTHALF,SECONDHALF;format=json'
        password = self.env['ir.config_parameter'].sudo().get_param('cosec.password')
        # print(url)
        response = requests.get(url,auth=(userid,password))
        json_response = response.json()
        spf_dict = {'0':False,
                    '1':'Official In',
                    '2':'Official out',
                    '3':'Short leave In',
                    '4':'Short leave Out',
                    '5':'Regular In',
                    '6':'Regular Out',
                    '7':'Lunch In',
                    '8':'Lunch Out',
                    '9':'Overtime In',
                    '10':'Over time out',}
        # print(json_response,"################3")
        for line in json_response['attendance-daily']:
            checkval=self.env['cosec.data'].search([
                ('userid', '=', line['userid']),('processdate', '=', datetime.strptime(line['processdate'],'%d/%m/%Y').date())])
            # # print(checkval)
            
            for x in range(1,13):

                line['spfid{}'.format(x)] = spf_dict.get(str(line['spfid{}'.format(x)]))


                    


                

                

        





            if checkval:
                checkval.write({
                    'punch1':datetime.strptime(line['punch1'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch1'] != '' else False,
                    'punch2':datetime.strptime(line['punch2'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch2'] != '' else False,
                    'punch3':datetime.strptime(line['punch3'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch3'] != '' else False,
                    'punch4':datetime.strptime(line['punch4'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch4'] != '' else False,
                    'punch5':datetime.strptime(line['punch5'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch5'] != '' else False,
                    'punch6':datetime.strptime(line['punch6'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch6'] != '' else False,
                    'punch7':datetime.strptime(line['punch7'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch7'] != '' else False,
                    'punch8':datetime.strptime(line['punch8'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch8'] != '' else False,
                    'punch9':datetime.strptime(line['punch9'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch9'] != '' else False,
                    'punch10':datetime.strptime(line['punch10'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch10'] != '' else False,
                    'punch11':datetime.strptime(line['punch11'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch11'] != '' else False,
                    'punch12':datetime.strptime(line['punch12'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch12'] != '' else False,
                    'workingshift':line['workingshift'],
                    'latein':line['latein'],
                    'earlyout':line['earlyout'],
                    'overtime':line['overtime'],
                    'worktime':line['worktime'],
                    'fun_one':line['spfid1'],
                    'fun_two':line['spfid2'],
                    'fun_three':line['spfid3'],
                    'fun_four':line['spfid4'],
                    'fun_five':line['spfid5'],
                    'fun_six':line['spfid6'],
                    'fun_seven':line['spfid7'],
                    'fun_eigth':line['spfid8'],
                    'fun_nine':line['spfid9'],
                    'fun_ten':line['spfid10'],
                    'fun_eleven':line['spfid11'],
                    'fun_twelve':line['spfid12'],
                    'first_half':line['firsthalf'],
                    'second_half':line['secondhalf'],
                    'missed_punch':True if line['punch1'] == '' and line['punch2'] == '' else False,
                    'missed_punchtwo':True if line['punch1'] != '' and line['punch2'] == '' else False,
                })

            else:
                self.env['cosec.data'].create({
                    'userid':line['userid'],
                    'username':line['username'],
                    'processdate':datetime.strptime(line['processdate'],'%d/%m/%Y').date() if line['processdate'] != '' else False,
                    'punch1':datetime.strptime(line['punch1'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch1'] != '' else False,
                    'punch2':datetime.strptime(line['punch2'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch2'] != '' else False,
                    'punch3':datetime.strptime(line['punch3'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch3'] != '' else False,
                    'punch4':datetime.strptime(line['punch4'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch4'] != '' else False,
                    'punch5':datetime.strptime(line['punch5'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch5'] != '' else False,
                    'punch6':datetime.strptime(line['punch6'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch6'] != '' else False,
                    'punch7':datetime.strptime(line['punch7'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch7'] != '' else False,
                    'punch8':datetime.strptime(line['punch8'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch8'] != '' else False,
                    'punch9':datetime.strptime(line['punch9'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch9'] != '' else False,
                    'punch10':datetime.strptime(line['punch10'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch10'] != '' else False,
                    'punch11':datetime.strptime(line['punch11'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch11'] != '' else False,
                    'punch12':datetime.strptime(line['punch12'],'%d/%m/%Y %H:%M:%S')- timedelta(hours=5, minutes=30) if line['punch12'] != '' else False,
                    'workingshift':line['workingshift'],
                    'latein':line['latein'],
                    'earlyout':line['earlyout'],
                    'overtime':line['overtime'],
                    'worktime':line['worktime'],
                    'fun_one':line['spfid1'],
                    'fun_two':line['spfid2'], 
                    'fun_three':line['spfid3'],
                    'fun_four':line['spfid4'], 
                    'fun_five':line['spfid5'],
                    'fun_six':line['spfid6'],
                    'fun_seven':line['spfid7'],
                    'fun_eigth':line['spfid8'],
                    'fun_nine':line['spfid9'],
                    'fun_ten':line['spfid10'],
                    'fun_eleven':line['spfid11'],
                    'fun_twelve':line['spfid12'],
                    'first_half':line['firsthalf'],
                    'second_half':line['secondhalf'],
                    'missed_punch':True if line['punch1'] == '' and line['punch2'] == '' else False,
                    'missed_punchtwo':True if line['punch1'] != '' and line['punch2'] == '' else False,
                })

                    
            # print(abc,"YYYYYYYYYYYYYYYYYYYYYYYY")        
    def validate_data(self):
        print(self)
        for rec in self:

            employid = self.env['hr.employee'].search([('cosec_id','=',rec.userid)])
            print(employid)

            self.env['hr.attendance'].create(
                {
                'employee_id':employid.id,
                'check_in':rec.punch1,
                'check_out':rec.punch2,
                'worked_hours':rec.worktime,
                })

                


            # validcos = self.env['hr.employee'].search([
            #     ('cosec_id','=','userid')])
            # if validcos:
            #     print(self)
            # else:
            #     print('skfuh')