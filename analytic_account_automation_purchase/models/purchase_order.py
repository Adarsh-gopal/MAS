# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_inventory')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_inventory')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')

    # @api.onchange('analytic_account_id')
    # def _onchange_of_aa(self):
    #     for line in self.order_line:
    #         line.account_analytic_id = self.analytic_account_id.id

    # @api.onchange('analytic_tag_ids')
    # def _onchange_of_at(self):
    #     for line in self.order_line:
    #         line.analytic_tag_ids = [(6, 0, self.analytic_tag_ids.ids)]


    @api.model
    def _prepare_picking(self):
        data = super(PurchaseOrder, self)._prepare_picking()

        data['analytic_account_id'] = self.analytic_account_id.id
        data['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return data


    def _prepare_invoice(self):
        invoice = super(PurchaseOrder, self)._prepare_invoice()
        invoice['analytic_account_id'] = self.analytic_account_id.id
        invoice['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return invoice



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_moves(self, picking):
        data = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)

        for rec in data:
            rec['analytic_account_id'] = self.account_analytic_id.id
            rec['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return data
    
    @api.depends('order_id')
    def _compute_analytic_id_and_tag_ids(self):
        for rec in self:
            if rec.order_id.analytic_account_id and not rec.account_analytic_id:
                rec.account_analytic_id = rec.order_id.analytic_account_id.id
            if rec.order_id.analytic_tag_ids and not rec.analytic_tag_ids:
                rec.analytic_tag_ids = [(6, 0, rec.order_id.analytic_tag_ids.ids)]