from odoo import fields,models,api, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # z_po_order_date = fields.Datetime(related="order_id.date_order",string="Date Order")
    z_status = fields.Char('Document Status',store=True,compute='_compute_status_type')
    z_currency_id = fields.Many2one('res.currency',' Currency',related="order_id.currency_id")
    z_partner_id = fields.Many2one('res.partner',' Partner',related="order_id.partner_id")
    z_remaining_qty = fields.Float("Pending Qty",compute="qty_remaining",store=True)
    z_client_order_ref = fields.Char('Customer Reference',related="order_id.client_order_ref")
    z_pending_order_value = fields.Float(compute='compute_value',string='Pending Order Value',store=True)

    @api.depends('qty_delivered','product_uom_qty')
    def qty_remaining(self):
        for each in self:
            if each.product_uom_qty :
                each.z_remaining_qty = each.product_uom_qty- each.qty_delivered
            else:
                each.z_remaining_qty = 0.0

    @api.depends('z_remaining_qty','price_unit')
    def compute_value(self):
        for l in self:
            l.z_pending_order_value = l.price_unit * l.z_remaining_qty

    @api.depends('qty_delivered','qty_invoiced','product_uom_qty')
    def _compute_status_type(self):
    	for line in self:
            if line.qty_delivered != line.product_uom_qty:
                line.z_status = 'Pending Order'
            if line.qty_delivered != line.qty_invoiced:
                line.z_status = 'Pending for Invoice'
            if line.state == 'cancel':
                line.z_status = 'Cancel'
            if line.qty_delivered == line.product_uom_qty == line.qty_invoiced:
                line.z_status = "Fully Invoiced"



