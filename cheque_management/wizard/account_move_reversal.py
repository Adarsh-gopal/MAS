# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pdb

class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    cheque_reason = fields.Many2one('cheque.reason', string='Cheque Cancellation Reason', ondelete='cascade', copy=False, help='Cheque Cancellation Reason')

    def reverse_moves(self):
        res = super(AccountMoveReversal, self).reverse_moves()
        if self.env.context['active_model'] =="account.move":
            moves = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id
            for move in moves:
                if move.register_id:
                    move.register_id.status = self.cheque_reason.name
            return res
        else:
            res


class ChequeReason(models.TransientModel):
    _name = 'cheque.reason'
    _description = 'Cheque Reason'

    name = fields.Char('Reason')
