from odoo import api,models,fields


class UpdateAnalyticAccount(models.TransientModel):
	_name='update.journal'
	_description='update.journal'

	def update_journals(self):
		line = self._context.get('active_ids')

		self.env.cr.execute("""UPDATE account_move_line 
				set debit = 0.0, credit = 0.0,amount_currency =0.0,'balance' = 0.0  WHERE id IN %s""",(tuple(line),))



            
