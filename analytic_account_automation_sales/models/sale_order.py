# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_sales')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')

    # @api.onchange('analytic_account_id')
    # def _onchange_of_aa(self):
    #     for line in self.order_line:
    #         line.analytic_account_id = self.analytic_account_id.id

    # @api.onchange('analytic_tag_ids')
    # def _onchange_of_at(self):
    #     for line in self.order_line:
    #         line.analytic_tag_ids = [(6, 0, self.analytic_tag_ids.ids)]

    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()

        vals['analytic_account_id'] = self.analytic_account_id.id
        vals['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
        compute='_compute_analytic_id_and_tag_ids', readonly=False, store=True)
    analytic_tag_ids = fields.Many2many(compute='_compute_analytic_id_and_tag_ids', readonly=False, store=True)

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        res['analytic_account_id'] = self.analytic_account_id.id
        res['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return res
    
    @api.depends('order_id')
    def _compute_analytic_id_and_tag_ids(self):
        for rec in self:
            if rec.order_id.analytic_account_id and not rec.analytic_account_id:
                rec.analytic_account_id = rec.order_id.analytic_account_id.id
            if rec.order_id.analytic_tag_ids and not rec.analytic_tag_ids:
                rec.analytic_tag_ids = [(6, 0, rec.order_id.analytic_tag_ids.ids)]



class Picking(models.Model):
    _inherit = 'stock.picking'

    analytic_sale_id = fields.Integer(compute='set_analytic_acc',store=True)

    @api.depends('sale_id')
    def set_analytic_acc(self):
        for rec in self:
            if rec.sale_id:
                rec.analytic_sale_id = rec.sale_id.id
                rec.analytic_account_id = rec.sale_id.analytic_account_id.id
                rec.analytic_tag_ids = [(6, 0, rec.sale_id.analytic_tag_ids.ids)]
            else:
                rec.analytic_sale_id = False


class StockMove(models.Model):
    _inherit = 'stock.move'

    analytic_sale_line_id = fields.Integer(compute='set_analytic_acc',store=True)

    @api.depends('sale_line_id')
    def set_analytic_acc(self):
        for rec in self:
            if rec.sale_line_id:
                rec.analytic_sale_line_id = rec.sale_line_id.id
                rec.analytic_account_id = rec.sale_line_id.analytic_account_id.id
                rec.analytic_tag_ids = [(6, 0, rec.sale_line_id.analytic_tag_ids.ids)]
            else:
                rec.analytic_sale_line_id = False