from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    z_close_sol = fields.Boolean(string = "Close",compute='boolean_close_sol',readonly=False)
    # z_close = fields.Boolean(string = "Clo", )

    @api.depends('z_close_sol')
    def boolean_close_sol(self):
        for line in self:
            if line.product_uom_qty == line.qty_delivered:
            	line.z_close_sol = True
