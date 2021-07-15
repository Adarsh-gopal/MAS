# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo import tools
from datetime import datetime, timedelta


class SalesRegisterReport(models.Model):
    _name = "sales.register.report"
    _auto = False
    _description =  " "

    name = fields.Char('Invoice name')
    quantity = fields.Float('Quantity')
    price_unit = fields.Float('Price')
    price_subtotal = fields.Float('Subtotal')
    journal_id = fields.Many2one('account.journal', 'Journal Name')
    account_id = fields.Many2one('account.account','Account Name')
    partner_id = fields.Many2one('res.partner', 'Customer Name')
    currency_id = fields.Many2one('res.currency', string="Currency")
    tax_id = fields.Many2one('account.tax','Taxes')
    partner_address = fields.Char('Customer Address')
    igst_amount = fields.Float(compute="report_compute_tax", string="IGST amount")
    cgst_amount = fields.Float(compute="report_compute_tax", string="CGST amount")
    sgst_amount = fields.Float(compute="report_compute_tax", string="SGST amount")
    tcs_amount = fields.Float(compute="report_compute_tax", string="TCS amount")
    igst_percent = fields.Float(compute="report_compute_tax", string="IGST Percent")
    cgst_percent = fields.Float(compute="report_compute_tax", string="CGST Percent")
    sgst_percent = fields.Float(compute="report_compute_tax", string="SGST Percent")
    tcs_percent = fields.Float(compute="report_compute_tax", string="TCS Percent")
    total = fields.Float(compute="total_amount", string="Total")
    tax_amount = fields.Float(compute="total_tax", string="Total Tax")
    accounting_date = fields.Date('Accounting Date')


    # Computing the taxes
    def report_compute_tax(self):
        for record in self:
            tcs_percent = 0.0
            cgst_percent = 0.0
            sgst_percent = 0.0
            igst_percent = 0.0
            tcs_amount = 0.0
            sgst_amount = 0.0
            cgst_amount = 0.0
            igst_amount = 0.0
            if record.tax_id:
                
                if record.tax_id.amount_type == 'group':
                    grp_sgst = []
                    grp_cgst = []
                    grp_igst = []
                    grp_tcs = []
                    total_tax = 0.0
                    for child_tax in record.tax_id.children_tax_ids:
                       
                        if child_tax.tax_group_id.name == 'CGST':
                            grp_cgst.append(child_tax.amount)
                        elif child_tax.tax_group_id.name == 'SGST':
                            grp_sgst.append(child_tax.amount)
                        elif child_tax.tax_group_id.name == 'IGST':
                            grp_igst.append(child_tax.amount)
                        elif child_tax.tax_group_id.name == 'TCS':
                            grp_tcs.append(child_tax.amount)

                    tcs_percent = sum(grp_tcs)
                    cgst_percent = sum(grp_cgst)
                    sgst_percent = sum(grp_sgst)
                    igst_percent = sum(grp_igst)

                    cgst_amount = (( record.price_unit/ 100) * sum(grp_cgst)) * record.quantity
                    sgst_amount = (( record.price_unit/ 100) * sum(grp_sgst)) * record.quantity
                    igst_amount = (( record.price_unit/ 100) * sum(grp_igst)) * record.quantity

                    if grp_tcs != []:
                        total_percent = sum([cgst_amount, sgst_amount, igst_amount])
                        tcs_amount = (((record.price_unit * record.quantity) + total_percent)/100)* sum(grp_tcs)


                else:
                    if record.tax_id.tax_group_id.name == 'CGST':
                        cgst_amount = (record.price_unit / 100) * record.tax_id.amount 
                        cgst_percent = record.tax_id.amount    
                    elif record.tax_id.tax_group_id.name == 'SGST':
                        sgst_amount = (record.price_unit / 100) * record.tax_id.amount
                        sgst_percent = record.tax_id.amount
                    elif record.tax_id.tax_group_id.name == 'IGST':
                        igst_amount = (record.price_unit / 100) * record.tax_id.amount
                        igst_percent = record.tax_id.amount
                    elif record.tax_id.tax_group_id.name == 'TCS':
                        tcs_amount = (record.price_unit / 100) * record.tax_id.amount
                        tcs_percent = record.tax_id.amount

        
            record.tcs_percent = tcs_percent
            record.sgst_percent = sgst_percent
            record.cgst_percent = cgst_percent 
            record.igst_percent = igst_percent 
            record.tcs_amount = tcs_amount 
            record.sgst_amount = sgst_amount
            record.cgst_amount = cgst_amount
            record.igst_amount = igst_amount 

    # Total amount
    def total_amount(self):
        for itm in self:
            itm.total = sum([itm.price_subtotal,itm.tcs_amount,itm.sgst_amount,itm.cgst_amount,itm.igst_amount])

    # Total Tax
    def total_tax(self):
        for itm in self:
            itm.tax_amount = sum([itm.tcs_amount,itm.sgst_amount,itm.cgst_amount,itm.igst_amount])

 
    @api.model
    def init(self):
        tools.drop_view_if_exists(self._cr, 'sales_register_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW sales_register_report AS (
                SELECT 
                row_number() OVER () as id,
                move.move_type AS move_type,
                move.id AS move_id,
                line.name AS name,
                line.quantity AS quantity,
                line.price_unit AS price_unit,
                line.price_subtotal AS price_subtotal,
                line.journal_id AS journal_id,
                line.account_id AS account_id,
                line.partner_id AS partner_id,
                line.currency_id AS currency_id,
                line.date AS accounting_date,
                tax_rel.account_tax_id AS tax_id,
                acc_tax.tax_group_id  AS tax_group_id,
                partner.contact_address_complete AS partner_address
                FROM account_move move
                LEFT JOIN account_move_line line ON move.id = line.move_id
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN account_move_line_account_tax_rel tax_rel ON line.id  = tax_rel.account_move_line_id
                LEFT JOIN account_tax acc_tax ON acc_tax.id = tax_rel.account_tax_id
                where line.exclude_from_invoice_tab = 'f' AND (move_type = 'out_invoice' OR move_type = 'out_refund'))""")


    @api.model
    def sale_register_query(self,start_date,end_date):
    
        tools.drop_view_if_exists(self._cr, 'sales_register_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW sales_register_report AS (
                SELECT 
                row_number() OVER () as id,
                move.move_type AS move_type,
                move.id AS move_id,
                line.name AS name,
                line.quantity AS quantity,
                line.price_unit AS price_unit,
                line.price_subtotal AS price_subtotal,
                line.journal_id AS journal_id,
                line.account_id AS account_id,
                line.partner_id AS partner_id,
                line.currency_id AS currency_id,
                line.date AS accounting_date,
                tax_rel.account_tax_id AS tax_id,
                acc_tax.tax_group_id  AS tax_group_id,
                partner.contact_address_complete AS partner_address
                FROM account_move move
                LEFT JOIN account_move_line line ON move.id = line.move_id
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN account_move_line_account_tax_rel tax_rel ON line.id  = tax_rel.account_move_line_id
                LEFT JOIN account_tax acc_tax ON acc_tax.id = tax_rel.account_tax_id
                where line.exclude_from_invoice_tab = 'f' AND (move_type = 'out_invoice' OR move_type = 'out_refund'))""".format(start_date,end_date))
        
       
        return {
            'name': _("Sale Register Report List"),

            'type': 'ir.actions.act_window',

            'res_model': 'sales.register.report',

            'view_mode': 'tree,form',

            'view_type': 'form',

            'views': [[False, 'tree'],[False, 'form'],],

            'target': 'current',
        }
