# -*- coding: utf-8 -*-
import time
from odoo import models, api, _
from odoo.exceptions import except_orm,UserError, ValidationError


class HrLoanAcc(models.Model):
    _inherit = 'hr.loan'

    # @api.multi
    def action_approve(self):
        """This create account move for request.
            """
        loan_approve = self.env['ir.config_parameter'].sudo().get_param('account.loan_approve')
        loan_amount = float(self.env['ir.config_parameter'].sudo().get_param('account.loan_amount'))
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise UserError(_('You must Define a contract for employee'))
        if not self.loan_lines:
            raise UserError(_('You must compute installment before Approved'))
        if loan_approve:
            self.write({'state': 'waiting_approval_2'})
        if self.state == 'waiting_approval_2' and loan_amount >= self.loan_amount:
            if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError(_(
                                 "You must enter employee account & Treasury account and journal to approve "))
            if not self.loan_lines:
                raise UserError(_('You must compute Loan Request before Approved'))
            timenow = time.strftime('%Y-%m-%d')
            for loan in self:
                amount = loan.loan_amount
                loan_name = loan.employee_id.name
                reference = loan.name
                journal_id = loan.journal_id.id
                debit_account_id = loan.treasury_account_id.id
                credit_account_id = loan.emp_account_id.id
                debit_vals = {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'move_id': loan.id,
                }
                credit_vals = {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'move_id': loan.id,
                }
                vals = {
                    #'name': 'Loan For' + ' ' + loan_name,
                    'narration': loan_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'date': timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                # print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',vals)
                move = self.env['account.move'].create(vals)
                move.post()
            self.write({'state': 'approve'})
            for line in self:
                var = self.env['hr.employee'].search([('id','=',line.employee_id.id)])
                for l in var:
                    l.loan_id = line.id
                    if self.state == 'approve':
                        l.loan_balance = line.balance_amount + l.loan_balance
        return True

    # @api.multi
    def action_double_approve(self):
        """This create account move for request in case of double approval.
            """
        loan_amount = float(self.env['ir.config_parameter'].sudo().get_param('account.loan_amount'))
        if self.state == 'waiting_approval_2' and loan_amount < self.loan_amount:
            if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError(_("You must enter employee account & Treasury account and journal to approve "))
            if not self.loan_lines:
                raise UserError(_('You must compute Loan Request before Approved'))
            timenow = time.strftime('%Y-%m-%d')
            for loan in self:
                amount = loan.loan_amount
                loan_name = loan.employee_id.name
                reference = loan.name
                journal_id = loan.journal_id.id
                debit_account_id = loan.treasury_account_id.id
                credit_account_id = loan.emp_account_id.id
                debit_vals = {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'move_id': loan.id,
                }
                credit_vals = {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'move_id': loan.id,
                }
                vals = {
                    'name': 'Loan For' + ' ' + loan_name,
                    'narration': loan_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'date': timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.post()
            self.write({'state': 'approve'})
            return True


class HrLoanLineAcc(models.Model):
    _inherit = "hr.loan.line"

    # @api.one
    def action_paid_amount(self):
        """This create the account move line for payment of each installment.
            """
        timenow = time.strftime('%Y-%m-%d')
        for line in self:
            if line.loan_id.state != 'approve':
                raise UserError(_("Loan Request must be approved"))
            amount = line.amount
            loan_name = line.employee_id.name
            reference = line.loan_id.name
            journal_id = line.loan_id.journal_id.id
            debit_account_id = line.loan_id.emp_account_id.id
            credit_account_id = line.loan_id.treasury_account_id.id
            debit_vals = {
                'name': loan_name,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
            }
            credit_vals = {
                'name': loan_name,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
            }
            """vals = {
                'name': 'Loan For' + ' ' + loan_name,
                'narration': loan_name,
                'ref': reference,
                'journal_id': journal_id,
                'date': timenow,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.post()
        return True"""


class HrPayslipAcc(models.Model):
    _inherit = 'hr.payslip'

    # @api.multi
    def action_payslip_done(self):
        for line in self.input_line_ids:
            if line.loan_line_id:
                line.loan_line_id.action_paid_amount()
        return super(HrPayslipAcc, self).action_payslip_done()
