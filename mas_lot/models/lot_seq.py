from odoo import api, fields, models, _,exceptions
from datetime import date

from odoo.tools.float_utils import float_compare, float_is_zero, float_round

# class ProductionLot(models.Model):
#     _inherit = 'stock.production.lot'

#     @api.model
#     def create(self,vals):
#         x = self.env['ir.sequence'].next_by_code('stock.lot.serials') or '/'
#         vals['name'] = x
#         return super(ProductionLot,self).create(vals)

#     name = fields.Char(
#         'Lot/Serial Number',
#         required=True, help="Unique Lot/Serial Number",readonly=True)

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    receive_from = fields.Many2one('res.partner',string='Receive From')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_lot = fields.Boolean(store=True)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    custom_lot = fields.Boolean(store=True)



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.location_id.usage == 'supplier':
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
            for l in lines_to_check:
                if not l.product_id.custom_lot:
                    if not l.lot_name and not l.lot_id:
                        l.lot_id=self.env['stock.production.lot'].create({'name':"""{}/{}/{}/{}""".format(l.picking_id.partner_id.name[:4],l.picking_id.scheduled_date.date(),l.picking_id.name.split('/')[-1],self.env['ir.sequence'].next_by_code('stock.lot.serial')),
                        'product_id':l.product_id.id,'company_id':l.company_id.id}).id
        return super(StockPicking, self).button_validate()

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one('res.partner',string='Partner',store=True,compute='compute_partner')
    custom_lot = fields.Boolean(store=True)

    @api.depends('product_id')
    def compute_partner(self):
        for line in self:
            for l in line.picking_id:
                if line.product_id:
                    line.partner_id = l.partner_id.id
                    line.custom_lot = line.product_id.custom_lot
                else:
                    line.partner_id = False


    @api.onchange('qty_done')
    def _onchange_lot(self):
        for l in self:
            if l.picking_id.picking_type_id.code == 'incoming' and l.qty_done > 0:
                if l.product_id.custom_lot == False:
                    l.lot_id=self.env['stock.production.lot'].create({'name':"""{}/{}/{}/{}""".format(l.picking_id.partner_id.name[:4],l.picking_id.scheduled_date.date(),l.picking_id.name.split('/')[-1],self.env['ir.sequence'].next_by_code('stock.lot.serial')),
                            'product_id':l.product_id.id,'company_id':l.company_id.id}).id
                   
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    partner_id = fields.Many2one('res.partner',string='Partner',store=True,compute='compute_quant_partner')
    z_date = fields.Datetime(string='Date',store=True,compute='compute_quant_partner')

    @api.depends('lot_id')
    def compute_quant_partner(self):
    	for line in self:
    		if line.lot_id:
    			rec = self.env['stock.production.lot'].search([('id','=',line.lot_id.id)])
    			for l in rec:
    				if l.receive_from:
    					line.partner_id = l.receive_from
    					line.z_date = l.create_date
    				else:
    					line.partner_id = False
    					line.create_date = False
    		else:
    			line.partner_id = False
    			line.create_date = False

    