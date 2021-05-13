# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models,_
from odoo.tools import date_utils, groupby as groupbyelem
from operator import itemgetter
from odoo.exceptions import UserError, ValidationError


class report_jobwork_challan(models.AbstractModel):
    _inherit = 'report.maintenance_base.report_jobwork_challan'



    def _get_report_values(self, docids, data):
        docs = self.env['maintenance.request'].browse(docids)

        if len(set(docs.mapped('purchase_order'))) > 1:
            raise UserError(_('Please select Meterial request having same purchase order reference'))


        return super(report_jobwork_challan,self)._get_report_values(docids=docids,data=data)