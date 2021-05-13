# -*- coding: utf-8 -*-

from odoo import models, fields, api


class journal_entry_domain_patch_14(models.Model):
    _inherit = 'account.move'

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = m.invoice_filter_type_domain
            alt_journals =  ('general','cash','bank')
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', '=?', journal_type)]
            if not journal_type:
                domain.pop()
                domain.append(('type', 'in', alt_journals))
            m.suitable_journal_ids = self.env['account.journal'].search(domain)