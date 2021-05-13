# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',help='analytic_account_automation_mrp')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',help='analytic_account_automation_mrp')
    analytic_company_type = fields.Selection(related='company_id.analytic_account_type')

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        data = super(MrpProduction, self)._get_move_raw_values(product_id, product_uom_qty, product_uom, operation_id, bom_line)

        data['analytic_account_id'] = self.analytic_account_id.id
        data['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]
        
        return data
    
    def _get_move_finished_values(self, product_id, product_uom_qty, product_uom, operation_id=False, byproduct_id=False):
        data = super(MrpProduction, self)._get_move_finished_values(product_id, product_uom_qty, product_uom, operation_id, byproduct_id)

        data['analytic_account_id'] = self.analytic_account_id.id
        data['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return data
    
    def action_confirm(self):
        self._check_company()
        for production in self:
            for raw_move in self.move_raw_ids:
                raw_move.analytic_account_id = production.analytic_account_id.id
                raw_move.analytic_tag_ids = [(6, 0, production.analytic_tag_ids.ids)]
            for finished_move in self.move_finished_ids:
                finished_move.analytic_account_id = production.analytic_account_id.id
                finished_move.analytic_tag_ids = [(6, 0, production.analytic_tag_ids.ids)]
        
        return super(MrpProduction, self).action_confirm()

    # def write(self, vals):
    #     res = super(MrpProduction, self).write(vals)

    #     if self.parent_picking_id:
    #         sub_con_picking = self.env['stock.picking'].search([('origin','=',self.parent_picking_id.name)])
    #         sub_con_picking.analytic_account_id = self.analytic_account_id.id
    #         return res