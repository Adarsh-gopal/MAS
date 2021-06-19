# See LICENSE file for full copyright and licensing details.

from odoo import api, fields,models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta,date

class PurchaseAppproval(models.Model):
    _name = "purchase.approval"
    _description ="purchase.approval"


    document_type_id = fields.Many2one("purchase.doc.type","Document Type")
    name = fields.Char("Name")
    warehouse_id = fields.Many2one("stock.warehouse","Warehouse")
    approval_lines = fields.One2many("purchase.approval.line","approval_id")
    approval_method = fields.Selection(selection=[
            
            ('stages', 'Levels'),
            ('amount', 'Amount'),
            ],string='Approval Method',default='amount')

    @api.onchange('document_type_id')
    def _update_name(self):
        if self.document_type_id:
            self.name = self.document_type_id.name

    @api.constrains('document_type_id', 'warehouse_id')
    def _check_duplicate(self):
        existing_id=self.env['purchase.approval'].search([
                                            ('document_type_id','=',self.document_type_id.id),
                                            ("warehouse_id",'=',self.warehouse_id.id),
                                            ])
        if not len(existing_id) ==1:
            raise UserError (_("You Can't create the Purchase Approval from the same Warehouse and Document Type"))


class PurchaseAppprovalLine(models.Model):
    _name = "purchase.approval.line"
    _description ="purchase.approval.line"

    def _group_internal_users(self):
        group = self.env.ref('base.group_user', raise_if_not_found=False)
        return [('groups_id', 'in', group.ids)] if group else []


    user_ids = fields.Many2many("res.users",string="Users",domain=_group_internal_users)
    approval_id = fields.Many2one("purchase.approval",string="Appove")
    approval_amount = fields.Float("Amount(UP To)")
    approval_one= fields.Boolean("1")
    approval_two= fields.Boolean("2")
    approval_three= fields.Boolean("3")
    approval_all= fields.Boolean("Parallel")
    role = fields.Char("Role")


    @api.onchange('approval_all')
    def _update_approval_all(self):
        if self.approval_all:
            self.approval_one = False
            self.approval_two = False
            self.approval_three = False
    @api.onchange('approval_one')
    def _update_approval_one(self):
        if self.approval_one:
            self.approval_two = False
            self.approval_three = False
            self.approval_all = False

    @api.onchange('approval_two')
    def _update_approval_two(self):
        if self.approval_two:
            self.approval_one = False
            self.approval_three = False
            self.approval_all = False

    @api.onchange('approval_three')
    def _update_approval_three(self):
        if self.approval_three:
            self.approval_one = False
            self.approval_two = False
            self.approval_all = False

    




class PurchaseOrderApproval(models.Model):
    _name="purchase.order.approval"
    _description  = 'purchase.order.approval'

    approvals = fields.Selection(selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', 'All'),
            ('amount', 'Amount'),
            ],string='Approvals')
    is_approve = fields.Boolean("Approved")
    purchase_id = fields.Many2one('purchase.order')
    user_ids= fields.Many2many('res.users', string='Users')
    amount = fields.Float("Amount")
    approved_date = fields.Datetime("Approved Date")
    remarks = fields.Char("Remarks")
    role = fields.Char("Role")
    approval_method = fields.Selection(selection=[
            ('stages', 'Stages'),
            ('amount', 'Amount'),
            ],string='Approval Method')





class PurchaseOrder(models.Model):
  _inherit = 'purchase.order'


  purchase_approval_line = fields.One2many("purchase.order.approval",'purchase_id')
  approval_data = fields.Boolean("Data",compute ="get_data",store=True)
  current_approvall = fields.Integer("Current Approval",default=1)
  approval_method = fields.Char("Approval Method")


  @api.depends('picking_type_id','doc_type_id')
  def get_data(self):
    for each in self:
        if each.picking_type_id.id and each.approval_data == False:
            approval_ids = self.env['purchase.approval'].search([('warehouse_id','=',each.picking_type_id.warehouse_id.id),('document_type_id','=',each.doc_type_id.id)])

            for each_line in approval_ids.approval_lines:
                if approval_ids.approval_method == 'stages':
                    if each_line.approval_one:
                        value='1'
                    elif each_line.approval_two:
                        value='2'
                    elif each_line.approval_three:
                        value='3'
                    else:
                        value='4'
                else:
                    value = 'amount'

                valas={
                'approvals':value ,
                'user_ids': [(6, 0, each_line.user_ids.ids)],
                'amount':each_line.approval_amount,
                'role':each_line.role,
                'purchase_id':each.id,
                'approval_method':each_line.approval_id.approval_method,
                }
                self.env['purchase.order.approval'].create(valas)
                each.approval_method = approval_ids.approval_method

 
  def button_confirm(self):
        self.ensure_one()
        if self.approval_method == 'amount':
            all_approvals = [x.is_approve for x in self.purchase_approval_line]
            if True in all_approvals:
                return super(PurchaseOrder, self).button_confirm()
            else:
                raise UserError (_("Purchase Approval is not done! Please approve it"))
        elif self.approval_method == 'stages':
            all_approvals = [x.is_approve for x in self.purchase_approval_line]
            if False in all_approvals:
                raise UserError (_("Purchase Approval is not done! Please approve it"))
            else:
                return super(PurchaseOrder, self).button_confirm()

            

  def get_approval(self):
    approval_ids = self.env['purchase.approval'].search([
                            ('warehouse_id','=',self.picking_type_id.warehouse_id.id),
                            ('document_type_id','=',self.doc_type_id.id)])
    if approval_ids:
        curr_method = approval_ids.approval_method
        all_approvals = [x.approvals for x in self.purchase_approval_line]
        if curr_method == 'stages':
            current_appoval_line = self.purchase_approval_line.filtered(lambda line : int(line.approvals) == self.current_approvall)
            if current_appoval_line:
                if self.env.user.id in current_appoval_line.user_ids.ids :
                    current_appoval_line.is_approve = True
                    current_appoval_line.approved_date = datetime.now()
                    self.current_approvall +=1
                else:
                    raise UserError (_("Oops!!!! You can't approve the order "))
        
        elif curr_method == 'amount':
            new_ids = self.purchase_approval_line.filtered(lambda line : int(line.amount) >= self.amount_total)
            user_list =[]
            for each in new_ids:
                if self.env.user.id in each.user_ids.ids:
                    user_list.append(each)
            if user_list:
                user_list[0].is_approve = True
                user_list[0].approved_date = datetime.now()
            else:
                raise UserError (_("Oops!!!! You can't approve the order  "))

                

    else:
        raise UserError (_("Oops!!!! Create the purchase approval "))

   