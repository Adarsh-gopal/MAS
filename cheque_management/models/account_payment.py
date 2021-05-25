# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pdb

class AccountMove(models.Model):
    _inherit = "account.move"

    register_id = fields.Many2one('account.cheque.register', string='Cheque Register', copy=False)



class Respartner(models.Model):
    _inherit = "res.partner"

    cheque_payee_name = fields.Char( string='Cheque Payee Name', copy=False)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    lot_id = fields.Many2one('account.cheque.lot', string='Cheque Lot', copy=False, domain="[('active', '=', True), ('journal_id', '=', journal_id)]")
    cheque_payee_name = fields.Char( string='Cheque Payee Name', copy=False)

    @api.onchange('lot_id')
    def _onchange_cheque_lot_id(self):
        self.ensure_one()
        pdb.set_trace()
        if self.lot_id.next_number:
            self.check_number = self.lot_id.next_number

    @api.onchange('partner_id')
    def _onchange_cheque_lot_id(self):
        self.ensure_one()
        if self.partner_id:
            self.cheque_payee_name = self.partner_id.cheque_payee_name

    

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        AccountChequeRegister = self.env['account.cheque.register']
        for payment in self:
            payment.check_number = payment.lot_id.next_number
            if payment.partner_type == 'supplier' and payment.lot_id and payment.check_number:
                register = AccountChequeRegister.search([('journal_entry_no', '=', payment.move_id.name)], limit=1)
                if not register:
                    register = AccountChequeRegister.create({
                        'cheque_number': payment.check_number,
                        'payment_id': payment.id,
                        'journal_entry_no': payment.move_id.name,
                        'partner_id': payment.partner_id.id,
                        'amount': payment.amount,
                        'date': payment.date,
                    })
                #move = AccountMove.search([('name', '=', payment.move_name)], limit=1)
                payment.move_id.register_id = register.id
                payment.lot_id.write({'last_number': payment.check_number})
        return res


class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    payment_method_code = fields.Char(related='payment_method_id.code',
        help="Technical field used to adapt the interface to the payment type selected.", readonly=True)
    lot_id = fields.Many2one('account.cheque.lot', string='Cheque Lot', copy=False, domain="[('active', '=', True), ('journal_id', '=', journal_id)]")
    check_number = fields.Char(string="Check Number", copy=False,store=True,
        help="The selected journal is configured to print check numbers. If your pre-printed check paper already has numbers "
             "or if the current numbering is wrong, you can change it in the journal configuration page.")
    check_date = fields.Date()

    @api.onchange('lot_id')
    def _onchange_cheque_lot_id(self):
        self.ensure_one()
        if self.lot_id.next_number:
            self.check_number = int(self.lot_id.last_number) +1 



    def _create_payments(self):
        for each in self:
            res = super(PaymentRegister, each)._create_payments()
            if each.lot_id:
                res.update({'check_number': int(each.lot_id.last_number) +1, 'lot_id': each.lot_id.id})
                register = each.env['account.cheque.register'].create({
                                'cheque_number': str(int(each.lot_id.last_number) +1),
                                'payment_id': res.id,
                                'journal_entry_no': res.move_id.name,
                                'partner_id': res.partner_id.id,
                                'amount': res.amount,
                                'date': res.date,
                            })
            each.lot_id.last_number =str(int(each.lot_id.last_number) +1)
        return res
