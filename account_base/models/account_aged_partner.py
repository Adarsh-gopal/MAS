# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain



class AccountMove(models.Model):
    _inherit = 'account.move'

    mv_sales_person = fields.Char(related="invoice_user_id.name", store=True)

class ReportAdgedPartner(models.AbstractModel):
    _inherit = 'account.aged.partner'

    filter_salesperson = True
    filter_negative_val = False

    sales_person = fields.Char(group_operator='max')
    period5 = fields.Monetary(string='121 - 180')
    period6 = fields.Monetary(string='181 - 365')
    period7 = fields.Monetary(string='Older')

    @api.model
    def _get_query_period_table(self, options):
        ''' Compute the periods to handle in the report.
        E.g. Suppose date = '2019-01-09', the computed periods will be:

        Name                | Start         | Stop
        --------------------------------------------
        As of 2019-01-09    | 2019-01-09    |
        1 - 30              | 2018-12-10    | 2019-01-08
        31 - 60             | 2018-11-10    | 2018-12-09
        61 - 90             | 2018-10-11    | 2018-11-09
        91 - 120            | 2018-09-11    | 2018-10-10
        Older               |               | 2018-09-10

        Then, return the values as an sql floating table to use it directly in queries.

        :return: A floating sql query representing the report's periods.
        '''
        def minus_days(date_obj, days):
            return fields.Date.to_string(date_obj - relativedelta(days=days))

        date_str = options['date']['date_to']
        date = fields.Date.from_string(date_str)
        period_values = [
            (False,                  date_str),
            (minus_days(date, 1),    minus_days(date, 30)),
            (minus_days(date, 31),   minus_days(date, 60)),
            (minus_days(date, 61),   minus_days(date, 90)),
            (minus_days(date, 91),   minus_days(date, 120)),
            (minus_days(date, 121),   minus_days(date, 180)),
            (minus_days(date, 181),   minus_days(date, 365)),
            (minus_days(date, 366),  False),
        ]

        period_table = ('(VALUES %s) AS period_table(date_start, date_stop, period_index)' %
                        ','.join("(%s, %s, %s)" for i, period in enumerate(period_values)))
        params = list(chain.from_iterable(
            (period[0] or None, period[1] or None, i)
            for i, period in enumerate(period_values)
        ))
        return self.env.cr.mogrify(period_table, params).decode(self.env.cr.connection.encoding)



    # @api.model
    # def _get_sql(self):
    #     options = self.env.context['report_options']
    #     query = ("""
    #         SELECT
    #             {move_line_fields},
    #             account_move_line.partner_id AS partner_id,
    #             partner.name AS partner_name,
    #             move.mv_sales_person AS sales_person,
    #             COALESCE(trust_property.value_text, 'normal') AS partner_trust,
    #             COALESCE(account_move_line.currency_id, journal.currency_id) AS report_currency_id,
    #             account_move_line.payment_id AS payment_id,
    #             COALESCE(account_move_line.date_maturity, account_move_line.date) AS report_date,
    #             account_move_line.expected_pay_date AS expected_pay_date,
    #             move.move_type AS move_type,
    #             move.name AS move_name,
    #             journal.code AS journal_code,
    #             account.name AS account_name,
    #             account.code AS account_code,""" + ','.join([("""
    #             CASE WHEN period_table.period_index = {i}
    #             THEN %(sign)s * ROUND((
    #                 account_move_line.balance - COALESCE(SUM(part_debit.amount), 0) + COALESCE(SUM(part_credit.amount), 0)
    #             ) * currency_table.rate, currency_table.precision)
    #             ELSE 0 END AS period{i}""").format(i=i) for i in range(6)]) + """
    #         FROM account_move_line
    #         JOIN account_move move ON account_move_line.move_id = move.id
    #         JOIN account_journal journal ON journal.id = account_move_line.journal_id
    #         JOIN account_account account ON account.id = account_move_line.account_id

    #         JOIN res_partner partner ON partner.id = account_move_line.partner_id
        
    #         LEFT JOIN ir_property trust_property ON (
    #             trust_property.res_id = 'res.partner,'|| account_move_line.partner_id
    #             AND trust_property.name = 'trust'
    #             AND trust_property.company_id = account_move_line.company_id
    #         )
    #         JOIN {currency_table} ON currency_table.company_id = account_move_line.company_id
    #         LEFT JOIN LATERAL (
    #             SELECT part.amount, part.debit_move_id
    #             FROM account_partial_reconcile part
    #         ) part_debit ON part_debit.debit_move_id = account_move_line.id
    #         LEFT JOIN LATERAL (
    #             SELECT part.amount, part.credit_move_id
    #             FROM account_partial_reconcile part
    #         ) part_credit ON part_credit.credit_move_id = account_move_line.id
    #         JOIN {period_table} ON (
    #             period_table.date_start IS NULL
    #             OR COALESCE(account_move_line.date_maturity, account_move_line.date) <= DATE(period_table.date_start)
    #         )
    #         AND (
    #             period_table.date_stop IS NULL
    #             OR COALESCE(account_move_line.date_maturity, account_move_line.date) >= DATE(period_table.date_stop)
    #         )
    #         WHERE account.internal_type = %(account_type)s
    #         GROUP BY account_move_line.id, partner.id, trust_property.id, journal.id, move.id, account.id,
    #                  period_table.period_index, currency_table.rate, currency_table.precision
    #     """).format(
    #         move_line_fields=self._get_move_line_fields('account_move_line'),
    #         currency_table=self.env['res.currency']._get_query_currency_table(options),
    #         period_table=self._get_query_period_table(options),
    #     )
    #     params = {
    #         'account_type': options['filter_account_type'],
    #         'sign': 1 if options['filter_account_type'] == 'receivable' else -1,
    #     }
    #     return self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)


    def _get_sql(self):
        options = self.env.context['report_options']
        query = ("""
            WITH last_rates AS (
                SELECT DISTINCT ON(rate.currency_id, rate.company_id)
                    rate.currency_id, rate.company_id, rate.rate
                FROM res_currency_rate rate
                WHERE rate.name <= %(date)s AND rate.rate > 0
                ORDER BY rate.currency_id, rate.company_id, rate.name DESC
            )
            SELECT
                {move_line_fields},
                account_move_line.partner_id AS partner_id,
                partner.name AS partner_name,
                move.mv_sales_person AS sales_person,
                COALESCE(trust_property.value_text, 'normal') AS partner_trust,
                COALESCE(account_move_line.currency_id, journal.currency_id) AS report_currency_id,
                account_move_line.payment_id AS payment_id,
                COALESCE(account_move_line.date_maturity, account_move_line.date) AS report_date,
                account_move_line.expected_pay_date AS expected_pay_date,
                move.move_type AS move_type,
                move.name AS move_name,
                journal.code AS journal_code,
                account.name AS account_name,
                account.code AS account_code,""" + ','.join([("""
                CASE WHEN period_table.period_index = {i}
                THEN %(sign)s *
                    CASE WHEN (
                        account_move_line.company_currency_id != account_move_line.currency_id
                        AND (bool_and(part_debit.debit_currency_id = account_move_line.currency_id) OR COUNT(part_debit) = 0)
                        AND (bool_and(part_credit.credit_currency_id = account_move_line.currency_id) OR COUNT(part_credit) = 0)
                    )
                    THEN ROUND((
                        account_move_line.amount_currency - COALESCE(SUM(part_debit.debit_amount_currency), 0) + COALESCE(SUM(part_credit.credit_amount_currency), 0)
                    ) * COALESCE(company_currency.rate, 1) / COALESCE(used_currency.rate, 1), currency_table.precision)
                    ELSE ROUND((
                        account_move_line.balance - COALESCE(SUM(part_debit.amount), 0) + COALESCE(SUM(part_credit.amount), 0)
                    ) * currency_table.rate, currency_table.precision) END
                ELSE 0 END AS period{i}""").format(i=i) for i in range(8)]) + """
            FROM account_move_line
            JOIN account_move move ON account_move_line.move_id = move.id
            JOIN account_journal journal ON journal.id = account_move_line.journal_id
            JOIN account_account account ON account.id = account_move_line.account_id
            JOIN res_partner partner ON partner.id = account_move_line.partner_id
            LEFT JOIN ir_property trust_property ON (
                trust_property.res_id = 'res.partner,'|| account_move_line.partner_id
                AND trust_property.name = 'trust'
                AND trust_property.company_id = account_move_line.company_id
            )
            JOIN {currency_table} ON currency_table.company_id = account_move_line.company_id
            LEFT JOIN LATERAL (
                SELECT part.amount, part.debit_move_id, part.debit_amount_currency, part.debit_currency_id
                FROM account_partial_reconcile part
                WHERE part.max_date <= %(date)s
            ) part_debit ON part_debit.debit_move_id = account_move_line.id
            LEFT JOIN LATERAL (
                SELECT part.amount, part.credit_move_id, part.credit_amount_currency, part.credit_currency_id
                FROM account_partial_reconcile part
                WHERE part.max_date <= %(date)s
            ) part_credit ON part_credit.credit_move_id = account_move_line.id
            LEFT JOIN last_rates AS company_currency ON company_currency.currency_id = account_move_line.company_currency_id
                AND company_currency.company_id = account_move_line.company_id
            LEFT JOIN last_rates AS used_currency ON used_currency.currency_id = account_move_line.currency_id
                AND used_currency.company_id = account_move_line.company_id
            JOIN {period_table} ON (
                period_table.date_start IS NULL
                OR COALESCE(account_move_line.date_maturity, account_move_line.date) <= DATE(period_table.date_start)
            )
            AND (
                period_table.date_stop IS NULL
                OR COALESCE(account_move_line.date_maturity, account_move_line.date) >= DATE(period_table.date_stop)
            )
            WHERE account.internal_type = %(account_type)s
            GROUP BY account_move_line.id, partner.id, trust_property.id, journal.id, move.id, account.id,
                     period_table.period_index, currency_table.rate, currency_table.precision, company_currency.rate, used_currency.rate
            HAVING CASE WHEN (
                account_move_line.company_currency_id != account_move_line.currency_id
                AND (bool_and(part_debit.debit_currency_id = account_move_line.currency_id) OR COUNT(part_debit) = 0)
                AND (bool_and(part_credit.credit_currency_id = account_move_line.currency_id) OR COUNT(part_credit) = 0)
            )
            THEN ROUND(account_move_line.amount_currency - COALESCE(SUM(part_debit.debit_amount_currency), 0) + COALESCE(SUM(part_credit.credit_amount_currency), 0), currency_table.precision) != 0
            ELSE ROUND(account_move_line.balance - COALESCE(SUM(part_debit.amount), 0) + COALESCE(SUM(part_credit.amount), 0), currency_table.precision) != 0 END
        """).format(
            move_line_fields=self._get_move_line_fields('account_move_line'),
            currency_table=self.env['res.currency']._get_query_currency_table(options),
            period_table=self._get_query_period_table(options),
        )
        params = {
            'account_type': options['filter_account_type'],
            'sign': 1 if options['filter_account_type'] == 'receivable' else -1,
            'date': options['date']['date_to'],
        }
        return self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)

    ####################################################
    # COLUMNS/LINES
    ####################################################
    @api.model
    def _get_column_details(self, options):
        return [
            self._header_column(),
            self._field_column('sales_person'),
            self._field_column('report_date'),
            self._field_column('journal_code', name="Journal"),
            self._field_column('account_name', name="Account"),
            self._field_column('expected_pay_date'),
            self._field_column('period0', name=_("As of: %s") % format_date(self.env, options['date']['date_to'])),
            self._field_column('period1', sortable=True),
            self._field_column('period2', sortable=True),
            self._field_column('period3', sortable=True),
            self._field_column('period4', sortable=True),
            self._field_column('period5', sortable=True),
            self._field_column('period6', sortable=True),
            self._field_column('period7', sortable=True),
            self._custom_column(  # Avoid doing twice the sub-select in the view
                name=_('Total'),
                classes=['number'],
                formatter=self.format_value,
                getter=(lambda v: v['period0'] + v['period1'] + v['period2'] + v['period3'] + v['period4'] + v['period5']+ v['period6']+ v['period7']),
                sortable=True,
            ),
        ]


    def _show_line(self, report_dict, value_dict, current, options):
        # Don't display an aml report line with all zero amounts.
        # res =  super(ReportAdgedPartner,self)._show_line(report_dict, value_dict, current, options)
        # for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5','period6','period7']:
        #     print(value_dict[f],'********************************************') 
        all_zero = all(
            self.env.company.currency_id.is_zero(value_dict[f])
            for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5','period6','period7']
        )
        return (report_dict['parent_id'] is None
                or report_dict['parent_id'] == 'total-None'
                or (report_dict['parent_id'] in options.get('unfolded_lines', [])
                or options.get('unfold_all'))
                or not self._get_hierarchy_details(options)[len(current) - 2].foldable) and not all_zero



