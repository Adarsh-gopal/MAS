# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AlternativeGL(models.Model):
    _name = 'alternative.gl'
    _description = 'Alternative GL'

    doc_type_options = [
        ('out_invoice','Customer Invoice'),
        ('out_refund','Customer Credit Note'),
        ('in_invoice','Vendor Bill'),
        ('in_refund','Vendor Debit Note')]

    name = fields.Char()
    description = fields.Char()
    document_type = fields.Selection(doc_type_options)
    alt_id = fields.Integer(compute='_get_alt_id')

    gl_lines = fields.One2many('alternative.gl.line','gl_id')

    @api.depends('document_type')
    def _get_alt_id(self):
        for rec in self:
            if rec.document_type:
                rec.alt_id = 1 if rec.document_type in ('out_invoice', 'out_refund') else 2
            else:
                rec.alt_id = False


class AlternativeGLLine(models.Model):
    _name = 'alternative.gl.line'
    _description = 'Alternative GL Line'

    gl_id = fields.Many2one('alternative.gl')

    account_on_partner = fields.Many2one('account.account')
    account_to_use_instead = fields.Many2one('account.account')