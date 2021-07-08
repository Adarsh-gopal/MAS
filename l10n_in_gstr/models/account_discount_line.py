
from odoo import models


class L10nGSTRInAccountInvoiceReport(models.Model):
    _inherit = "l10n_in.account.invoice.report"



    # def _where(self):
    #     return """
    #             WHERE am.state = 'posted'
    #                 AND tag_rep_ln.account_tax_report_line_id in (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name in ('tax_report_line_igst','tax_report_line_cgst','tax_report_line_sgst','tax_report_line_zero_rated'))
    #                 AND (
    #                         parent_at.id is NULL
    #                         OR
    #                         parent_at.id in (
    #                           SELECT account_tax_id
    #                           FROM account_move_line_account_tax_rel aml_taxes
    #                           JOIN account_move_line aml2 on aml_taxes.account_move_line_id = aml2.id
    #                          WHERE aml2.move_id = aml.move_id
    #                            AND aml2.product_id = aml.product_id
    #                         )
    #                     )
    #     """

    def _where(self):
        where_str = super(L10nGSTRInAccountInvoiceReport, self)._where()
        where_str ="""  WHERE am.state = 'posted'
                    AND tag_rep_ln.account_tax_report_line_id in (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name in ('tax_report_line_igst','tax_report_line_cgst','tax_report_line_sgst','tax_report_line_zero_rated'))
                    AND (
                            parent_at.id is NULL
                            OR
                            parent_at.id in (
                              SELECT account_tax_id
                              FROM account_move_line_account_tax_rel aml_taxes
                              JOIN account_move_line aml2 on aml_taxes.account_move_line_id = aml2.id
                             WHERE aml2.move_id = aml.move_id
                               AND aml2.product_id = aml.product_id
                            )
                        )
            """
        return where_str
