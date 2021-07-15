from odoo import models, fields, api, _


class SaleRegisterReportWizard(models.TransientModel):
    _name = "sale.register.wizard"
    _description = " "


    name  = fields.Char()
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')


    # Calling report method
    def retrieve_register(self):
        
        return self.env['sales.register.report'].sale_register_query(self.start_date, self.end_date)
        

    # Validation for start date and end date
    @api.onchange('start_date','end_date')
    def date_validation(self):
        if self.start_date and self.end_date:
            if not self.start_date < self.end_date:
                self.end_date = False
                return {'warning': {
            'title': _('User Warning'),
            'message': _('Selected End Date must be greater than Selected Start Date!')
        }}
