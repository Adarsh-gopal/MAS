# -*- coding: utf-8 -*-

from odoo import fields, models, api,_,tools
from operator import itemgetter
from odoo.tools import date_utils, groupby as groupbyelem

class SalesAnalysisReport(models.Model):
    _name = 'sales.analysis.report'
    _auto = False
    _description =  " "

    name = fields.Char('Name',related='category_id.name')
    product_id = fields.Many2one('product.product', string="Product")
    category_id = fields.Many2one('product.category',string='Product Category')
    sales_person = fields.Many2one('res.users',string='Sales Person')
    team_id = fields.Many2one('crm.team',string='Sales Team')
    jan = fields.Float('January')
    feb = fields.Float('February')
    march = fields.Float('March')
    april = fields.Float('April')
    may = fields.Float('May')
    june = fields.Float('June')
    july = fields.Float('July')
    august = fields.Float('August')
    sept = fields.Float('Sepember')
    october = fields.Float('October')
    november = fields.Float('November')
    december = fields.Float('December')
    company_id = fields.Many2one('res.company')



    @api.model
    def init(self):
        company = self.env.company.id
        tools.drop_view_if_exists(self._cr, 'sales_analysis_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW sales_analysis_report AS (
                SELECT 
                row_number() OVER () as id,
                line.product_category AS category_id,
                line.product_id AS product_id,
                move.invoice_user_id AS sales_person,
                move.team_id AS team_id,
                {company}  AS company_id,
                line.name AS name,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 1
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS jan,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 2
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS feb,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 3
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS march,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 4
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS april,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 5
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS may,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 6
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS june,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 7
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS july,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 8
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS august,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 9
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS sept,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 10
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS october,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 11
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS november,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 12
                    THEN line.price_unit
                ELSE 0.0 END 
                    AS december
                FROM account_move_line line
                LEFT JOIN account_move move ON line.move_id = move.id 
                where line.exclude_from_invoice_tab = 'f' AND (move_type = 'out_invoice' OR move_type = 'out_refund') AND line.company_id = {company})""".format(company=company))


    @api.model
    def sale_analysis_report_query(self,start_date,end_date,based_on,analyse_by):
        company = self.env.company.id
        if analyse_by == 'pc':
            context ={'search_default_group_by_product_category': 1,'col_by':'pc'}
        if analyse_by == 'sp':
            context ={'search_default_group_by_sales_person': 1,'col_by':'sp'}
        if analyse_by == 'st':
            context ={'search_default_group_by_team_id': 1,'col_by':'st'}
        if analyse_by == 'prod':
            context ={'search_default_group_by_product_id': 1,'col_by':'prod'}
    
        tools.drop_view_if_exists(self._cr, 'sales_analysis_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW sales_analysis_report AS (
                SELECT 
                row_number() OVER () as id,
                line.product_category AS category_id,
                line.product_id AS product_id,
                move.invoice_user_id AS sales_person,
                move.team_id AS team_id,
                line.name AS name,
                {company}  AS company_id,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 1
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS jan,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 2
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS feb,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 3
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS march,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 4
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS april,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 5
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS may,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 6
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS june,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 7
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS july,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 8
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS august,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 9
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS sept,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 10
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS october,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 11
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS november,
                CASE WHEN EXTRACT(MONTH FROM line.date) = 12
                    THEN line.{based_on}
                ELSE 0.0 END 
                    AS december
                FROM account_move_line line
                LEFT JOIN account_move move ON line.move_id = move.id             
                where line.exclude_from_invoice_tab = 'f' AND (move_type = 'out_invoice' OR move_type = 'out_refund') AND line.company_id ={company} AND line.date >= '{sd}' AND line.date <= '{ed}')""".format(company=company,based_on=based_on,sd=(start_date),ed=(end_date)))
        
       
        return {
            'name': _("Sale Analysis Report"),
            'type': 'ir.actions.act_window',
            'res_model': 'sales.analysis.report',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context':context,
            'views': [[False, 'tree'],[False, 'form'],],
            'target': 'current',
        }


class SaleAnalisysWiz(models.TransientModel):
    _name = 'sale.analysis.wiz'
    _description = 'Inventory Summary Wizard'

    financial_year = fields.Many2one('financial.year')
    based_on = fields.Selection([('price_subtotal', 'Sub Total'),('price_total','Total')],string="Based On",default="price_subtotal")
    analyse_by = fields.Selection([('pc','Product Category'),('prod','Product'),('st','Sales Team'),('sp','Sales Person')], string="Analyse By",default="pc")

    def action_open_report(self):
        if self.financial_year:
            start_date = self.financial_year.date_from
            end_date = self.financial_year.date_to
        return self.env['sales.analysis.report'].sale_analysis_report_query(start_date, end_date,self.based_on,self.analyse_by)

