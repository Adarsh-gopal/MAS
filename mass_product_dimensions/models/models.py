from odoo import api, fields, models, SUPERUSER_ID, _

class ProductDimension(models.Model):
    _name = 'product.dimension'
    _description = 'product.dimension'

    product_varient_id = fields.Many2one('product.product')
    product_template_id = fields.Many2one('product.template')

    typee = fields.Selection([
        ('frame','Frame'),
        ('shutter', 'Shutter'),
        ('door', 'Door'),
        ('others', 'Others')],string='Type')

    lengthx = fields.Float()
    lengthx_UOM = fields.Many2one('uom.uom')
    
    width = fields.Float()
    width_UOM = fields.Many2one('uom.uom')
    
    thickness = fields.Float()
    thickness_UOM = fields.Many2one('uom.uom')
    
    height = fields.Float()
    height_UOM = fields.Many2one('uom.uom')
    
    diameter = fields.Float()
    diameter_UOM = fields.Many2one('uom.uom')
    
    description = fields.Char()
    
    face_description = fields.Char()
    back_description = fields.Char()
    edge_banding = fields.Char()




class ProductTemplate(models.Model):
    _inherit = 'product.template'

    material_group = fields.Selection([
                    ('door', 'Door'),
                    ('frame', 'Frame'),
                    ('doorframe','Door Frame'),
                    ('furniture', 'Furniture'),
                    ('others', 'Others')])

    product_dimension_ids = fields.One2many('product.dimension','product_template_id')

    @api.onchange('material_group')
    def prepare_dimension_lines(self):
        for dimension in self.product_dimension_ids:
            self.product_dimension_ids = [(2,dimension.id)]

        if self.material_group == 'door':
            self.product_dimension_ids.create({'typee':'door','product_template_id':self.id})

        if self.material_group == 'frame':
            self.product_dimension_ids.create({'typee':'frame','product_template_id':self.id})
        
        if self.material_group == 'doorframe':
            self.product_dimension_ids.create({'typee':'shutter','product_template_id':self.id})
            self.product_dimension_ids.create({'typee':'frame','product_template_id':self.id})

        if self.material_group == 'furniture' or self.material_group == 'others':
            self.product_dimension_ids.create({'typee':'others','product_template_id':self.id})

    #concatinate dimension values to product name
    def dimension_to_name(self):
        #add dimensions to name that have been entered
        name_list = self.name.split(' : ')
        name_len = len(name_list)
        if name_len > 1:
            self.name = name_list[0] + ' : ' + name_list[1] + ' : '
        elif name_len == 1:
            self.name = name_list[0] + ' : '
        else:
            self.name = ' : '
        if self.material_group:
            if self.material_group != 'doorframe':
                self.name += '( '
                if self.product_dimension_ids.lengthx != 0.0:
                    if self.product_dimension_ids.lengthx:
                        self.name += str(self.product_dimension_ids.lengthx) + str(self.product_dimension_ids.lengthx_UOM.name)
                    if self.product_dimension_ids.width:
                        self.name += ' x '+str(self.product_dimension_ids.width) + str(self.product_dimension_ids.width_UOM.name)
                    if self.product_dimension_ids.thickness:
                        self.name += ' x '+str(self.product_dimension_ids.thickness) + str(self.product_dimension_ids.thickness_UOM.name)
                    if self.product_dimension_ids.height:
                        self.name += ' x '+str(self.product_dimension_ids.height) + str(self.product_dimension_ids.height_UOM.name)
                    if self.product_dimension_ids.diameter:
                        self.name += ' x '+str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                if self.product_dimension_ids.lengthx == 0.0:
                    if self.product_dimension_ids.width:
                        self.name += str(self.product_dimension_ids.width) + str(self.product_dimension_ids.width_UOM.name)
                    if self.product_dimension_ids.width > 0.0:
                        if self.product_dimension_ids.thickness:
                            self.name += ' x '+str(self.product_dimension_ids.thickness) + str(self.product_dimension_ids.thickness_UOM.name)
                        if self.product_dimension_ids.height:
                            self.name += ' x '+str(self.product_dimension_ids.height) + str(self.product_dimension_ids.height_UOM.name)
                        if self.product_dimension_ids.diameter:
                            self.name += ' x '+str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                if self.product_dimension_ids.lengthx == 0.0 and self.product_dimension_ids.width==0.0:
                    if self.product_dimension_ids.thickness:
                        self.name += str(self.product_dimension_ids.thickness) + str(self.product_dimension_ids.thickness_UOM.name)
                    if self.product_dimension_ids.thickness != 0:
                        if self.product_dimension_ids.height:
                            self.name += ' x '+str(self.product_dimension_ids.height) + str(self.product_dimension_ids.height_UOM.name)
                        if self.product_dimension_ids.diameter:
                            self.name += ' x '+str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                if self.product_dimension_ids.lengthx == 0.0 and self.product_dimension_ids.width==0.0 and self.product_dimension_ids.thickness == 0.0:
                    if self.product_dimension_ids.height:
                        self.name += str(self.product_dimension_ids.height) + str(self.product_dimension_ids.height_UOM.name)
                    if self.product_dimension_ids.diameter:    
                        if self.product_dimension_ids.height != 0:
                            self.name += ' x '+str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                if self.product_dimension_ids.lengthx == 0.0 and self.product_dimension_ids.width==0.0 and self.product_dimension_ids.thickness == 0.0 and self.product_dimension_ids.height == 0.0:
                    if self.product_dimension_ids.diameter:
                        self.name += str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                self.name += ' ) '

            else:
                for l in self.product_dimension_ids:
                    self.name += '( '
                    if l.lengthx:
                        self.name += str(l.lengthx) + str(l.lengthx_UOM.name)
                    if l.width:
                        self.name += ' x '+str(l.width) + str(l.width_UOM.name)
                    if l.thickness:
                        self.name += ' x '+str(l.thickness) + str(l.thickness_UOM.name)
                    if l.height:
                        self.name += ' x '+str(l.height) + str(l.height_UOM.name)
                    if l.diameter:
                        self.name += ' x '+str(l.diameter) + str(l.diameter_UOM.name)
                    self.name += ' ) '
                    # self.name += '( '
                    # if self.product_dimension_ids.lengthx:
                    #     self.name += str(self.product_dimension_ids.lengthx) + str(self.product_dimension_ids.lengthx_UOM.name)
                    # if self.product_dimension_ids.width:
                    #     self.name += ' x '+str(self.product_dimension_ids.width) + str(self.product_dimension_ids.width_UOM.name)
                    # if self.product_dimension_ids.thickness:
                    #     self.name += ' x '+str(self.product_dimension_ids.thickness) + str(self.product_dimension_ids.thickness_UOM.name)
                    # if self.product_dimension_ids.height:
                    #     self.name += ' x '+str(self.product_dimension_ids.height) + str(self.product_dimension_ids.height_UOM.name)
                    # if self.product_dimension_ids.diameter:
                    #     self.name += ' x '+str(self.product_dimension_ids.diameter) + str(self.product_dimension_ids.diameter_UOM.name)
                    # self.name += ' ) '
    



