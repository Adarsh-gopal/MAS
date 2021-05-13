from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total','order_line.product_id')
    def _amount_gross_charges(self):
        for order in self:
            gross = charges = 0.0
            for line in order.order_line:
                line._compute_amount()
                if line.product_id.type =='service':
                    charges += line.price_subtotal
                elif line.product_id.type in ('product','consu'):
                    gross += line.price_subtotal
            order.update({
                'gross_amount': order.currency_id.round(gross),
                'service_charges': order.currency_id.round(charges),
            })

    gross_amount = fields.Monetary(string='Gross Amount', store=True, tracking=True,compute='_amount_gross_charges')
    service_charges = fields.Monetary(string='Charges', store=True, tracking=True,compute='_amount_gross_charges')
