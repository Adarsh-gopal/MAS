
from odoo import api, fields, models


class Lead2OpportunityPartner(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection(selection_add=[('create', 'Create a new customer/contact')])