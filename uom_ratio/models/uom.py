from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, ValidationError
import re


class UoMCategory(models.Model):
    _inherit = 'uom.category'

    length = fields.Float('Length')
    width = fields.Float('Width')


class UoM(models.Model):
    _inherit = 'uom.uom'

    length = fields.Float('Length')
    width = fields.Float('Width')
    thickness = fields.Float('Thickness')


    cat_width = fields.Float(related='category_id.width', string="Category Width")
    cat_length = fields.Float(related='category_id.length',string="Category length")


    @api.onchange('length','width','thickness')
    def _update_name(self):
        if self.length or self.width or self.thickness:
            self.name = re.sub(r'\([^)]*\)', '', self.name)+'('+str(self.length)+'X'+str(self.width)+'X'+str(self.thickness)+')'
        else:
            self.name = re.sub(r'\([^)]*\)', '', self.name or '') 


    @api.model_create_multi
    def create(self, vals_list):
        # res = super(UoM, self).create(vals_list)
        # self._update_ratio()
        for values in vals_list:
            if 'category_id' in values:
                category = self.env['uom.category'].browse(values.get('category_id'))
                if category.length != 0.0 and category.width != 0.0:
                    if values.get('length') != 0 and values.get('width') != 0 and values.get('thickness') != 0:
                        print(values.get('length'),values.get('width'),values.get('thickness'),)
                        values['factor'] = (values.get('length')/category.length)*(values.get('width')/category.width)*values.get('thickness')

            # if 'length' in values or 'width' in values or 'thickness' in values:
            #     values['name'] = values.get('name')+'('+str(values.get('length'))+'X'+str(values.get('width'))+'X'+str(values.get('thickness'))+')'
        return super(UoM, self).create(vals_list)

    def write(self, values):
        # res = super(UoM, self).write(values)
        # self._update_ratio()

        if 'length' in values or 'width' in values or 'thickness' in values:
            # values['name'] = re.sub(r'\([^)]*\)', '', values.get('name') or self.name)+'('+str(values.get('length') or self.length)+'X'+str(values.get('width') or self.width)+'X'+str(values.get('thickness') or self.thickness)+')'
            if self.category_id.width != 0.0 and self.category_id.length != 0.0:
                if  ('length' in values  and values.get('length') != 0) or ('width' in values and values.get('width') != 0) or ('thickness'in values and values.get('thickness') != 0): 
                    # print((values.get('length') or self.length),(values.get('width') or self.width),(values.get('thickness') or self.thickness),'looop in **************************')
                # if  ((values.get('length') or self.length )!= 0.0) and ((values.get('width') or self.width )!= 0.0) and ((values.get('thickness') or self.thickness) != 0.0):
                    values['factor'] = ((values.get('length') or self.length)/self.category_id.length)*((values.get('width') or self.width)/self.category_id.width)*(values.get('thickness') or self.thickness)
                else:
                    values['factor'] = 1

        return super(UoM, self).write(values)


