from odoo import fields, models,api,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import pdb
class Purchasetoleranceinventry(models.Model):
    _inherit='product.template'

    z_purchase_tolerance = fields.Float(string=' Purchase Tolerance',default=0.0)
    purchase_tol_reqd = fields.Boolean(string='Purchase Tolerance Required?',)


class Purchasetolerancevariants(models.Model):
    _inherit='product.product'

    zx_purchase_tolerance = fields.Float(string='Purchase Tolerance',default=0.0)

class Validatepurchasetolerance(models.Model):
    _inherit="stock.picking"



    @api.depends('move_line_ids_without_package','stock.move','stock.move.line')
    
    def _get_overprocessed_stock_moves(self):
        self.ensure_one()
        return self.move_lines.filtered(
            lambda move: move.product_uom_qty != 0 and float_compare(move.quantity_done, move.product_uom_qty,
                                                                     precision_rounding=move.product_uom.rounding) == 1
        )


    def button_validate(self):
        res = super(Validatepurchasetolerance, self).button_validate()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))
       
        # pdb.set_trace()
        if self.move_ids_without_package and self.picking_type_id.code=='incoming':
            for line in self.move_ids_without_package:
                if line.purchase_line_id:
                    if line.quantity_done > line.purchase_line_id.product_qty:
                            if line.product_id.purchase_tol_reqd == True:
                                if (line.quantity_done - line.purchase_line_id.product_qty) > line.product_id.z_purchase_tolerance:
                                    raise UserError(_('GR quantity is greater than PO quantity for {}. You can do {} {} of extra GR over the PO quantity.'.format(line.product_id.name,line.product_id.z_purchase_tolerance,line.product_id.uom_id.name)))
                       
        
        return res