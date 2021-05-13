from odoo import api, fields, models, SUPERUSER_ID, _

#product specification group that is related to product category
class ProductSpecificationGroup(models.Model):
    _name = 'product.specification.group'
    _description = 'product.specification.group'

    #name of the specification group
    name = fields.Char()
    #link to product category 
    product_group_1 = fields.Many2one('product.group.1')
    #link to specifications for this group
    specifications = fields.One2many('product.specification','specification_group')



#product specification that auto populates in specification lines on selection on specification group
class ProductSpecification(models.Model):
    _name = 'product.specification'
    _description = 'product.specification'

    #sequence of specification
    sequence = fields.Integer()
    #name of the specification
    name = fields.Char()
    #link to the parent specification group
    specification_group = fields.Many2one('product.specification.group')
    #links to the child values
    values = fields.One2many('product.specification.value','specification')


#specification value related to product specification
class ProductSpecificationValue(models.Model):
    _name = 'product.specification.value'
    _description = 'product.specification.value'

    #name of value
    name = fields.Char()
    #link to the parent specification
    specification = fields.Many2one('product.specification')



#product specification line items held in product.template
class ProductSpecificationLine(models.Model):
    _name = 'product.specification.line'
    _description = 'product.specification.line'

    #sequence of specification
    # sequence = fields.Integer()
    #product that this specification belongs to
    product = fields.Many2one('product.template')
    #current specification
    specification = fields.Many2one('product.specification')
    #user chooses value of that specification
    value = fields.Many2one('product.specification.value')



#holds product specification line items
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #specification group of selected product category
    specification_group = fields.Many2one('product.specification.group')
    #specification line items
    specification_lines = fields.One2many('product.specification.line','product')

    @api.onchange('product_group_1')
    def set_specification_group(self):
        try:
            print(self.product_group_1, self.product_group_1.id, type(self.specification_group), type(self.product_group_1))
            product_specification_rec = self.env['product.specification.group'].search([('product_group_1', '=', self.product_group_1.id)])
            print(product_specification_rec)
            self.specification_group = product_specification_rec.id if product_specification_rec else False
        except Exception as e:
            print("Updated the module")
            print(e)

    #setup specification lines on change of specification group
    @api.onchange('specification_group')
    def setup_specification_lines(self):
        
        #unlink and delete all existing specification lines
        for spec_line in self.specification_lines:
            self.specification_lines = [(2,spec_line.id)]

        #populate specification lines with new data
        if self.specification_group.id:
            categories = self.env['product.specification'].search([('specification_group','=',self.specification_group.id)],order="sequence")
            for categ in categories:
                self.specification_lines.create({
                    'product':self.id,
                    'specification':categ.id
                    })


    #concatinate specification and dimension values to the product name
    def specification_to_name(self):
        name_list = self.name.split(' : ')
        name_len = len(name_list)
        #depending on amount of info present in name
        if name_len == 3:
            self.name = name_list[0] + ' : ' + self.specification_group.name  + ' - '
            #find the line in which value has been entered
            for spec_line in self.specification_lines:
                if spec_line.value:
                    self.name +=   spec_line.value.name + ', '
            # Additional ` ` [space] was getting added at the nd of values bcz of the space so to remove the space.
            self.name = self.name.strip()
            # Additional `,` was getting added at the end of value so to remove the `,`.
            self.name = self.name[:-1]
            self.name += ' : ' + name_list[2]

        elif name_len == 2:
            self.name = name_list[0] + ' : ' + self.specification_group.name  + ' - '
            #find the line in which value has been entered
            for spec_line in self.specification_lines:
                if spec_line.value:
                    self.name +=   spec_line.value.name + ', '
            self.name = self.name.strip()
            self.name = self.name[:-1]
            self.name += ' : ' + name_list[1]
        
        elif name_len == 1:
            self.name = name_list[0] + ' : ' + self.specification_group.name + ' - '
            #find the line in which value has been entered
            for spec_line in self.specification_lines:
                if spec_line.value:
                    self.name +=  spec_line.value.name + ', '
            self.name = self.name.strip()
            self.name = self.name[:-1]
        else:
            self.name = ' : ' + self.specification_group.name + ' - '
            #find the line in which value has been entered
            for spec_line in self.specification_lines:
                if spec_line.value:
                    self.name +=   spec_line.value.name + ', '
            self.name = self.name.strip()
            self.name = self.name[:-1]

    # def name_get(self):
    #     res = super(ProductTemplate, self).name_get()
    #     data = []
    #     for product in self:
    #         name = product.name
    #         for line in product.specification_lines:
    #             if line.value in line:
    #                 name += ' '+line.value

    #         data.append((product.id,name))

    #     return data