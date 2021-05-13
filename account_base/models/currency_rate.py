import logging
from datetime import date,datetime
from odoo import models, api, fields,_
from odoo.exceptions import UserError,Warning
from pytz import timezone
import pdb

from odoo.tools.float_utils import float_compare, float_is_zero, float_round
_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    is_currency_same = fields.Boolean("Invisible",store=True ,compute='find_currency_field')



    # Invisible BOE Rate
    @api.depends('currency_id')
    def find_currency_field(self):
        for l in self:
            if l.currency_id:
                if self.env.user.currency_id.id == l.currency_id.id:
                    l.is_currency_same = True
                else:
                    l.is_currency_same = False

    def view_currency_rate_tree(self):
        self.ensure_one()
        tree_view = self.env.ref('base.view_currency_rate_tree')
        view_id = self.env.ref('base.view_currency_rate_form')

        return {
            'name': _('Currency Rates'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'res.currency.rate',
            'domain': [('currency_id', '=', self.currency_id.id)],
            'context':{'default_currency_id': self.currency_id.id},
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }

    def action_post(self):
        for rec in self:
            if rec.move_type == 'entry':
                if rec.journal_id and rec.journal_id.ceiling_limit:
                    if sum(rec.line_ids.mapped('credit')) > rec.journal_id.ceiling_limit_value:
                        raise Warning(_('Amount should not exceed %s %s')%(rec.journal_id.ceiling_limit_value,rec.currency_id.symbol))
        return super(AccountMoveInherit,self).action_post()


class AccountPayment(models.Model):
    _inherit = "account.payment"

    is_currency_same = fields.Boolean("Invisible",store=True ,compute='find_currency_field')



    def action_post(self):
        for rec in self:
            if rec.payment_type == 'outbound':
                if rec.journal_id and rec.journal_id.ceiling_limit:
                    if rec.amount > rec.journal_id.ceiling_limit_value:
                        raise Warning(_('Amount should not exceed %s %s')%(rec.journal_id.ceiling_limit_value,rec.currency_id.symbol))

        return self.move_id.action_post()



    # Invisible BOE Rate
    @api.depends('currency_id')
    def find_currency_field(self):
        for l in self:
            if l.currency_id:
                if self.env.user.currency_id.id == l.currency_id.id:
                    l.is_currency_same = True
                else:
                    l.is_currency_same = False

    def view_currency_rate_tree(self):
        self.ensure_one()
        tree_view = self.env.ref('base.view_currency_rate_tree')
        view_id = self.env.ref('base.view_currency_rate_form')

        return {
            'name': _('Currency Rates'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'res.currency.rate',
            'domain': [('currency_id', '=', self.currency_id.id)],
            'context':{'default_currency_id': self.currency_id.id},
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }

   
   
class PurchaseorderInherit(models.Model):
    _inherit = "purchase.order"

    
    po_currency_id = fields.Many2one('res.currency',string='Company Currency', store=True ,default=lambda s: s.env.company.currency_id.id)
    is_currency_same =  fields.Boolean("Invisible",store=True ,compute='find_currency_pur')     
    

    # Invisible BOE Rate
    @api.depends('currency_id','po_currency_id')
    def find_currency_pur(self):
        for l in self:
            if l.po_currency_id and l.currency_id:
                if l.po_currency_id.id == l.currency_id.id:
                    l.is_currency_same = True
                else:
                    l.is_currency_same = False
    def view_currency_rate_tree(self):
        self.ensure_one()
        tree_view = self.env.ref('base.view_currency_rate_tree')
        view_id = self.env.ref('base.view_currency_rate_form')

        return {
            'name': _('Currency Rates'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'res.currency.rate',
            'domain': [('currency_id','=', self.currency_id.id)],
            'context':{'default_currency_id': self.currency_id.id},
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }



class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

   
    z_currency_id = fields.Many2one('res.currency',string='Currency', store=True,compute="get_currency")
    currency_id = fields.Many2one('res.currency',string='Company Currency', store=True ,default=lambda s: s.env.company.currency_id.id)
    is_currency_same = fields.Boolean(" Invisible",store=True ,compute='boe_invisible_curr')

    # get the currency from PO
    @api.depends('origin')
    def get_currency(self):
        for l in self:
            po_red_id = self.env['purchase.order'].search([('name','=',l.origin)])
            if po_red_id:
                l.z_currency_id = po_red_id.currency_id.id
            else :
                l.z_currency_id  = False
               

    # Invisible BOE Rate
    @api.depends('currency_id','z_currency_id')
    def boe_invisible_curr(self):
        for l in self:
            if l.z_currency_id and l.currency_id:
                if l.z_currency_id.id == l.currency_id.id:
                    l.is_currency_same = True
                else:
                    l.is_currency_same = False


    def view_currency_rate_tree(self):
        self.ensure_one()
        tree_view = self.env.ref('base.view_currency_rate_tree')
        view_id = self.env.ref('base.view_currency_rate_form')

        return {
            'name': _('Currency Rate'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'res.currency.rate',
            'domain': [('currency_id', '=', self.z_currency_id.id)],
            'context':{'default_currency_id': self.z_currency_id.id},
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',

            }







   

        

# class res_currency(models.Model):
#     _inherit = "res.currency"

#     inverse_rate = fields.Float(
#         'Current Inverse Rate', digits=(12, 4),
#         help='The rate of the currency from the currency of rate 1 (0 if no '
#                 'rate defined).'
#     )


#     @api.onchange('rate')
#     def get_inverse_rate(self):
#         self.inverse_rate = self.rate and (
#             1.0 / (self.rate))


#     rate = fields.Float(compute='_compute_current_rate', string='Current Rate', digits=(12, 12),
#                         help='The rate of the currency to the currency of rate 1.')


#     @api.depends('rate_ids.rate')
#     def _compute_current_rate(self):
#         for each_rate in self:
#             date = self._context.get('date') or fields.Datetime.now()
#             # company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
#             company_id = self._context.get('company_id')
#             # the subquery selects the last rate before 'date' for the given currency/company
#             query = """SELECT c.id, (SELECT r.rate FROM res_currency_rate r
#                                       WHERE r.currency_id = c.id AND r.name <= %s
#                                         AND (r.company_id IS NULL OR r.company_id = %s)
#                                    ORDER BY r.company_id, r.name DESC
#                                       LIMIT 1) AS rate
#                        FROM res_currency c
#                        WHERE c.id IN %s"""
#             self._cr.execute(query, (date, company_id, tuple(each_rate.ids)))
#             currency_rates = dict(self._cr.fetchall())
#             for currency in each_rate:
#                 currency.rate = currency_rates.get(currency.id) or 1.0

# class res_currency_rate(models.Model):
#     _inherit = "res.currency.rate"
#     rate = fields.Float(string='Current Rate', digits=(12, 12),)

#     inverse_rate = fields.Float(
#         'Inverse Rate', digits=(12, 4),
#         compute='get_inverse_rate',
#         inverse='set_inverse_rate',
#         help='The rate of the currency from the currency of rate 1',
#     )


#     @api.depends('rate')
#     def get_inverse_rate(self):
#         for l in self:
#             l.inverse_rate = l.rate and (1.0 / (l.rate))


#     def set_inverse_rate(self):
#         for k in self:
#             k.rate = k.inverse_rate and (1.0 / (k.inverse_rate))





# class StockImmediateTransfer(models.TransientModel):
#     _inherit = 'stock.immediate.transfer'
#     _description = 'Immediate Transfer'

   


#     def process(self):
#         pickings_to_do = self.env['stock.picking']
#         pickings_not_to_do = self.env['stock.picking']
#         for line in self.immediate_transfer_line_ids:
#             if line.to_immediate is True:
#                 pickings_to_do |= line.picking_id
#             else:
#                 pickings_not_to_do |= line.picking_id

#         for picking in pickings_to_do:
#             # If still in draft => confirm and assign
#             if picking.state == 'draft':
#                 picking.action_confirm()
#                 if picking.state != 'assigned':
#                     picking.action_assign()
#                     if picking.state != 'assigned':
#                         raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
#             for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
#                 # for move_line in move.move_line_ids:
#                 #     move_line.qty_done = move_line.product_uom_qty
#                 raise UserError(_("Please Enter the product Quantity ")) 

#         pickings_to_validate = self.env.context.get('button_validate_picking_ids')
#         if pickings_to_validate:
#             pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate)
#             pickings_to_validate = pickings_to_validate - pickings_not_to_do
#             return pickings_to_validate.with_context(skip_immediate=True).button_validate()
#         return True




    



 #    