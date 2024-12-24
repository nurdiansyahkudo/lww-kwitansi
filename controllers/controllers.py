# -*- coding: utf-8 -*-
# from odoo import http


# class LwwKwitansi(http.Controller):
#     @http.route('/lww_kwitansi/lww_kwitansi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lww_kwitansi/lww_kwitansi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lww_kwitansi.listing', {
#             'root': '/lww_kwitansi/lww_kwitansi',
#             'objects': http.request.env['lww_kwitansi.lww_kwitansi'].search([]),
#         })

#     @http.route('/lww_kwitansi/lww_kwitansi/objects/<model("lww_kwitansi.lww_kwitansi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lww_kwitansi.object', {
#             'object': obj
#         })

