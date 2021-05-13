# -*- coding: utf-8 -*-
# from odoo import http


# class Dimensions14(http.Controller):
#     @http.route('/dimensions_14/dimensions_14/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dimensions_14/dimensions_14/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dimensions_14.listing', {
#             'root': '/dimensions_14/dimensions_14',
#             'objects': http.request.env['dimensions_14.dimensions_14'].search([]),
#         })

#     @http.route('/dimensions_14/dimensions_14/objects/<model("dimensions_14.dimensions_14"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dimensions_14.object', {
#             'object': obj
#         })
