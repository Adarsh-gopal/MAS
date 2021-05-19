# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # journal_type_name = fields.Selection(string="Journal Name",related='move_id.journal_id.type')
    # move_type_name = fields.Selection(related='move_id.move_type')
    # account_tax_name = fields.Char(related='tax_line_id.name')
    # cgst_rate = fields.Float(string="CGST %" ,compute='compute_tax_move_line')
    # cgst_amount = fields.Float(string="CGST Amount",compute='compute_tax_move_line')
    # sgst_rate = fields.Float(string="SGST %",compute='compute_tax_move_line')
    # sgst_amount = fields.Float(string="SGST Amount",compute='compute_tax_move_line')
    # igst_rate = fields.Float(string="IGST %",compute='compute_tax_move_line')
    # igst_amount = fields.Float(string="IGST Amount",compute='compute_tax_move_line')
    # tds_rate = fields.Float(string="TDS %",compute='compute_tax_move_line')
    # tds_amount = fields.Float(string="TDS Amount",compute='compute_tax_move_line')
    # tcs_rate = fields.Float(string="TCS %",compute='compute_tax_move_line')
    # tcs_amount = fields.Float(string="TCS Amount",compute='compute_tax_move_line')
    # rcm_rate = fields.Float(string="RCM Rate",compute='compute_tax_move_line')
    # rcm_amount = fields.Float(string="RCM Amount",compute='compute_tax_move_line') 
    # amount_inclusive_tax = fields.Float(string="Amount Inclusive Tax",compute='compute_tax_move_line')  



    # journal_type_name = fields.Selection(string="Journal Name",related='move_id.journal_id.type')
    # move_type_name = fields.Selection(related='move_id.move_type')
    # account_tax_name = fields.Char(related='tax_line_id.name')
    # partner_name = fields.Char(related='partner_id.name',string="Partner Tag")
    # partner_category_name = fields.Char(related='partner_id.category_id.name',string="Partner Category")
    # partner_state_name = fields.Char(related='partner_id.state_id.name',string="Partner State")
    # partner_country_name = fields.Char(related='partner_id.country_id.name',string="Partner Country")
    # product_category = fields.Char(string="Product Category",related='product_id.categ_id.name')
    # product_group_1= fields.Char(string="Product Group 1",related='product_id.product_group_1.name')
    # product_group_2 = fields.Char(string="Product Group 2",related='product_id.product_group_1.name')
    # product_group_3 = fields.Char(string="Product Group 3",related='product_id.product_group_1.name')
    # # hsn_code_name = fields.Char(string="HSN Code",related='product_id.l10n_in_hsn_code.name')
    # gst_name = fields.Char(related='partner_id.vat',string="Partner GST")
    # cgst_rate = fields.Float(string="CGST %" ,compute='compute_tax_move_line')
    # cgst_amount = fields.Float(string="CGST Amount",compute='compute_tax_move_line')
    # sgst_rate = fields.Float(string="SGST %",compute='compute_tax_move_line')
    # sgst_amount = fields.Float(string="SGST Amount",compute='compute_tax_move_line')
    # igst_rate = fields.Float(string="IGST %",compute='compute_tax_move_line')
    # igst_amount = fields.Float(string="IGST Amount",compute='compute_tax_move_line')
    tcs_rate = fields.Float(string="TCS %",compute='compute_tax_move_line')
    tcs_amount = fields.Float(string="TCS Amount",compute='compute_tax_move_line')
    invoice_date = fields.Date(related='move_id.invoice_date', store=True)
    hsn_code = fields.Char(related='product_id.l10n_in_hsn_code', store=True)
    # uom_id = fields.Many2one(related='product_id.uom_id', store=True)
    uqc = fields.Char(related='product_uom_id.l10n_in_code', store=True)
    # amount_inclusive_tax = fields.Float(string="Amount Inclusive Tax",compute='compute_tax_move_line')  


    @api.depends('price_subtotal','tax_ids')
    def compute_tax_move_line(self):
        self.cgst_rate = 0
        self.cgst_amount = 0
        self.sgst_rate = 0
        self.sgst_amount = 0
        self.igst_rate = 0
        self.igst_amount = 0

        self.tcs_rate = 0
        self.tcs_amount = 0
        self.tds_amount = 0
        self.tds_amount = 0
        self.amount_inclusive_tax = 0
        # self.hsn_code_name = False


        for line in self:
            if line.tax_ids:
                for each_line in line.tax_ids:
                    # for line in self:
                    if each_line.amount_type == "group":
                        for each_tcs in each_line.children_tax_ids:
                            
                            if each_tcs.tax_group_id.name == 'IGST':
                                line.igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                line.igst_amount  = (line.price_subtotal *line.igst_rate)/100
                            if each_tcs.tax_group_id.name == 'TDS':
                                line.tds_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                line.tds_amount = (line.price_subtotal *line.tds_rate)/100
                            if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                line.sgst_rate  = each_tcs.amount if each_tcs.amount else 0
                                line.sgst_amount = (line.price_subtotal *line.sgst_rate)/100
                                line.cgst_rate  = each_tcs.amount if each_tcs.amount else 0
                                line.cgst_amount = (line.price_subtotal *line.cgst_rate)/100
                            # if each_tcs.tax_group_id.name == 'TCS':
                            #     line.tcs_rate  = each_tcs.amount if each_tcs.amount else 0.0
                            #     line.tcs_amount  = (line.price_subtotal *line.tcs_rate)/100
                        # if each_line.tax_group_id.name == 'RCM':
                            
                        #     for rcm_per in each_line.children_tax_ids:
                        #         line.rcm_rate += abs(rcm_per.amount)/2 if rcm_per.amount else 0.0
                        #         line.rcm_amount += line.price_subtotal*line.rcm_rate/100


                    
                    elif each_line.amount_type == "percent":
                        for each_tcs in each_line:
                            
                            if each_tcs.tax_group_id.name == 'IGST':
                                line.igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                line.igst_amount  = (line.price_subtotal *line.igst_rate)/100
                            if each_tcs.tax_group_id.name == 'TDS':
                                line.tds_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                line.tds_amount  = (line.price_subtotal *line.tds_rate)/100
                            if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                line.sgst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                line.sgst_amount = (line.price_subtotal *line.sgst_rate)/100
                                line.cgst_rate  = each_tcs.amount if each_tcs.amount else 0
                                line.cgst_amount = (line.price_subtotal *line.cgst_rate)/100

            line.amount_inclusive_tax = line.price_subtotal + line.cgst_amount + line.sgst_amount + line.igst_amount+ line.tcs_amount 

            # sub_total_amount = line.price_subtotal
            # self.cgst_amount = line.price_subtotal / self.cgst_rate     

    # @api.depends('price_subtotal')
    # def compute_diff_tax(self):
    #     self.amount_inclusive_tax = 0
    #     for line in self:
    #         if line.cgst_rate:
    #             self.amount_inclusive_tax = line.price_subtotal/ line.cgst_rate