class ProductProduct(models.Model):
    _inherit = 'product.product'

    material_group = fields.Selection([
                    ('door', 'Door'),
                    ('frame', 'Frame'),
                    ('doorframe','Door Frame'),
                    ('furniture', 'Furniture'),
                    ('others', 'Others')])

    product_dimension_ids = fields.One2many('product.dimension','product_varient_id')

    @api.onchange('material_group')
    def prepare_dimension_lines(self):
        for dimension in self.product_dimension_ids:
            self.product_dimension_ids = [(2,dimension.id)]

        if self.material_group == 'door':
            self.product_dimension_ids.create({'typee':'door','product_varient_id':self.id})

        if self.material_group == 'frame':
            self.product_dimension_ids.create({'typee':'frame','product_varient_id':self.id})

        if self.material_group == 'doorframe':
            self.product_dimension_ids.create({'typee':'shutter','product_varient_id':self.id})
            self.product_dimension_ids.create({'typee':'frame','product_varient_id':self.id})

        if self.material_group == 'furniture' or self.material_group == 'others':
            self.product_dimension_ids.create({'typee':'others','product_varient_id':self.id})


    #concatinate dimension values to product name
    def dimension_to_name(self):
        #add dimensions to name that have been entered
        name_list = self.name.split(' : ')
        name_len = len(name_list)
        if name_len > 1:
            self.name = name_list[0] + ' : ' + name_list[1] + ' : '
        if name_len == 1:
            self.name = name_list[0] + ' : '
        else:
            self.name = ' : '
        if self.material_group:
            if self.material_group != 'doorframe':
                self.name += '( '
                if self.product_dimension_ids.lengthx:
                    self.name += str(self.product_dimension_ids.lengthx)
                if self.product_dimension_ids.width:
                    self.name += ' x '+str(self.product_dimension_ids.width)
                if self.product_dimension_ids.thickness:
                    self.name += ' x '+str(self.product_dimension_ids.thickness)
                if self.product_dimension_ids.height:
                    self.name += ' x '+str(self.product_dimension_ids.height)
                if self.product_dimension_ids.diameter:
                    self.name += ' x '+str(self.product_dimension_ids.diameter)
                self.name += ' ) '

            else:
                self.name += '( '
                if self.product_dimension_ids[0].lengthx:
                    self.name += str(self.product_dimension_ids[0].lengthx)
                if self.product_dimension_ids[0].width:
                    self.name += ' x '+str(self.product_dimension_ids[0].width)
                if self.product_dimension_ids[0].thickness:
                    self.name += ' x '+str(self.product_dimension_ids[0].thickness)
                if self.product_dimension_ids[0].height:
                    self.name += ' x '+str(self.product_dimension_ids[0].height)
                if self.product_dimension_ids[0].diameter:
                    self.name += ' x '+str(self.product_dimension_ids[0].diameter)
                self.name += ' ) '
                self.name += '( '
                if self.product_dimension_ids[1].lengthx:
                    self.name += str(self.product_dimension_ids[1].lengthx)
                if self.product_dimension_ids[1].width:
                    self.name += ' x '+str(self.product_dimension_ids[1].width)
                if self.product_dimension_ids[1].thickness:
                    self.name += ' x '+str(self.product_dimension_ids[1].thickness)
                if self.product_dimension_ids[1].height:
                    self.name += ' x '+str(self.product_dimension_ids[1].height)
                if self.product_dimension_ids[1].diameter:
                    self.name += ' x '+str(self.product_dimension_ids[1].diameter)
                self.name += ' ) '




