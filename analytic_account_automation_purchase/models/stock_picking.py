# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    landed_cost_ids = fields.One2many('stock.landed.cost.lines','stock_picking_id')
    hide_landed_cost = fields.Boolean(compute="_compute_hiding")

    @api.depends('landed_cost_ids')
    def _compute_hiding(self):
        for rec in self:
            if rec.picking_type_id.code not in ('internal','incoming'):
                rec.hide_landed_cost = True
            else:
                rec.hide_landed_cost = False

    def button_validate(self):
        
        if not len(self.landed_cost_ids) and not self.hide_landed_cost:
            raise UserError(_('OOPS !!!\nLooks Like you have missed adding landed cost. Are you sure you want to continue?'))

        res = super(StockPicking, self).button_validate()

        self.env['stock.landed.cost'].create({
            'picking_ids':[(4, self.id)],
            'cost_lines':[(6, 0, self.landed_cost_ids.ids)]
            })

        return res