# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):

    	
    	var_ret = super(MrpProduction, self).button_mark_done()
    	list_err = []
    	new_work = []
    	for each_work in self.workorder_ids:
    		if each_work.state not in ['done','cancel']:
    			raise UserError(_('Please complete all the work orders before closing manufacturing order'))
    	return var_ret


    			

    	





    
        




    



    
        







        

    