class ReportAccountAgedReceivable(models.Model):
    _inherit = "account.aged.receivable"

    filter_negative_val = False


    def _show_line(self, report_dict, value_dict, current, options):
        # Don't display an aml report line with all zero amounts.
        # print(report_dict['columns'][-1],'*************************************')
        if options.get('negative_val') == True:
            # if negative_val == True and 
            # negative_val = any(
            #     value_dict[f] < 0
            #     for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5']
            # )
            negative_val = True if report_dict['columns'][-1]['no_format'] < 0 and report_dict['unfoldable'] == True  and report_dict['unfolded'] != True else False
            return super()._show_line(report_dict, value_dict, current, options) and not negative_val
        else:
            return super()._show_line(report_dict, value_dict, current, options)
   

    # @api.model
    # def _get_options(self, previous_options=None):
    #     # OVERRIDE
    #     options = super(ReportAccountAgedReceivable, self)._get_options(previous_options=previous_options)
    #     options['filter_lessthan_zero'] = False
    #     options['filter_negative_val'] = False
    #     return options
class ReportAccountAgedPayable(models.Model):
    _inherit = "account.aged.payable"

    filter_negative_val = False

    def _show_line(self, report_dict, value_dict, current, options):
        # Don't display an aml report line with all zero amounts.
        # print(options.get('lessthan_zero'),'*************************')
        if options.get('negative_val') == True:
            # negative_val = any(
            #     value_dict[f] < 0
            #     for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5']
            # )
            negative_val = True if report_dict['columns'][-1]['no_format'] < 0 and report_dict['unfoldable'] == True and report_dict['unfolded'] != True  else False
            return super()._show_line(report_dict, value_dict, current, options) and not negative_val
        else:
            return super()._show_line(report_dict, value_dict, current, options)
   

    # @api.model
    # def _get_options(self, previous_options=None):
    #     # OVERRIDE
    #     options = super(ReportAccountAgedPayable, self)._get_options(previous_options=previous_options)
    #     options['filter_lessthan_zero'] = False
    #     options['filter_negative_val'] = False
    #     return options