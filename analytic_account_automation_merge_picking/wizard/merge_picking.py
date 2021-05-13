# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError, Warning



class MergePicking(models.TransientModel):
    _inherit = "merge.picking"
    
    def validate_pickings(self,pickings,pick_type):
        res, pick_type = super(MergePicking, self).validate_pickings(pickings,pick_type)

        analytic_account = []
        analytic_tag = []
        for pick in pickings:
            analytic_account.append(pick.analytic_account_id)
            analytic_tag.append(pick.analytic_tag_ids)

            if not analytic_account[1:] == analytic_account[:-1]:
                raise Warning ('Merging is only allowed on Pickings of same analytic account')
            if not analytic_tag[1:] == analytic_tag[:-1]:
                raise Warning ('Merging is only allowed on Pickings of same analytic tag')

            res['analytic_account_id'] = pick.analytic_account_id.id
            res['analytic_tag_ids'] = pick.analytic_tag_ids.ids

        return res, pick_type


    def prepare_picking(self,vals):
        res = super(MergePicking, self).prepare_picking(vals)

        res['analytic_account_id'] = vals['analytic_account_id']
        res['analytic_tag_ids'] = [(6,0,vals['analytic_tag_ids'])]
        return res


    def prepare_move(self,move,new_pick):
        res = super(MergePicking, self).prepare_move(move,new_pick)

        res['analytic_account_id'] = move.analytic_account_id.id
        res['analytic_tag_ids'] = [(6,0,move.analytic_tag_ids.ids)]

        return res
