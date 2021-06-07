# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MrpDistributeMoWiz(models.Model):
    _name = 'mrp.distribute.mo.wiz'
    _description = 'Mrp Distribute Mo Wiz'

    mo_id = fields.Many2one('mrp.production')
    quantity = fields.Float(related='mo_id.product_qty')
    distribute_mo_lines = fields.One2many('mrp.distribute.mo.wiz.line','distribute_mo')

    def distribute(self):
        for line in self.distribute_mo_lines:
            rec = self.mo_id.copy({
                'product_qty':line.quantity,
                'date_planned_start':line.scheduled_date,
                'user_id':line.responsible.id,
                'distribute_source_id':self.mo_id.id
            })
            rec._onchange_move_raw()
            rec._onchange_product_qty()
            self.mo_id.product_qty -= line.quantity
        self.mo_id._onchange_move_raw()
        self.mo_id._onchange_product_qty()

class MrpDistributeMoWizLine(models.Model):
    _name = 'mrp.distribute.mo.wiz.line'
    _description = 'Mrp Distribute Mo Wiz Line'

    distribute_mo = fields.Many2one('mrp.distribute.mo.wiz')
    quantity = fields.Float()
    scheduled_date = fields.Datetime()
    responsible = fields.Many2one('res.users')

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    distribute_source_id = fields.Many2one('mrp.production')
    distributions_ids = fields.One2many('mrp.production','distribute_source_id')
    distribution_count = fields.Integer(compute='_count_distro')

    @api.depends('distributions_ids')
    def _count_distro(self):
        for rec in self:
            rec.distribution_count = len(rec.distributions_ids)

    def action_view_mo_distributions(self):
        tree_view = self.env.ref('mrp.mrp_production_tree_view')
        view_id = self.env.ref('mrp.mrp_production_form_view')
        return {
            'name': _('Distributed MOs'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'mrp.production',
            'domain': [('distribute_source_id', '=', self.id)],
            'view_id': view_id.id,
            'views': [(tree_view.id, 'tree'),(view_id.id, 'form')],
            'type': 'ir.actions.act_window',
            'context': "{'create': False}"
            }

    def distribute(self):
        view_id = self.env.ref('manufacturing_distribution.mrp_distribute_mo_wiz_view_form')
        return {
            'name': _("{}({})".format(self.name,self.product_qty)),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.distribute.mo.wiz',
            'context':{'default_mo_id': self.id},
            'view_id': view_id.id,
            'views': [(view_id.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new'
            }