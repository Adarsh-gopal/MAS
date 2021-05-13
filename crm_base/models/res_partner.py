# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_a_quothation_customer = fields.Boolean()

    # quation customer can be only one created on(09-07-2020)
    @api.onchange('is_a_quothation_customer')
    def on_change_is_a_quothation_customer(self):
        if self.is_a_quothation_customer:
            if True in self.env['res.partner'].search([]).mapped('is_a_quothation_customer'):
                raise ValidationError(("""You can only have one Quotation Customer"""))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.partner_id.is_a_quothation_customer:
            raise ValidationError(_("""Please select an actual customer to Confirm the quotation"""))
        return super(SaleOrder, self).action_confirm()

   # added the crm.lead model fields data to sale.order model  below to payment_term_id(09-07-2020)
    rel_company_name = fields.Char(string="Customer Name",related='opportunity_id.partner_name')
    rel_contact_name = fields.Char(string="Contact Name",related='opportunity_id.contact_name')
    lead_no = fields.Char(string="Lead No",compute='get_lead_no',store=True)


    @api.depends("opportunity_id")
    def get_lead_no(self):
        for each_lead in self:
            if each_lead.opportunity_id:
                each_lead.lead_no= each_lead.opportunity_id.sequence_name
            else:
                each_lead.lead_no =False

class SaleReport(models.Model):
    _inherit = "sale.report"

    lead_no = fields.Char(string="Lead No", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['lead_no'] = ",s.lead_no as lead_no"

        groupby += ', s.lead_no'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

