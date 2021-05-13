# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import api, models, fields,tools, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError, ValidationError




class StockLandedCostLines(models.Model):
    _inherit = 'stock.landed.cost.lines'

    stock_picking_id = fields.Many2one('stock.picking')
    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost',required=False)
    value = fields.Char("Value")
    # to get the only landed cost true  by s
    product_id = fields.Many2one('product.product', 'Product', domain=[('landed_cost_ok', '=', True)])
    # to set the value by quantity overide the standerd by s


    ####### For manufacturing
    mrp_order_id = fields.Many2one('mrp.production')


    # @api.onchange('product_id')
    # def onchange_product_id_inherit(self):
    #     self.split_method = 'by_quantity'


class LandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    picking_ids = fields.Many2many(
        'stock.picking', string='Transfers',
        copy=False, states={'done': [('readonly', True)]},store=True)

    z_account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    def compute_landed_cost(self):
        AdjustementLines = self.env['stock.valuation.adjustment.lines']
        AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()

        digits = self.env['decimal.precision'].precision_get('Product Price')
        towrite_dict = {}
        for cost in self.filtered(lambda cost: cost._get_targeted_move_ids()):
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            for val_line_values in all_val_line_values:
                for cost_line in cost.cost_lines:
                    val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                    self.env['stock.valuation.adjustment.lines'].create(val_line_values)
                total_qty += val_line_values.get('quantity', 0.0)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += tools.float_round(former_cost, precision_digits=digits) if digits else former_cost

                total_line += 1

            for line in cost.cost_lines:
                value_split = 0.0
                for valuation in cost.valuation_adjustment_lines:
                    value = 0.0
                    if valuation.cost_line_id and valuation.cost_line_id.id == line.id:
                        if line.split_method == 'by_quantity' and total_qty:
                            per_unit = (line.price_unit / total_qty)
                            value = valuation.quantity * per_unit
                        elif line.split_method == 'by_weight' and total_weight:
                            per_unit = (line.price_unit / total_weight)
                            value = valuation.weight * per_unit
                        elif line.split_method == 'by_volume' and total_volume:
                            per_unit = (line.price_unit / total_volume)
                            value = valuation.volume * per_unit
                        elif line.split_method == 'equal':
                            value = (line.price_unit / total_line)
                        elif line.split_method == 'by_current_cost_price' and total_cost:
                            per_unit = (line.price_unit / total_cost)
                            value = valuation.former_cost * per_unit
                        else:
                            value = (line.price_unit / total_line)

                        if digits:
                            value = tools.float_round(value, precision_digits=digits, rounding_method='UP')
                            fnc = min if line.price_unit > 0 else max
                            value = fnc(value, line.price_unit - value_split)
                            value_split += value

                        if valuation.id not in towrite_dict:
                            towrite_dict[valuation.id] = value
                        else:
                            towrite_dict[valuation.id] += value
        for key, value in towrite_dict.items():
            AdjustementLines.browse(key).write({'additional_landed_cost': value,'analytic_account_id':self.z_account_analytic_id.id})
        return True



    # def button_validate(self):
    #     if any(cost.state != 'draft' for cost in self):
    #         raise UserError(_('Only draft landed costs can be validated'))
    #     if not all(cost.picking_ids for cost in self):
    #         raise UserError(_('Please define the transfers on which those additional costs should apply.'))
    #     cost_without_adjusment_lines = self.filtered(lambda c: not c.valuation_adjustment_lines)
    #     if cost_without_adjusment_lines:
    #         cost_without_adjusment_lines.compute_landed_cost()
    #     if not self._check_sum():
    #         raise UserError(_('Cost and adjustments lines do not match. You should maybe recompute the landed costs.'))

    #     for cost in self:
    #         move = self.env['account.move']
    #         move_vals = {
    #             'journal_id': cost.account_journal_id.id,
    #             'date': cost.date,
    #             'ref': cost.name,
    #             'analytic_account_id':cost.z_account_analytic_id.id,
    #             'line_ids': [],
    #             'move_type': 'entry',
    #         }
    #         valuation_layer_ids = []
    #         for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
    #             remaining_qty = sum(line.move_id.stock_valuation_layer_ids.mapped('remaining_qty'))
    #             linked_layer = line.move_id.stock_valuation_layer_ids[:1]

    #             # Prorate the value at what's still in stock
    #             cost_to_add = (remaining_qty / line.move_id.product_qty) * line.additional_landed_cost
    #             if not cost.company_id.currency_id.is_zero(cost_to_add):
    #                 valuation_layer = self.env['stock.valuation.layer'].create({
    #                     'value': cost_to_add,
    #                     'unit_cost': 0,
    #                     'quantity': 0,
    #                     'remaining_qty': 0,
    #                     'stock_valuation_layer_id': linked_layer.id,
    #                     'description': cost.name,
    #                     'stock_move_id': line.move_id.id,
    #                     'product_id': line.move_id.product_id.id,
    #                     'stock_landed_cost_id': cost.id,
    #                     'company_id': cost.company_id.id,
    #                 })
    #                 linked_layer.remaining_value += cost_to_add
    #                 valuation_layer_ids.append(valuation_layer.id)
    #             # Update the AVCO
    #             product = line.move_id.product_id
    #             if product.cost_method == 'average' and not float_is_zero(product.quantity_svl, precision_rounding=product.uom_id.rounding):
    #                 product.with_context(force_company=self.company_id.id).sudo().standard_price += cost_to_add / product.quantity_svl
    #             # `remaining_qty` is negative if the move is out and delivered proudcts that were not
    #             # in stock.
    #             qty_out = 0
    #             if line.move_id._is_in():
    #                 qty_out = line.move_id.product_qty - remaining_qty
    #             elif line.move_id._is_out():
    #                 qty_out = line.move_id.product_qty
    #             move_vals['line_ids'] += line._create_accounting_entries(move, qty_out)

    #         move_vals['stock_valuation_layer_ids'] = [(6, None, valuation_layer_ids)]
    #         move = move.create(move_vals)
    #         cost.write({'state': 'done', 'account_move_id': move.id})
    #         move.post()

    #         if cost.vendor_bill_id and cost.vendor_bill_id.state == 'posted' and cost.company_id.anglo_saxon_accounting:
    #             all_amls = cost.vendor_bill_id.line_ids | cost.account_move_id.line_ids
    #             for product in cost.cost_lines.product_id:
    #                 accounts = product.product_tmpl_id.get_product_accounts()
    #                 input_account = accounts['stock_input']
    #                 all_amls.filtered(lambda aml: aml.account_id == input_account and not aml.full_reconcile_id).reconcile()
    #     return True


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    allowed_picking_ids = fields.Many2many('stock.picking', compute='_compute_allowed_picking_ids')
    bool_field = fields.Boolean(default=False)
    @api.depends('company_id')
    def _compute_allowed_picking_ids(self):
        self.env.cr.execute("""SELECT sm.picking_id, sm.company_id
                                 FROM stock_move AS sm
                           INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                                WHERE sm.picking_id IS NOT NULL""")
        valued_picking_ids_per_company = defaultdict(list)
        for res in self.env.cr.fetchall():
            valued_picking_ids_per_company[res[1]].append(res[0])
        for cost in self:
            cost.allowed_picking_ids = valued_picking_ids_per_company[cost.company_id.id]
            if cost in cost.allowed_picking_ids:
                cost.hide_landed_cost = False
            else:
                cost.hide_landed_cost = True

    landed_cost_ids = fields.One2many('stock.landed.cost.lines','stock_picking_id')
    hide_landed_cost = fields.Boolean(default=True)
    required_landed_cost = fields.Boolean( "Apply Landed Cost" ,default=True)


    # def button_validate(self):

    #     if not len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost :
    #         raise UserError(_('OOPS !!!\nLooks Like you have missed adding landed cost. Are you sure you want to continue?'))

    #     res = super(StockPicking, self).button_validate()
    #     done_qty=0.0
    #     for each in self.move_ids_without_package:
    #         for each_line in each.move_line_ids:
    #             done_qty+= each_line.qty_done
    #     # print("done_qtydone_qtydone_qty",done_qty)

    #     if len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost and done_qty>0 :
    #         # print("13.0.0.213.0.0.2",self.landed_cost_ids.ids)

    #         self.env['stock.landed.cost'].create({
    #             'picking_ids':[(4, self.id)],
    #             'z_account_analytic_id':self.analytic_account_id.id,
    #             'cost_lines':[(6, 0, self.landed_cost_ids.ids)]
    #             })
        
    #     self._compute_allowed_picking_ids()

    #     return res


    def Validate_LC(self):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if not len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost :
            raise UserError(_('OOPS !!!\nLooks Like you have missed adding landed cost. Are you sure you want to continue?'))

        # res = (StockPicking, self).Validate_LC()
        done_qty=0.0
        for each in self.move_ids_without_package:
            for each_line in each.move_line_ids:
                done_qty+= each_line.qty_done
        # print("done_qtydone_qtydone_qty",done_qty)

        if len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost and done_qty>0 :
            # print("13.0.0.213.0.0.2",self.landed_cost_ids.ids)

            self.env['stock.landed.cost'].create({
                'picking_ids':[(4, self.id)],
                'z_account_analytic_id':self.analytic_account_id.id,
                'cost_lines':[(6, 0, self.landed_cost_ids.ids)]
                })

            self.bool_field = True

        # return res


    def view_landed_cost_tree(self):
        self.ensure_one()
        picking_ids=[]
        action = self.env.ref('stock_landed_costs.view_stock_landed_cost_tree').read()[0]
        for lines in self.landed_cost_ids:
            picking_ids = [(4, picking_ids.id, None) for picking_ids in lines.stock_picking_id]
        print("picking_idspicking_idspicking_ids",picking_ids)
        tree_view = self.env.ref('stock_landed_costs.view_stock_landed_cost_tree')
        view_id = self.env.ref('stock_landed_costs.view_stock_landed_cost_form')

        return {
            'name': _('Landed Cost'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'stock.landed.cost',
            'domain': [('picking_ids', 'in', self.ids)],
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }


class MrpProductionOrder(models.Model):
    _inherit = 'mrp.production'


    allowed_mrp_production_ids = fields.Many2many('mrp.production', compute='_compute_allowed_mrp_production_ids')
    bool_field = fields.Boolean(default=False)

    @api.depends('company_id')
    def _compute_allowed_mrp_production_ids(self):
        self.env.cr.execute("""SELECT sm.production_id, sm.company_id
                                 FROM stock_move AS sm
                           INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                                WHERE sm.production_id IS NOT NULL""")
        valued_picking_ids_per_company = defaultdict(list)
        for res in self.env.cr.fetchall():
            valued_picking_ids_per_company[res[1]].append(res[0])
        for cost in self:
            cost.allowed_mrp_production_ids = valued_picking_ids_per_company[cost.company_id.id]
            if cost in cost.allowed_mrp_production_ids:
                cost.hide_landed_cost = False
            else:
                cost.hide_landed_cost = True


    landed_cost_ids = fields.One2many('stock.landed.cost.lines','mrp_order_id')
    hide_landed_cost = fields.Boolean(default=True)
    required_landed_cost = fields.Boolean( "Apply Landed Cost" ,default=True)


    def button_mark_done(self):

        # if not len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost :
        #     raise UserError(_('OOPS !!!\nLooks Like you have missed adding landed cost. Are you sure you want to continue?'))

        res = super(MrpProductionOrder, self).button_mark_done()
        # # done_qty=0.0
        # for each in self.move_ids_without_package:
        #     for each_line in each.move_line_ids:
        #         done_qty+= each_line.qty_done
        # # print("done_qtydone_qtydone_qty",done_qty)

        # if len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost and done_qty>0 :
        #     # print("13.0.0.213.0.0.2",self.landed_cost_ids.ids)

        #     self.env['stock.landed.cost'].create({
        #         'picking_ids':[(4, self.id)],
        #         'z_account_analytic_id':self.analytic_account_id.id,
        #         'cost_lines':[(6, 0, self.landed_cost_ids.ids)]
        #         })
        
        self._compute_allowed_mrp_production_ids()

        return res


    def Validate_mrp_LC(self):
        if not len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost :
            raise UserError(_('OOPS !!!\nLooks Like you have missed adding landed cost. Are you sure you want to continue?'))

        # res = (StockPicking, self).Validate_LC()
        done_qty=0.0
        for each in self.move_raw_ids:
            for each_line in each.move_line_ids:
                done_qty+= each_line.qty_done
        # print("done_qtydone_qtydone_qty",done_qty)

        if len(self.landed_cost_ids) and not self.hide_landed_cost and self.required_landed_cost and done_qty>0 :
            # print("13.0.0.213.0.0.2",self.landed_cost_ids.ids)

            self.env['stock.landed.cost'].create({
                'mrp_production_ids':[(4, self.id)],
                'target_model':'manufacturing',
                # 'z_account_analytic_id':self.analytic_account_id.id,
                'cost_lines':[(6, 0, self.landed_cost_ids.ids)]
                })

            self.bool_field = True


    def view_landed_cost_tree(self):
        self.ensure_one()
        production_id=[]
        action = self.env.ref('stock_landed_costs.view_stock_landed_cost_tree').read()[0]
        for lines in self.landed_cost_ids:
            production_id = [(4, production_id.id, None) for production_id in lines.mrp_order_id]
        print("picking_idspicking_idspicking_ids",production_id)
        tree_view = self.env.ref('stock_landed_costs.view_stock_landed_cost_tree')
        view_id = self.env.ref('stock_landed_costs.view_stock_landed_cost_form')

        return {
            'name': _('Landed Cost'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'stock.landed.cost',
            'domain': [('mrp_production_ids', 'in', self.ids)],
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }




