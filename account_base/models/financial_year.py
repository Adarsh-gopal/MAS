from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date

class FinancialYear(models.Model):
    _name = "financial.year"
    _description = "Financial Year"
    _order = 'name desc, id desc'

    name = fields.Char(string="Financial Year", required=True)
    date_from = fields.Date(string='Start Date', required=True,
        help='Start Date, included in the fiscal year.')
    date_to = fields.Date(string='End Date', required=True,
        help='Ending Date, included in the fiscal year.')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    new_financial_year = fields.Boolean(string="New Financial Year")
    closed = fields.Boolean(string="Closed")
    date_locked = fields.Boolean(string="Date Locked")


    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        '''
        Check interleaving between Financial years.
        There are 3 cases to consider:

        s1   s2   e1   e2
        (    [----)----]

        s2   s1   e2   e1
        [----(----]    )

        s1   s2   e2   e1
        (    [----]    )
        '''
        for fy in self:
            # Starting date must be prior to the ending date
            date_from = fy.date_from
            date_to = fy.date_to
            if date_to < date_from:
                raise ValidationError(_('The ending date must not be prior to the starting date.'))


            domain = [
                ('id', '!=', fy.id),
                '|', '|',
                '&', ('date_from', '<=', fy.date_from), ('date_to', '>=', fy.date_from),
                '&', ('date_from', '<=', fy.date_to), ('date_to', '>=', fy.date_to),
                '&', ('date_from', '<=', fy.date_from), ('date_to', '>=', fy.date_to),
            ]

            if self.search_count(domain) > 0:
                raise ValidationError(_('You can not have an overlap between two Financial years, please correct the start and/or end dates of your Financial years.'))

