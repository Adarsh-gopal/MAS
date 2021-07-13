# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    serial_no = fields.Integer(string='Sl No',compute="_compute_sl")

    @api.depends('order_id.order_line')
    def _compute_sl(self):
        var = 1
        for l in self:
            if l.serial_no == 0 and l.display_type not in ('line_section','line_note'):
                l.serial_no = var + l.serial_no
                var += 1
            else:
                l.serial_no = 0

# class SaleOrderLine(models.Model):
#     _inherit = 'purchase.order.line'

#     serial_no = fields.Integer(string='Sl No',compute="_compute_sl")

#     @api.depends('order_id.order_line')
#     def _compute_sl(self):
#         var = 1
#         for l in self:
#             if l.serial_no == 0 and l.display_type not in ('line_section','line_note'):
#                 l.serial_no = var + l.serial_no
#                 var += 1
#             else:
#                 l.serial_no = 0

