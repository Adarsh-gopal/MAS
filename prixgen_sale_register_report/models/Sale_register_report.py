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
    analytic_account_id = fields.Many2one('account.analytic.account','Analytic Account')
    account_user_type_id = fields.Many2one('account.account.type',"Account Type")
    account_group_type_id = fields.Many2one('account.group',"Account Group")
    invoice_id = fields.Many2one('account.move', 'Invoice Number')
    currency_id = fields.Many2one('res.currency', string="Currency")


    # Partner relate fields
    partner_id = fields.Many2one('res.partner', 'Customer Name')
    gst_treatment = fields.Selection([
        ('regular', 'Registered Business - Regular'),
        ('composition', 'Registered Business - Composition '),
        ('unregistered', 'Unregistered Business '),
        ('consumer', 'Consumer'),
        ('overseas', 'Overseas'),
        ('special_economic_zone', 'Special Economic Zone'),
        ('deemed_export', 'Deemed Export'),
        ],string="GST Treatment")
    partner_ref = fields.Char(string="Partner Reference")
    partner_category_id = fields.Many2one('partner.category',string="Partner Category")
    partner_state_id = fields.Many2one('res.country.state',string="Partner State")
    partner_country_id = fields.Many2one('res.country',string="Partner Country")
    # Product relate fields
    product_id = fields.Many2one('product.product', string="Product")
    product_category_id = fields.Char(string="Product Category",related='product_id.categ_id.name')
    item_group_id= fields.Many2one('item.group',string="Item Group")
    product_group_1_id= fields.Many2one('product.group.1',string="Product Group 1")
    product_group_2_id = fields.Many2one('product.group.2',string="Product Group 2")
    product_group_3_id = fields.Many2one('product.group.3',string="Product Group 3")
    product_ref = fields.Char(string="Product Reference")

    gst_name = fields.Char(string="Partner GST")
    tax_id = fields.Many2one('account.tax','Taxes')
    igst_amount = fields.Float(compute="report_compute_tax", string="IGST Amt" )
    cgst_amount = fields.Float(compute="report_compute_tax", string="CGST Amt")
    sgst_amount = fields.Float(compute="report_compute_tax", string="SGST Amt" )
    tcs_amount = fields.Float(compute="report_compute_tax", string="TCS Amt")
    igst_percent = fields.Float(compute="report_compute_tax", string="IGST %")
    cgst_percent = fields.Float(compute="report_compute_tax", string="CGST %")
    sgst_percent = fields.Float(compute="report_compute_tax", string="SGST %")
    tcs_percent = fields.Float(compute="report_compute_tax", string="TCS %")
    tax_amount = fields.Float(compute="total_tax", string="Tax Amt")
    total = fields.Float(compute="total_amount", string="Net Total")

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
                line.product_id AS product_id,
                line.quantity AS quantity,
                line.move_id AS invoice_id,
                line.price_unit AS price_unit,
                line.price_subtotal AS price_subtotal,
                line.journal_id AS journal_id,
                line.account_id AS account_id,
                line.analytic_account_id AS analytic_account_id,
                line.partner_id AS partner_id,
                line.currency_id AS currency_id,
                line.date AS accounting_date,
                tax_rel.account_tax_id AS tax_id,
                acc_tax.tax_group_id  AS tax_group_id,
                partner.vat AS gst_name,
                partner.ref AS partner_ref,
                partner.z_partner_category AS partner_category_id,
                partner.state_id AS partner_state_id,
                partner.country_id AS partner_country_id,
                partner.l10n_in_gst_treatment AS gst_treatment,
                account.user_type_id as account_user_type_id,
                account.group_id as account_group_type_id,
                product.item_group as item_group_id ,
                product.product_group_1 as product_group_1_id ,
                product.product_group_2 as product_group_2_id ,
                product.product_group_3 as product_group_3_id ,
                product.default_code as product_ref 
                FROM account_move move
                LEFT JOIN account_move_line line ON move.id = line.move_id
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN account_move_line_account_tax_rel tax_rel ON line.id  = tax_rel.account_move_line_id
                LEFT JOIN account_tax acc_tax ON acc_tax.id = tax_rel.account_tax_id
                where line.exclude_from_invoice_tab = 'f' AND line.product_id is Not null AND (move_type = 'out_invoice' OR move_type = 'out_refund'))""")


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
                line.product_id AS product_id,
                line.move_id AS invoice_id,
                line.quantity AS quantity,
                line.price_unit AS price_unit,
                line.price_subtotal AS price_subtotal,
                line.journal_id AS journal_id,
                line.account_id AS account_id,
                line.analytic_account_id AS analytic_account_id,
                line.partner_id AS partner_id,
                line.currency_id AS currency_id,
                line.date AS accounting_date,
                tax_rel.account_tax_id AS tax_id,
                acc_tax.tax_group_id  AS tax_group_id,
                partner.vat AS gst_name,
                partner.ref AS partner_ref,
                partner.z_partner_category AS partner_category_id,
                partner.state_id AS partner_state_id,
                partner.country_id AS partner_country_id,
                partner.l10n_in_gst_treatment AS gst_treatment,
                account.user_type_id as account_user_type_id,
                account.group_id as account_group_type_id,
                product.item_group as item_group_id ,
                product.product_group_1 as product_group_1_id ,
                product.product_group_2 as product_group_2_id ,
                product.product_group_3 as product_group_3_id ,
                product.default_code as product_ref 
                FROM account_move move
                LEFT JOIN account_move_line line ON move.id = line.move_id
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN account_move_line_account_tax_rel tax_rel ON line.id  = tax_rel.account_move_line_id
                LEFT JOIN account_tax acc_tax ON acc_tax.id = tax_rel.account_tax_id
                where line.exclude_from_invoice_tab = 'f' AND (move_type = 'out_invoice' OR move_type = 'out_refund') AND line.date >='{}' AND line.date <= '{}' ) """.format(start_date,end_date))
        
       
        return {
            'name': _("Sale Register Report List"),

            'type': 'ir.actions.act_window',

            'res_model': 'sales.register.report',

            'view_mode': 'tree,form',

            'view_type': 'form',

            'views': [[False, 'tree'],[False, 'form'],],

            'target': 'current',
        }
