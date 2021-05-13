# See LICENSE file for full copyright and licensing details.

from odoo import api, fields,models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta,date
from odoo.tools.misc import formatLang, format_date, parse_date


class account_journal(models.Model):
    _inherit = "account.journal"

    # def action_open_reconcile(self):
    #     if self.type in ['bank', 'cash']:
    #         # Open reconciliation view for bank statements belonging to this journal
    #         lock_date = self.company_id._get_user_fiscal_lock_date() # defaults to date.min
    #         bank_stmt = self.env['account.bank.statement.line'].search([
    #             ('statement_id.journal_id', 'in', self.ids),
    #             ('is_reconciled', '=', False),
    #             ('date', '>', lock_date),
    #         ])
    #         # print(lock_date,bank_stmt,'*(*****************************')
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'bank_statement_reconciliation_view',
    #             'context': {'statement_line_ids': bank_stmt.ids, 'company_ids': self.mapped('company_id').ids},
    #         }
    #     else:
    #         # Open reconciliation view for customers/suppliers
    #         action_context = {'show_mode_selector': False, 'company_ids': self.mapped('company_id').ids}
    #         if self.type == 'sale':
    #             action_context.update({'mode': 'customers'})
    #         elif self.type == 'purchase':
    #             action_context.update({'mode': 'suppliers'})
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'manual_reconciliation_view',
    #             'context': action_context,
    #         }



class AccountReconciliation(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'


    @api.model
    def get_move_lines_for_bank_statement_line(self, st_line_id, partner_id=None, excluded_ids=None, search_str=False, offset=0, limit=None, mode=None,journal_id=None):
        """ Returns move lines for the bank statement reconciliation widget,
            formatted as a list of dicts

            :param st_line_id: ids of the statement lines
            :param partner_id: optional partner id to select only the moves
                line corresponding to the partner
            :param excluded_ids: optional move lines ids excluded from the
                result
            :param search_str: optional search (can be the amout, display_name,
                partner name, move line name)
            :param offset: offset of the search result (to display pager)
            :param limit: number of the result to search
            :param mode: 'rp' for receivable/payable or 'other'
        """
        statement_line = self.env['account.bank.statement.line'].browse(st_line_id)

        if search_str:
            domain = self._get_search_domain(search_str=search_str)
        else:
            domain = []

        partner_id = partner_id or statement_line.partner_id.id
        if partner_id:
            domain.append(('partner_id', '=', partner_id))

        if excluded_ids:
            domain.append(('id', 'not in', tuple(excluded_ids)))
        if journal_id:
            domain.append(('journal_id','=',journal_id))

        if mode == 'rp':
            # print('*********************************** RP')
            query, params = self._get_query_reconciliation_widget_customer_vendor_matching_lines(statement_line, domain=domain)
        else:
            # print('*********************************** other')
            query, params = self._get_query_reconciliation_widget_miscellaneous_matching_lines(statement_line, domain=domain)

        trailing_query, trailing_params = self._get_trailing_query(statement_line, limit=limit, offset=offset)

        self._cr.execute(query + trailing_query, params + trailing_params)
        move_lines = self.env['account.move.line'].browse(res['id'] for res in self._cr.dictfetchall())
        # print(move_lines,'*********************')

        js_vals_list = []
        for line in move_lines:
            js_vals_list.append(self._prepare_js_reconciliation_widget_move_line(statement_line, line))
        return js_vals_list

