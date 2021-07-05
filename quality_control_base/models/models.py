# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import pdb 

#Inspection Plan
class InspectionPlan(models.Model):
    _name = "inspection.plan"
    _inherit = ['mail.thread']
    _description = "Inspection Plan"

    name = fields.Char()
    team_id = fields.Many2one(
        'quality.alert.team', 'Team', check_company=True)
    product_id = fields.Many2one(
        'product.product',domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    product_tmpl_id = fields.Many2one(
        'product.template', check_company=True,
        domain="[('type', 'in', ['consu', 'product']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    picking_type_id = fields.Many2one('stock.picking.type', "Operation Type", check_company=True)

    quality_point_ids = fields.One2many('quality.point','inspection_plan_id', check_company=True)

    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        default=lambda self: self.env.company)

    @api.model
    def create(self,vals):
        sequence = self.env['stock.picking.type'].browse(vals.get('picking_type_id')).sequence_for_inspection_plan
        if sequence:
            vals['name'] = sequence.next_by_id()
        else:
            raise UserError(_("Please Enter The sequence for this operation Type"))
        return super(InspectionPlan,self).create(vals)

    start_date = fields.Date()
    end_date = fields.Date()

    @api.constrains('start_date','end_date')
    def _check_quantities(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_("""End Date Can not be less than Start Date"""))



# Quality Point
class QualityPoint(models.Model):
    _inherit = "quality.point"

    inspection_plan_id = fields.Many2one('inspection.plan', ondelete='cascade')
    team_id = fields.Many2one(
        'quality.alert.team', 'Team', check_company=True,
        default=False, required=False,
        compute='_compute_details',store=True)

    product_ids = fields.Many2many(
        'product.product', string='Products',
        compute='_compute_details',store=True)
    
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product', required=False, check_company=True,
        domain="[('type', 'in', ['consu', 'product']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        compute='_compute_details',store=True,readonly="False")
    picking_type_ids = fields.Many2many(
        'stock.picking.type', string='Operation Types', required=True, check_company=True,
        compute='_compute_details',store=True,readonly="False")
   
    company_id = fields.Many2one(
        'res.company', string='Company', required=False, index=True,default=False,
        compute='_compute_details',store=True)
    code = fields.Char(compute="_compute_details",store=True)

    @api.depends('inspection_plan_id','inspection_plan_id.team_id')
    def _compute_details(self):
        for rec in self:
            if rec.inspection_plan_id:
                if not rec.inspection_plan_id.product_id:
                    prod_id = self.env[('product.product')].search([('product_tmpl_id','=',rec.inspection_plan_id.product_tmpl_id.id)])
                else:
                    prod_id = rec.inspection_plan_id.product_id

                rec.product_ids = [(6,0,prod_id.ids)]
                # rec.product_tmpl_id = rec.inspection_plan_id.product_tmpl_id.id
                rec.picking_type_ids = rec.inspection_plan_id.picking_type_id
                rec.team_id = rec.inspection_plan_id.team_id.id
                rec.company_id = rec.inspection_plan_id.company_id.id
                rec.code = rec.picking_type_ids.code
            else:
                rec.picking_type_ids = rec.team_id = rec.code = False

    test_method_id = fields.Many2one('quality.test.method')

    characteristic = fields.Many2one('quality.characteristic')

    @api.onchange('characteristic')
    def _set_title(self):
        self.title = self.characteristic.description




#Inspection Sheet
class InspectionSheet(models.Model):
    _name = "inspection.sheet"
    _inherit = ['mail.thread']
    _description = "Inspection Sheet"

    name = fields.Char()
    
    source = fields.Char(compute='_get_source')
    product_id = fields.Many2one('product.product')
    picking_id = fields.Many2one('stock.picking')
    production_id = fields.Many2one('mrp.production')
    lot_id = fields.Many2one('stock.production.lot')
    team_id = fields.Many2one('quality.alert.team')
    company_id = fields.Many2one('res.company')


    @api.depends('picking_id','product_id')
    def _get_source(self):
        for rec in self:
            if rec.picking_id:
                rec.source = rec.picking_id.origin
            elif rec.production_id:
                rec.source = rec.production_id.name


    quality_check_ids = fields.One2many('quality.check','inspection_sheet_id')

    
    date = fields.Date(default=fields.Date.today())
    quantity_recieved = fields.Float(compute='_compute_details')
    quantity_accepted = fields.Float()
    quantity_rejected = fields.Float()
    quantity_destructive = fields.Float()
    under_deviation = fields.Float()

    @api.depends('picking_id','picking_id.move_ids_without_package','picking_id.move_line_ids_without_package.product_uom_qty')
    def _compute_details(self):
        for rec in self:
            if rec.picking_id:
                if rec.lot_id:
                    rec.quantity_recieved = rec.picking_id.move_line_ids_without_package.filtered(lambda line: line.product_id == rec.product_id and line.lot_id == rec.lot_id and not line.no_inspect).product_uom_qty
                else:
                    rec.quantity_recieved = rec.picking_id.move_ids_without_package.filtered(lambda line: line.product_id == rec.product_id).reserved_availability
            elif rec.production_id:
                rec.quantity_recieved = rec.production_id.product_qty

    status = fields.Selection([('open','Open'),
                            ('accept','Accept'),
                            ('reject','Reject'),
                            ('acceptud','Accepted Under Deviation')],default='open')
    state = fields.Selection([('open','Open'),
                            ('accept','Accepted'),
                            ('reject','Rejected')],default='open')

    def state_approve(self):
        if self.env.user.id in self.team_id.approver_ids.ids:
            current_sates=self.quality_check_ids.mapped('quality_state')
            if 'none' in current_sates:
                raise UserError(_("""OOPS!!!\nStill you need to do quality testing"""))
            else:
                self.state = 'accept'
        else:
            raise UserError(_("""OOPS!!!\nLooks like you aren't authorized to Approve"""))
        if self.quantity_accepted + self.quantity_rejected + self.quantity_destructive + self.under_deviation != self.quantity_recieved:
            raise ValidationError(_("""Sum of Quantities (Accepeted, Rejected, Destructive and Accepeted under Deviation) "MUST" be equal to Recieved Quantity"""))

        checks = self.env['quality.check'].search([('picking_id','=',self.picking_id.id),
                                                    ('production_id','=',self.production_id.id),
                                                    ('inspection_sheet_id','!=',False),
                                                    ('quality_state','=','none')])
        if not checks:
            for rec in self.env['quality.check'].search([('picking_id','=',self.picking_id.id),('production_id','=',self.production_id.id),('inspection_sheet_id','=',False)]):
                rec.unlink()



    def state_reject(self):
        if self.env.user.id in self.team_id.approver_ids.ids:
            current_sates=self.quality_check_ids.mapped('quality_state')
            if 'none' in current_sates:
                raise UserError(_("""OOPS!!!\nStill you need to do quality testing"""))
            else:
                self.state = 'reject'
        else:
            raise UserError(_("""OOPS!!!\nLooks like you aren't authorized to Reject"""))
        if self.quantity_accepted + self.quantity_rejected + self.quantity_destructive + self.under_deviation != self.quantity_recieved:
            raise ValidationError(_("""Sum of Quantities (Accepeted, Rejected, Destructive and Accepeted under Deviation) "MUST" be equal to Recieved Quantity"""))


    @api.model
    def create(self,vals):
        sequence = self.env['stock.picking'].browse(vals.get('picking_id')).picking_type_id.sequence_for_inspection_sheet or \
                    self.env['mrp.production'].browse(vals.get('production_id')).picking_type_id.sequence_for_inspection_sheet
        if sequence:
            vals['name'] = sequence.next_by_id()
        return super(InspectionSheet,self).create(vals)

    def process_quantities(self):
        if self.picking_id:
            line = {
                    'product_id':self.product_id.id,
                    'location_dest_id':self.picking_id.location_dest_id.id,
                    'product_uom_id':self.product_id.product_tmpl_id.uom_id.id,
                    'location_id':self.picking_id.location_id.id,
                    'lot_id':self.lot_id.id,
                    'no_inspect':True
                    }
            if self.quantity_accepted or self.under_deviation:
                line.update({'qty_done':self.quantity_accepted+self.under_deviation})
                self.picking_id.move_line_nosuggest_ids = [(0,0,line)]

            if self.quantity_rejected:
                line.update({'qty_done':self.quantity_rejected})
                self.picking_id.move_line_nosuggest_ids = [(0,0,line)]

            if self.quantity_destructive:
                current_move_id =self.env['stock.move'].search([('picking_id','=', self.picking_id.id),('product_id','=',self.product_id.id)])
                line.update({'qty_done':self.quantity_destructive})
                line.update({'location_dest_id':self.env['stock.location'].search([('destructive_location','=',True)]).id})
                current_move_id.location_dest_id =self.env['stock.location'].search([('destructive_location','=',True)]).id
                # line.move_id.update({'location_dest_id':self.env['stock.location'].search([('destructive_location','=',True)]).id})
                self.picking_id.move_line_nosuggest_ids = [(0,0,line)]
        
        self.processed = True

    processed = fields.Boolean()
    sampled_quantity = fields.Float()

    revised_sheet_ids = fields.One2many('inspection.sheet.revision','inspection_sheet_id')
    code = fields.Selection( related="picking_id.picking_type_code")

    def revise(self):

        ids = []
        for line in self.quality_check_ids:
            ids.append(self.env['quality.check.revision'].create({
                                'point_id':line.point_id.id,
                                'title':line.title,
                                'test_type':line.test_type,
                                'test_type_id':line.test_type_id.id,
                                'test_method_id':line.test_method_id.id,
                                'measure':line.measure,
                                'norm':line.norm,
                                'norm_unit':line.norm_unit,
                                'tolerance_min':line.tolerance_min,
                                'tolerance_max':line.tolerance_max,
                                'quality_state':line.quality_state,
                                }).id)

        revise_sheet = self.env['inspection.sheet.revision'].create({
                                'name':self.name,
                                'source':self.source,
                                'product_id':self.product_id.id,
                                'picking_id':self.picking_id.id,
                                'production_id':self.production_id.id,
                                'lot_id':self.lot_id.id,
                                'team_id':self.team_id.id,
                                'company_id':self.company_id.id,
                                'date':self.date,
                                'quantity_recieved':self.quantity_recieved,
                                'quantity_accepted':self.quantity_accepted,
                                'quantity_rejected':self.quantity_rejected,
                                'quantity_destructive':self.quantity_destructive,
                                'under_deviation':self.under_deviation,
                                'status':self.status,
                                'sampled_quantity':self.sampled_quantity,
                                'quality_check_ids':[(6,0,ids)],
                                })

        self.revised_sheet_ids = [(4,revise_sheet.id,0)]
        
        name = self.name.split('-')
        number = int(name[1]) if len(name)>1 else 0
        name = name[0]
        
        self.name = name+'-'+str(number+1)
        self.state = 'open'


#Desctructive Location
class StockLocation(models.Model):
    _inherit = 'stock.location'

    destructive_location = fields.Boolean('Is a Desctructive Location?')

    @api.onchange('destructive_location')
    def _check_one(self):
        if self.destructive_location == True:
            if len(self.env['stock.location'].search([('destructive_location','=',True)])):
                self.destructive_location = False
                raise ValidationError(_("""Can not have more than one destructive location"""))



# Quality Check
class QualityCheck(models.Model):
    _inherit = "quality.check"

    inspection_sheet_id = fields.Many2one('inspection.sheet',compute='_get_inspection_sheet', store=True)


    @api.depends('product_id','picking_id','lot_id','picking_id.state')
    def _get_inspection_sheet(self):
        for rec in self:

            if (rec.production_id or rec.picking_id.state == 'assigned','done','cancel') and (rec.product_id.tracking != 'lot' or rec.lot_id):
                search_params = [('product_id','=',rec.product_id.id),
                                ('team_id','=',rec.team_id.id,),
                                ('company_id','=',rec.company_id.id)]

                if rec.picking_id:
                    search_params.append(('picking_id','=',rec.picking_id.id))

                if rec.lot_id:
                    search_params.append(('lot_id','=',rec.lot_id.id))

                if rec.production_id:
                    search_params.append(('production_id','=',rec.production_id.id))

                sheet = self.env['inspection.sheet'].search(search_params,limit=1).id

                
                
                if not sheet:

                    create_params = {'product_id':rec.product_id.id,
                                    'team_id':rec.team_id.id,
                                    'company_id':rec.company_id.id}

                    if rec.picking_id:
                        create_params.update({'picking_id':rec.picking_id.id})

                    if rec.lot_id:
                        create_params.update({'lot_id':rec.lot_id.id})

                    if rec.production_id:
                        create_params.update({'production_id':rec.production_id.id})
                    
                    sheet = self.env['inspection.sheet'].create(create_params).id
                
                rec.inspection_sheet_id = sheet
            else:
                rec.inspection_sheet_id = False


    norm = fields.Float(related="point_id.norm")
    tolerance_min = fields.Float(related="point_id.tolerance_min")
    tolerance_max = fields.Float(related="point_id.tolerance_max")
    norm_unit = fields.Char(related="point_id.norm_unit")
    test_method_id = fields.Many2one('quality.test.method',related="point_id.test_method_id")


    quality_state = fields.Selection([
        ('none', 'To do'),
        ('pass', 'Passed'),
        ('fail', 'Failed')], string='Status', tracking=True,
        default='none', copy=False, store=True, compute='_set_state')

    confirm_measurement = fields.Boolean()

    @api.depends('test_type','measure','confirm_measurement')
    def _set_state(self):
        for rec in self:
            if rec.test_type == 'measure' and rec.confirm_measurement:
                # this condition for the negative values
                if not rec.tolerance_min >= 0.0 and not rec.tolerance_max > 0.0:
                    if rec.measure <= rec.tolerance_min and rec.measure >= rec.tolerance_max:
                         rec.quality_state = 'pass'
                    else:
                        rec.quality_state = 'fail'
                elif rec.measure >= rec.tolerance_min and rec.measure <= rec.tolerance_max:

                    rec.quality_state = 'pass'
                else:
                    rec.quality_state = 'fail'
            else:
                rec.quality_state = 'none'

    title = fields.Char(related="point_id.title")

    def confirm_measure_btn(self):
        
        if self.test_type == 'measure':
            self.confirm_measurement = True
        else:
            self.quality_state = 'pass'
    def fail_btn(self):
        self.quality_state = 'fail'



class QualityTestMethod(models.Model):
    _name = "quality.test.method"
    _description = "Quality Test Method"

    name = fields.Char(string="Test Method")


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    sequence_for_inspection_plan = fields.Many2one('ir.sequence')
    sequence_for_inspection_sheet = fields.Many2one('ir.sequence')

    code = fields.Selection(required=False)


#Quality Characteristics
class QualityCharacteristic(models.Model):
    _name = 'quality.characteristic'
    _description = 'QualityCharacteristic'

    name = fields.Char(compute='_generate_name')
    code = fields.Char()
    description = fields.Char()

    @api.depends('code','description')
    def _generate_name(self):
        for rec in self:
            rec.name = "%s %s"%(rec.code or '',rec.description or '')


class QualityAlertTeam(models.Model):
    _inherit = 'quality.alert.team'

    approver_id = fields.Many2one('res.users', 'Approver ')
    approver_ids = fields.Many2many('res.users', string='Approver')
    inspection_sheet_count = fields.Integer('# Inspection Sheet Alerts', compute='_compute_inspection_sheet_count')

    def _compute_inspection_sheet_count(self):
        sheet_data = self.env['inspection.sheet'].read_group([('team_id', 'in', self.ids), ('state', '=', 'open')], ['team_id'], ['team_id'])
        sheet_result = dict((data['team_id'][0], data['team_id_count']) for data in sheet_data)
        for team in self:
            team.inspection_sheet_count = sheet_result.get(team.id, 0)


# Quality with lots from Picking
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    inspection_sheet_id = fields.Many2one('inspection.sheet',compute='_get_inspection_sheet', store=True)
    no_inspect = fields.Boolean()

    @api.depends('product_id','picking_id','lot_id')
    def _get_inspection_sheet(self):
        for rec in self:

            if rec.picking_id:
                for check in self.env['quality.check'].search([('product_id','=',rec.product_id.id),('picking_id','=',rec.picking_id.id),('lot_id','=',False)]):
                    if rec.lot_id and not rec.no_inspect:
                        check.copy({'lot_id':rec.lot_id.id})
            
            elif rec.move_id.production_id:
                for check in self.env['quality.check'].search([('product_id','=',rec.product_id.id),('production_id','=',rec.move_id.production_id.id),('lot_id','=',False)]):
                    if rec.lot_id and not rec.no_inspect:
                        check.copy({'lot_id':rec.lot_id.id})



#Quality Check Revision
class QualityCheckRevision(models.Model):
    _name = "quality.check.revision"
    _description = "Quality Check Revision"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    inspection_sheet_id = fields.Many2one('inspection.sheet.revision')
    
    point_id = fields.Many2one('quality.point','Control Point')
    title = fields.Char(related="point_id.title")
    test_type = fields.Char("TTP")
    quality_state = fields.Selection([
        ('none', 'To do'),
        ('pass', 'Passed'),
        ('fail', 'Failed')], string='Status', tracking=True,
        default='none', copy=False, store=True, compute='_set_state')
    test_type_id = fields.Many2one('quality.point.test_type')
    test_method_id = fields.Many2one('quality.test.method',related="point_id.test_method_id")
    measure = fields.Float()
    norm = fields.Float(related="point_id.norm")
    norm_unit = fields.Char(related="point_id.norm_unit")
    tolerance_min = fields.Float(related="point_id.tolerance_min")
    tolerance_max = fields.Float(related="point_id.tolerance_max")

    
    @api.depends('test_type','measure')
    def _set_state(self):
        for rec in self:
            if rec.test_type == 'measure':
                if rec.measure >= rec.tolerance_min and rec.measure <= rec.tolerance_max:
                    rec.quality_state = 'pass'
                else:
                    rec.quality_state = 'fail'
            else:
                rec.quality_state = 'none'



#Inspection Sheet Revision
class InspectionSheetRevision(models.Model):
    _name = "inspection.sheet.revision"
    _inherit = ['mail.thread']
    _description = "Inspection Sheet Revision"

    inspection_sheet_id = fields.Many2one('inspection.sheet')

    name = fields.Char()
    
    date = fields.Date(default=fields.Date.today())
    company_id = fields.Many2one('res.company')
    team_id = fields.Many2one('quality.alert.team')
    source = fields.Char()
    picking_id = fields.Many2one('stock.picking')
    production_id = fields.Many2one('mrp.production')
    product_id = fields.Many2one('product.product')
    lot_id = fields.Many2one('stock.production.lot')
    
    status = fields.Selection([('open','Open'),
                            ('accept','Accept'),
                            ('reject','Reject'),
                            ('acceptud','Accepted Under Deviation')],default='open')
    quantity_recieved = fields.Float()
    sampled_quantity = fields.Float()
    quantity_accepted = fields.Float()
    quantity_rejected = fields.Float()
    quantity_destructive = fields.Float()
    under_deviation = fields.Float()
    quality_check_ids = fields.One2many('quality.check.revision','inspection_sheet_id')