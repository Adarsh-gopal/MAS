from odoo import models, fields, api,_

class CloseLoan(models.TransientModel):
    _name = 'close.loan'
    _description = 'CLose Loan'
    reason = fields.Many2one('loan.close', string="Reason",required=True)
    
    # @api.multi
    def send_mail(self):
        order = self.env['hr.loan'].search([('id','=',self._context.get('active_id'))])
        for var in order:
            var.write({'state': 'close'})
            var.employee_id.loan_balance = var.employee_id.loan_balance - var.loan_amount
            # order_2 = self.env['hr.employee'].search([])
            # for var2 in order_2:
            #     if var2.name == var.employee_id.name and var2.loan_id == var.id:
            #         var2.loan_balance = 0
        # return var.write({'state': 'close'})

class LoanClose(models.Model):
    _name = 'loan.close'
    _description = 'Loan Close'
    name = fields.Char('Name')
        
        