class SaleOrder(models.Model):
    _inherit = 'sale.order'

    material_group = fields.Selection([
                    ('door', 'Door'),
                    ('frame', 'Frame'),
                    ('doorframe','Door Frame'),
                    ('furniture', 'Furniture'),
                    ('others', 'Others')])

    show_lengthx = fields.Boolean(compute="get_visibility")
    show_width = fields.Boolean(compute="get_visibility")
    show_thickness = fields.Boolean(compute="get_visibility")
    show_height = fields.Boolean(compute="get_visibility")
    show_diameter = fields.Boolean(compute="get_visibility")
    
    show_face_description = fields.Boolean(compute="get_visibility")
    show_back_description = fields.Boolean(compute="get_visibility")
    show_edge_banding = fields.Boolean(compute="get_visibility")

    show_frame_lengthx = fields.Boolean(compute="get_visibility")
    show_frame_width = fields.Boolean(compute="get_visibility")
    show_frame_thickness = fields.Boolean(compute="get_visibility")
    show_frame_height = fields.Boolean(compute="get_visibility")
    show_frame_diameter = fields.Boolean(compute="get_visibility")
    show_frame_description = fields.Boolean(compute="get_visibility")
    show_frame_price = fields.Boolean(compute="get_visibility")
    show_shutter_lengthx = fields.Boolean(compute="get_visibility")
    show_shutter_width = fields.Boolean(compute="get_visibility")
    show_shutter_thickness = fields.Boolean(compute="get_visibility")
    show_shutter_height = fields.Boolean(compute="get_visibility")
    show_shutter_diameter = fields.Boolean(compute="get_visibility")
    show_shutter_description = fields.Boolean(compute="get_visibility")
    show_shutter_price = fields.Boolean(compute="get_visibility")

    @api.depends('order_line','order_line.lengthx','order_line.width','order_line.thickness','order_line.height','order_line.diameter','order_line.face_description','order_line.back_description','order_line.edge_banding','order_line.frame_lengthx','order_line.frame_width','order_line.frame_thickness','order_line.frame_height','order_line.frame_diameter','order_line.frame_description','order_line.frame_price','order_line.shutter_lengthx','order_line.shutter_width','order_line.shutter_thickness','order_line.shutter_height','order_line.shutter_diameter','order_line.shutter_description','order_line.shutter_price')
    def get_visibility(self):
        show_lengthx = False
        for line in self.order_line:
            if line.lengthx:
                show_lengthx = True
                break
        self.show_lengthx = show_lengthx

        show_width = False
        for line in self.order_line:
            if line.width:
                show_width = True
                break
        self.show_width = show_width

        show_thickness = False
        for line in self.order_line:
            if line.thickness:
                show_thickness = True
                break
        self.show_thickness = show_thickness

        show_height = False
        for line in self.order_line:
            if line.height:
                show_height = True
                break
        self.show_height = show_height

        show_diameter = False
        for line in self.order_line:
            if line.diameter:
                show_diameter = True
                break
        self.show_diameter = show_diameter

        show_face_description = False
        for line in self.order_line:
            if line.face_description:
                show_face_description = True
                break
        self.show_face_description = show_face_description

        show_back_description = False
        for line in self.order_line:
            if line.back_description:
                show_back_description = True
                break
        self.show_back_description = show_back_description

        show_edge_banding = False
        for line in self.order_line:
            if line.edge_banding:
                show_edge_banding = True
                break
        self.show_edge_banding = show_edge_banding

        show_frame_lengthx = False
        for line in self.order_line:
            if line.frame_lengthx:
                show_frame_lengthx = True
                break
        self.show_frame_lengthx = show_frame_lengthx

        show_frame_width = False
        for line in self.order_line:
            if line.frame_width:
                show_frame_width = True
                break
        self.show_frame_width = show_frame_width

        show_frame_thickness = False
        for line in self.order_line:
            if line.frame_thickness:
                show_frame_thickness = True
                break
        self.show_frame_thickness = show_frame_thickness

        show_frame_height = False
        for line in self.order_line:
            if line.frame_height:
                show_frame_height = True
                break
        self.show_frame_height = show_frame_height

        show_frame_diameter = False
        for line in self.order_line:
            if line.frame_diameter:
                show_frame_diameter = True
                break
        self.show_frame_diameter = show_frame_diameter

        show_frame_description = False
        for line in self.order_line:
            if line.frame_description:
                show_frame_description = True
                break
        self.show_frame_description = show_frame_description

        show_frame_price = False
        for line in self.order_line:
            if line.frame_price:
                show_frame_price = True
                break
        self.show_frame_price = show_frame_price

        show_shutter_lengthx = False
        for line in self.order_line:
            if line.shutter_lengthx:
                show_shutter_lengthx = True
                break
        self.show_shutter_lengthx = show_shutter_lengthx

        show_shutter_width = False
        for line in self.order_line:
            if line.shutter_width:
                show_shutter_width = True
                break
        self.show_shutter_width = show_shutter_width

        show_shutter_thickness = False
        for line in self.order_line:
            if line.shutter_thickness:
                show_shutter_thickness = True
                break
        self.show_shutter_thickness = show_shutter_thickness

        show_shutter_height = False
        for line in self.order_line:
            if line.shutter_height:
                show_shutter_height = True
                break
        self.show_shutter_height = show_shutter_height

        show_shutter_diameter = False
        for line in self.order_line:
            if line.shutter_diameter:
                show_shutter_diameter = True
                break
        self.show_shutter_diameter = show_shutter_diameter

        show_shutter_description = False
        for line in self.order_line:
            if line.shutter_description:
                show_shutter_description = True
                break
        self.show_shutter_description = show_shutter_description

        show_shutter_price = False
        for line in self.order_line:
            if line.shutter_price:
                show_shutter_price = True
                break
        self.show_shutter_price = show_shutter_price


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lengthx = fields.Float()    
    width = fields.Float()    
    thickness = fields.Float()    
    height = fields.Float()    
    diameter = fields.Float()
    
    face_description = fields.Char()
    back_description = fields.Char()
    edge_banding = fields.Char()

    frame_lengthx = fields.Float()    
    frame_width = fields.Float()    
    frame_thickness = fields.Float()    
    frame_height = fields.Float()    
    frame_diameter = fields.Float()
    frame_description = fields.Char()
    frame_price = fields.Float()
    shutter_lengthx = fields.Float()    
    shutter_width = fields.Float()    
    shutter_thickness = fields.Float()    
    shutter_height = fields.Float()    
    shutter_diameter = fields.Float()
    shutter_description = fields.Char()
    shutter_price = fields.Float()

    @api.onchange('frame_price','shutter_price')
    def set_unit_price_from_framenshutter(self):
        if self.frame_price and self.shutter_price:
            self.price_unit = self.frame_price + self.shutter_price

    @api.onchange('product_id')
    def get_product_dimensions(self):
        if self.product_id.product_tmpl_id.attribute_line_ids:
            if self.product_id.material_group == 'door':

                self.face_description = self.product_id.product_dimension_ids[0].face_description
                self.back_description = self.product_id.product_dimension_ids[0].back_description
                self.edge_banding = self.product_id.product_dimension_ids[0].edge_banding


            if self.product_id.material_group == 'frame':
                self.frame_description = self.product_id.product_dimension_ids[0].description


            if self.product_id.material_group == 'doorframe':
                
                self.shutter_lengthx = self.product_id.product_dimension_ids[0].lengthx
                self.shutter_width = self.product_id.product_dimension_ids[0].width
                self.shutter_thickness = self.product_id.product_dimension_ids[0].thickness
                self.shutter_height = self.product_id.product_dimension_ids[0].height
                self.shutter_diameter = self.product_id.product_dimension_ids[0].diameter
                self.shutter_description = self.product_id.product_dimension_ids[0].description
                
                self.frame_lengthx = self.product_id.product_dimension_ids[1].lengthx
                self.frame_width = self.product_id.product_dimension_ids[1].width
                self.frame_thickness = self.product_id.product_dimension_ids[1].thickness
                self.frame_height = self.product_id.product_dimension_ids[1].height
                self.frame_diameter = self.product_id.product_dimension_ids[1].diameter
                self.frame_description = self.product_id.product_dimension_ids[1].description

            elif self.product_id.material_group:

                self.lengthx = self.product_id.product_dimension_ids[0].lengthx
                self.width = self.product_id.product_dimension_ids[0].width
                self.thickness = self.product_id.product_dimension_ids[0].thickness
                self.height = self.product_id.product_dimension_ids[0].height
                self.diameter = self.product_id.product_dimension_ids[0].diameter

        else:
            if self.product_id.product_tmpl_id.material_group == 'door':

                self.face_description = self.product_id.product_tmpl_id.product_dimension_ids[0].face_description
                self.back_description = self.product_id.product_tmpl_id.product_dimension_ids[0].back_description
                self.edge_banding = self.product_id.product_tmpl_id.product_dimension_ids[0].edge_banding


            if self.product_id.product_tmpl_id.material_group == 'frame':
                self.frame_description = self.product_id.product_tmpl_id.product_dimension_ids[0].description


            if self.product_id.product_tmpl_id.material_group == 'doorframe':
                
                self.shutter_lengthx = self.product_id.product_tmpl_id.product_dimension_ids[0].lengthx
                self.shutter_width = self.product_id.product_tmpl_id.product_dimension_ids[0].width
                self.shutter_thickness = self.product_id.product_tmpl_id.product_dimension_ids[0].thickness
                self.shutter_height = self.product_id.product_tmpl_id.product_dimension_ids[0].height
                self.shutter_diameter = self.product_id.product_tmpl_id.product_dimension_ids[0].diameter
                self.shutter_description = self.product_id.product_tmpl_id.product_dimension_ids[0].description
                
                self.frame_lengthx = self.product_id.product_tmpl_id.product_dimension_ids[1].lengthx
                self.frame_width = self.product_id.product_tmpl_id.product_dimension_ids[1].width
                self.frame_thickness = self.product_id.product_tmpl_id.product_dimension_ids[1].thickness
                self.frame_height = self.product_id.product_tmpl_id.product_dimension_ids[1].height
                self.frame_diameter = self.product_id.product_tmpl_id.product_dimension_ids[1].diameter
                self.frame_description = self.product_id.product_tmpl_id.product_dimension_ids[1].description

            elif self.product_id.product_tmpl_id.material_group:

                self.lengthx = self.product_id.product_tmpl_id.product_dimension_ids[0].lengthx
                self.width = self.product_id.product_tmpl_id.product_dimension_ids[0].width
                self.thickness = self.product_id.product_tmpl_id.product_dimension_ids[0].thickness
                self.height = self.product_id.product_tmpl_id.product_dimension_ids[0].height
                self.diameter = self.product_id.product_tmpl_id.product_dimension_ids[0].diameter

            else:
                if self.product_id.material_group == 'door':

                    self.face_description = self.product_id.product_dimension_ids[0].face_description
                    self.back_description = self.product_id.product_dimension_ids[0].back_description
                    self.edge_banding = self.product_id.product_dimension_ids[0].edge_banding


                if self.product_id.material_group == 'frame':
                    self.frame_description = self.product_id.product_dimension_ids[0].description


                if self.product_id.material_group == 'doorframe':
                    
                    self.shutter_lengthx = self.product_id.product_dimension_ids[0].lengthx
                    self.shutter_width = self.product_id.product_dimension_ids[0].width
                    self.shutter_thickness = self.product_id.product_dimension_ids[0].thickness
                    self.shutter_height = self.product_id.product_dimension_ids[0].height
                    self.shutter_diameter = self.product_id.product_dimension_ids[0].diameter
                    self.shutter_description = self.product_id.product_dimension_ids[0].description
                    
                    self.frame_lengthx = self.product_id.product_dimension_ids[1].lengthx
                    self.frame_width = self.product_id.product_dimension_ids[1].width
                    self.frame_thickness = self.product_id.product_dimension_ids[1].thickness
                    self.frame_height = self.product_id.product_dimension_ids[1].height
                    self.frame_diameter = self.product_id.product_dimension_ids[1].diameter
                    self.frame_description = self.product_id.product_dimension_ids[1].description

                elif self.product_id.material_group:

                    self.lengthx = self.product_id.product_dimension_ids[0].lengthx
                    self.width = self.product_id.product_dimension_ids[0].width
                    self.thickness = self.product_id.product_dimension_ids[0].thickness
                    self.height = self.product_id.product_dimension_ids[0].height
                    self.diameter = self.product_id.product_dimension_ids[0].diameter