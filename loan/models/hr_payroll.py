# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime
import pdb


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line', string="Loan Installment")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # @api.onchange('employee_id', 'date_from', 'date_to','struct_id')
    # def onchange_employee(self):
    #     if (not self.employee_id) or (not self.date_from) or (not self.date_to):
    #         return

    #     employee = self.employee_id
    #     date_from = self.date_from
    #     date_to = self.date_to
    #     contract_ids = []

    #     ttyme = datetime.fromtimestamp(time.mktime(time.strptime(str(date_from), "%Y-%m-%d")))
    #     locale = self.env.context.get('lang') or 'en_US'
    #     self.name = _('Salary Slip of %s for %s') % (
    #     employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
    #     self.company_id = employee.company_id

    #     if not self.env.context.get('contract') or not self.contract_id:
    #         contract_ids = employee._get_contracts(date_from, date_to)
    #         if not contract_ids:
    #             return
    #         self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

    #     if not self.contract_id.struct_id:
    #         return
    #     self.struct_id = self.contract_id.struct_id
    #     self.input_line_ids = [(0,0,self.get_inputs())]

        # computation of the salary input
        # contracts = self.env['hr.contract'].browse(contract_ids)
        # worked_days_line_ids = self._get_new_worked_days_lines(contracts, date_from, date_to)
        # worked_days_lines = self.worked_days_line_ids.browse([])
        # for r in worked_days_line_ids:
        #     worked_days_lines += worked_days_lines.new(r)
        # self.worked_days_line_ids = worked_days_lines
        # if contracts:
        #     input_line_ids = self.get_inputs()
        #     input_lines = self.input_line_ids.browse([])
        #     for r in input_line_ids:
        #         input_lines += input_lines.new(r)
        #     self.input_line_ids = input_lines
        #return

    @api.onchange('struct_id')
    def get_inputs(self):
        contract_obj = self.env['hr.contract']
        #print(self.id,'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        #emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        lon_obj = self.env['hr.loan'].search([('employee_id', '=', self.contract_id.employee_id.id), ('state', '=', 'approve')])
        for loan in lon_obj:
            for loan_line in loan.loan_lines:
                #pdb.set_trace()
                if self.date_from <= loan_line.date <= self.date_to and not loan_line.paid:
                    for result in self.struct_id.input_line_type_ids:
                        if result.code == 'LO':
                            self.input_line_ids = [(0,0,
                                {
                                'name':result.name,
                                'code':result.code,
                                #'payslip_id':self.id,
                                'amount':loan_line.amount,
                                'contract_id':self.contract_id.id,
                                'loan_line_id':loan_line.id,
                                'input_type_id':result.id,})]
                            #print(int(str(self.id).split('=')[1][:-1]),'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
                            # self.env['hr.payslip.input'].create({
                            #     'name':result.name,
                            #     'code':result.code,
                            #     'payslip_id':self.id,
                            #     'amount':loan_line.amount,
                            #     'contract_id':self.contract_id.id,
                            #     'loan_line_id':loan_line.id,
                            #     'input_type_id':result.id,
                            #     })
        return

    def action_payslip_done(self):
        total = 0
        for line in self.input_line_ids:
            if line.loan_line_id:
               # print('*****************************************88')
                line.loan_line_id.paid = True
                if line.loan_line_id.paid == True:
                    total += line.loan_line_id.amount
                    for l in self:
                        l.employee_id.loan_balance =l.employee_id.loan_balance - total
                # var = self.env['hr.employee'].search([('id','=',self.employee_id.id)])
                # for l in var:
                #     rec = self.env['hr.loan'].search([('employee_id','=',self.employee_id.id)])
                #     print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')
                #     for j in rec:
                #         print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQS',l,j)
                #         if l == j:
                #             print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSss')
        return super(HrPayslip, self).action_payslip_done()

