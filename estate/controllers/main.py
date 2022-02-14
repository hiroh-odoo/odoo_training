from odoo import http
from odoo.http import request


class Estate(http.Controller):
    @http.route(['/property','/property/static/<string:is_static>'],website=True,auth='public')
    def estate_porperty_show(self,is_static=False, **kw):

        if is_static:
            return request.render('estate.property_static', {
                'properties': request.env['estate.property'].sudo().search([], limit=8)
            })

        return request.render('estate.property', {
                'properties': request.env['estate.property'].sudo().search([], limit=8)
            })


        # properties = request.env['estate.property'].sudo().search([])
        # return request.render("estate.property",{
        #         'properties':properties,
        # })

    @http.route(['/property/<model("estate.property"):property>', '/property/<string:is_static>'], auth="public", website=True)
    def property_details(self, property=False, **kw):
        if property:
            return request.render('estate.property_details', {
                'property': property,
            })

