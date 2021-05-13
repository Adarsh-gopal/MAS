from odoo import api, models, fields, _, exceptions
from datetime import datetime
import pdb



class ReportData(models.Model):
	_name='sales.summary.report'
	_description = "sales.summary.report"


	invoice_number_sale = fields.Char(string="Invoice No") 
	date=fields.Datetime(string="Invoice Date")
	analytic_account_id_sale = fields.Char("Analytical Account Id")
	customer_code_sale = fields.Char("Customer Code")
	customer_name_sale = fields.Char("Customer Name")
	gst_no_sale = fields.Char("GST No")
	customer_sate_sale = fields.Char("Customer State")
	customer_city_sale = fields.Char("Customer City")
	sales_team_sale = fields.Char("Sales Team")
	sales_person_sale = fields.Char("Sales Person")
	journal_sale = fields.Char("Journal")
	currency_sale = fields.Char("Currency")
	sale_order_no_sale = fields.Char("Sale Order No")
	sale_order_date_sale =fields.Datetime("Sales Order Date")
	# journal_sale = fields.Char("Journal")
	# terms_del_sale = fields.Char("Terms of Delivery")
	# freight_charges_sale =fields.Float("Freight Charges")
	product_cat_sale1= fields.Char("Product Group 1")
	product_cat_sale2 = fields.Char("Product Group 2")
	product_cat_sale3 = fields.Char("Product Groups 3")
	product_code_sale = fields.Char("Product Code")
	product_name_sale = fields.Char(string="Product Name")
	hsn_code_sale = fields.Char("HSN Code")
	uom_sale = fields.Char("Uom")
	unit_price_sale = fields.Float("Unit Price")
	qty_invoiced_sale = fields.Float("Qty Invoiced")
	amount_exc_sale = fields.Float("Amount Exclusive Tax")
	discount_per = fields.Float("Discount %")
	discount_amount = fields.Float("Discount Amount")
	cgst_rate_sale = fields.Float("CGST Rate %") 
	cgst_amount_sale = fields.Float("CGST Amount")
	sgst_rate_sale = fields.Float("SGST Rate %") 
	sgst_amount_sale = fields.Float("SGST Amount")
	igst_rate_sale = fields.Float("IGST Rate %") 
	igst_amount_sale = fields.Float("IGST Amount")
	tcs_rate_sale = fields.Float("TCS Rate %")
	tcs_amount_sale = fields.Float("TCS Amount")
	other_tax_name = fields.Char("Other tax")
	other_tax_rate = fields.Float("Tax Rate %")
	other_tax_amount = fields.Float("Tax Amount")
	# tax_one_sale = fields.Char("Tax 1")
	# tax_one_percent = fields.Float("Tax1 %")
	# tax_one_amount = fields.Float("Tax1 Amount")
	# tax_two_sale = fields.Char("Tax 2")
	# tax_two_percent = fields.Float("Tax2 %")
	# tax_two_amount = fields.Float("Tax2 Amount")	
	total_tax_sale = fields.Float("Total Tax Amount")
	amount_inclusive_sale = fields.Float("Amount Inclusive Tax")
	currency_name = fields.Char("Currency")
	payment_state_sale =fields.Char("Payment State")
	data_sent = fields.Boolean(default=False)
	sales_account_id = fields.Integer("sale_ref")




