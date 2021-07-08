# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    
    tcs_rate = fields.Float(string="TCS %",compute='compute_tcs_tax_move_line')
    tcs_amount = fields.Float(string="TCS Amount",compute='compute_tcs_tax_move_line')
    invoice_date = fields.Date(related='move_id.invoice_date', store=True)
    hsn_code = fields.Char(related='product_id.l10n_in_hsn_code', store=True)
    uqc = fields.Char(related='product_uom_id.l10n_in_code', store=True)
   

    @api.depends('price_subtotal','tax_ids')
    def compute_tcs_tax_move_line(self):
        self.cgst_rate = 0
        self.cgst_amount = 0
        self.sgst_rate = 0
        self.sgst_amount = 0
        self.igst_rate = 0
        self.igst_amount = 0

        self.tcs_rate = 0
        self.tcs_amount = 0
       
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
                            if each_tcs.tax_group_id.name == 'TCS':
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

            else:
                line.cgst_rate = 0
                line.cgst_amount = 0
                line.sgst_rate = 0
                line.sgst_amount = 0
                line.igst_rate = 0
                line.igst_amount = 0

                line.tds_rate = 0
                line.tds_amount = 0
                line.amount_inclusive_tax = 0
            line.amount_inclusive_tax = line.price_subtotal + line.cgst_amount + line.sgst_amount + line.igst_amount+ line.tcs_amount 

            # sub_total_amount = line.price_subtotal
            # self.cgst_amount = line.price_subtotal / self.cgst_rate     

    # @api.depends('price_subtotal')
    # def compute_diff_tax(self):
    #     self.amount_inclusive_tax = 0
    #     for line in self:
    #         if line.cgst_rate:
    #             self.amount_inclusive_tax = line.price_subtotal/ line.cgst_rate
