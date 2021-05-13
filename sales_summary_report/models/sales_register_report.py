# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api,_
from datetime import datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import logging
_logger = logging.getLogger(__name__)
import pdb
                        
class AccountMove(models.Model):
    _inherit = "account.move"

    def sale_summery(self):
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.product_id:
                    if rec.move_type == 'out_invoice' and rec.state == 'posted' and line.move_id.id == rec.id:
                        tot_sgst = tot_cgst = tot_gst = tot_amount = tot_cogs_amount = tot_with_tax_amount = tot_gp_amount = 0.0

                        sgst_rate= sgst_amount= cgst_rate= cgst_amount=igst_rate=igst_amount = other_tax_rate = other_tax_amount=0.0
                        tcs_rate = 0.0
                        other_tax_name = ''
                        sale_order_id = self.env['sale.order'].search([('name','=',rec.invoice_origin)],limit=1)
                        if line.product_id:                                                                        
                            ReportObj = self.env['sales.summary.report']

                            sale_id = self.env['sale.order'].search([('name','=',rec.invoice_origin)])

                            sale_order_date = None

                            if  rec.invoice_origin and sale_id:
                                sale_order_name = rec.invoice_origin
                                sale_order_date = sale_order_id.date_order
                            if rec.sto_id and not rec.invoice_origin:
                                sale_order_name = rec.sto_id.name
                                sale_order_date = rec.sto_id.dispatch_date
                            elif not rec.sto_id and not rec.invoice_origin:
                                sale_order_name = sale_order_id.name

                            for each_line in line.tax_ids:

                                if each_line.amount_type == "group":
                                    for each_tcs in each_line.children_tax_ids:
                                        
                                        if each_tcs.tax_group_id.name == 'IGST':
                                            igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                        if each_tcs.tax_group_id.name == 'TDS':
                                            tds_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                            sgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                            cgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        if each_tcs.tax_group_id.name == 'TCS':
                                            tcs_rate  = each_tcs.amount if each_tcs.amount else 0.0

                                    if each_line.tax_group_id.name not in ['GST','IGST']:
                                        
                                        for other_tax in each_line.children_tax_ids:
                                            other_tax_rate += abs(other_tax.amount)/2
                                            other_tax_amount += line.price_subtotal*other_tax.amount/100
                                            other_tax_name = each_line.tax_group_id.name


                                
                                elif each_line.amount_type == "percent":
                                    for each_tcs in each_line:
                                        
                                        if each_tcs.tax_group_id.name == 'IGST':
                                            igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                        if each_tcs.tax_group_id.name == 'TDS':
                                            tds_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                            sgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                            cgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        if each_tcs.tax_group_id.name == 'TCS':
                                            tcs_rate  = each_tcs.amount if each_tcs.amount else 0.0

                            sub_total_amount = line.price_subtotal
                            sgst_amount = round(sub_total_amount*sgst_rate/100,2)
                            cgst_amount = round(sub_total_amount*cgst_rate/100,2)
                            igst_amount = round((sub_total_amount if sub_total_amount else 0.0)*(igst_rate/100 if igst_rate >0.0 else 0.0),2)
                            
                            tcs_amount = round((sub_total_amount+sgst_amount+cgst_amount+igst_amount)*tcs_rate/100 if tcs_rate>0.0 else 0.0,2)
                            gst_total = round(sgst_amount+cgst_amount+igst_amount+tcs_amount+other_tax_amount,2)

                            total_with_tax_amount = round(sub_total_amount+gst_total,2)
                            path_ids=line.product_id.product_tmpl_id.categ_id.parent_path.split('/') if line.product_id else ''
           
                            cont_row = 0




                            # for path in path_ids:
                            #     if len(path):
                            #         if int(path) == 1 and cont_row == 0:
                            #             categ_ids = self.env['product.category'].search([('id','=',int(path))])
                            #             cate_name = categ_ids[0]
                            #             product_cat_sale1 = cate_name.name
                            #             cont_row += 1
                            #         if int(path) == 2 and cont_row == 1:
                            #             categ_ids = self.env['product.category'].search([('id','=',int(path))])
                            #             cate_name = categ_ids[0]
                            #             product_cat_sale2 = categ_ids.name
                            #             cont_row += 1

                            #         if int(path) == 3 and cont_row == 2:
                            #             categ_ids = self.env['product.category'].search([('id','=',int(path))])
                            #             cate_name = categ_ids[0]
                            #             product_cat_sale3 = categ_ids.name
                            #             cont_row += 1

                            vals_list = {
                                'invoice_number_sale': rec.name,
                                'date': rec.invoice_date,
                                'analytic_account_id_sale': line.analytic_account_id.name,
                                'customer_code_sale':rec.partner_id.ref,
                                'customer_name_sale':rec.partner_id.name,
                                'gst_no_sale':rec.partner_id.vat,
                                'customer_sate_sale':rec.partner_id.state_id.name,
                                'customer_city_sale':rec.partner_id.city,
                                'sales_team_sale':rec.team_id.name,
                                'sales_person_sale':rec.user_id.name,
                                'journal_sale':rec.journal_id.name,
                                'currency_sale':rec.currency_id.name,
                                'sale_order_no_sale':sale_order_name,
                                'sale_order_date_sale':sale_order_date,
                                # 'journal_sale':invoice.journal_id.name,
                                # 'terms_del_sale':0,
                                # 'amount_exc_sale':0,
                                'product_cat_sale1':line.product_id.product_group_1.name,
                                'product_cat_sale2':line.product_id.product_group_2.name,
                                'product_cat_sale3':line.product_id.product_group_3.name,
                                'product_code_sale':line.product_id.default_code,
                                'product_name_sale':line.product_id.name,
                                'hsn_code_sale':line.product_id.l10n_in_hsn_code ,
                                'uom_sale':line.product_uom_id.name,
                                'unit_price_sale':line.price_unit,
                                'qty_invoiced_sale':line.quantity,
                                'amount_exc_sale':sub_total_amount,

                                'cgst_rate_sale':cgst_rate,
                                'cgst_amount_sale':cgst_amount,
                                'sgst_rate_sale':sgst_rate,
                                'sgst_amount_sale':sgst_amount,
                                'igst_rate_sale':igst_rate,
                                'igst_amount_sale':igst_amount,
                                'tcs_rate_sale':tcs_rate,
                                'tcs_amount_sale':tcs_amount,
                                'other_tax_name':other_tax_name,
                                'other_tax_rate':other_tax_rate,
                                'other_tax_amount':other_tax_amount,
                                'total_tax_sale':gst_total,
                                'amount_inclusive_sale':total_with_tax_amount,
                                'currency_name':line.currency_id.name,
                                'payment_state_sale':rec.state,
                                'sales_account_id': rec.id,
                            }
                            new_id =ReportObj.create(vals_list)


    def action_post(self):
        res= super(AccountMove, self).action_post()
        for line in self.invoice_line_ids:
            if line.product_id:
                if self.move_type == 'out_invoice' and self.state == 'posted' and line.move_id.id == self.id:
                    tot_sgst = tot_cgst = tot_gst = tot_amount = tot_cogs_amount = tot_with_tax_amount = tot_gp_amount = 0.0

                    sgst_rate= sgst_amount= cgst_rate= cgst_amount=igst_rate=igst_amount = other_tax_rate = other_tax_amount=0.0
                    tcs_rate = 0.0
                    other_tax_name = ''
                    sale_order_id = self.env['sale.order'].search([('name','=',self.invoice_origin)],limit=1)
                    if line.product_id:                                                                        
                        ReportObj = self.env['sales.summary.report']

                        sale_id = self.env['sale.order'].search([('name','=',self.invoice_origin)])

                        sale_order_date = None

                        if  self.invoice_origin and sale_id:
                            sale_order_name = self.invoice_origin
                            sale_order_date = sale_order_id.date_order
                        if self.sto_id and not self.invoice_origin:
                            sale_order_name = self.sto_id.name
                            sale_order_date = self.sto_id.dispatch_date
                        elif not self.sto_id and not self.invoice_origin:
                            sale_order_name = sale_order_id.name

                        for each_line in line.tax_ids:

                            if each_line.amount_type == "group":
                                for each_tcs in each_line.children_tax_ids:
                                    
                                    if each_tcs.tax_group_id.name == 'IGST':
                                        igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                    if each_tcs.tax_group_id.name == 'TDS':
                                        tds_rate  = each_tcs.amount if each_tcs.amount else ' '
                                    if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                        sgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        cgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                    if each_tcs.tax_group_id.name == 'TCS':
                                        tcs_rate  = each_tcs.amount if each_tcs.amount else 0.0

                                if each_line.tax_group_id.name not in ['GST','IGST']:
                                    
                                    for other_tax in each_line.children_tax_ids:
                                        other_tax_rate += abs(other_tax.amount)/2
                                        other_tax_amount += line.price_subtotal*other_tax.amount/100
                                        other_tax_name = each_line.tax_group_id.name


                            
                            elif each_line.amount_type == "percent":
                                for each_tcs in each_line:
                                    
                                    if each_tcs.tax_group_id.name == 'IGST':
                                        igst_rate  = each_tcs.amount if each_tcs.amount else 0.0
                                    if each_tcs.tax_group_id.name == 'TDS':
                                        tds_rate  = each_tcs.amount if each_tcs.amount else ' '
                                    if each_tcs.tax_group_id.name == 'SGST' or each_tcs.tax_group_id.name == 'CGST':
                                        sgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                        cgst_rate  = each_tcs.amount if each_tcs.amount else ' '
                                    if each_tcs.tax_group_id.name == 'TCS':
                                        tcs_rate  = each_tcs.amount if each_tcs.amount else 0.0

                        sub_total_amount = line.price_subtotal
                        sgst_amount = round(sub_total_amount*sgst_rate/100,2)
                        cgst_amount = round(sub_total_amount*cgst_rate/100,2)
                        igst_amount = round((sub_total_amount if sub_total_amount else 0.0)*(igst_rate/100 if igst_rate >0.0 else 0.0),2)
                        
                        tcs_amount = round((sub_total_amount+sgst_amount+cgst_amount+igst_amount)*tcs_rate/100 if tcs_rate>0.0 else 0.0,2)
                        gst_total = round(sgst_amount+cgst_amount+igst_amount+tcs_amount+other_tax_amount,2)

                        total_with_tax_amount = round(sub_total_amount+gst_total,2)
                        path_ids=line.product_id.product_tmpl_id.categ_id.parent_path.split('/') if line.product_id else ''
       
                        cont_row = 0




                        vals_list = {
                            'invoice_number_sale': self.name,
                            'date': self.invoice_date,
                            'analytic_account_id_sale': line.analytic_account_id.name,
                            'customer_code_sale':self.partner_id.ref,
                            'customer_name_sale':self.partner_id.name,
                            'gst_no_sale':self.partner_id.vat,
                            'customer_sate_sale':self.partner_id.state_id.name,
                            'customer_city_sale':self.partner_id.city,
                            'sales_team_sale':self.team_id.name,
                            'sales_person_sale':self.user_id.name,
                            'journal_sale':self.journal_id.name,
                            'currency_sale':self.currency_id.name,
                            'sale_order_no_sale':sale_order_name,
                            'sale_order_date_sale':sale_order_date,
                            # 'journal_sale':invoice.journal_id.name,
                            # 'terms_del_sale':0,
                            # 'freight_charges_sale':0,
                            'product_cat_sale1':line.product_id.product_group_1.name,
                            'product_cat_sale2':line.product_id.product_group_2.name,
                            'product_cat_sale3':line.product_id.product_group_3.name,
                            'product_code_sale':line.product_id.default_code,
                            'product_name_sale':line.product_id.name,
                            'hsn_code_sale':line.product_id.l10n_in_hsn_code ,
                            'uom_sale':line.product_uom_id.name,
                            'unit_price_sale':line.price_unit,
                            'qty_invoiced_sale':line.quantity,
                            'discount_per':line.discount,
                            'discount_amount':(line.quantity* line.price_unit) -line.price_subtotal,
                            'amount_exc_sale':sub_total_amount,

                            'cgst_rate_sale':cgst_rate,
                            'cgst_amount_sale':cgst_amount,
                            'sgst_rate_sale':sgst_rate,
                            'sgst_amount_sale':sgst_amount,
                            'igst_rate_sale':igst_rate,
                            'igst_amount_sale':igst_amount,
                            'tcs_rate_sale':tcs_rate,
                            'tcs_amount_sale':tcs_amount,
                            'other_tax_name':other_tax_name,
                            'other_tax_rate':other_tax_rate,
                            'other_tax_amount':other_tax_amount,
                            'total_tax_sale':gst_total,
                            'amount_inclusive_sale':total_with_tax_amount,
                            'currency_name':line.currency_id.name,
                            'payment_state_sale':self.state,
                            'sales_account_id': self.id,
                        }
                        new_id =ReportObj.create(vals_list)     

        return res


    def button_draft(self):

        for account_move in self:
            account_id = account_move.id
            self.env.cr.execute("""DELETE FROM sales_summary_report where sales_account_id = %s ;"""% account_id)
        return super(AccountMove, self).button_draft()

