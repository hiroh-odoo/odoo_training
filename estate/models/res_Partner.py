from odoo import api,models,fields

class ResPartner(models.Model):
    _inherit = "res.partner"
    buyer_property_id = fields.One2many('estate.property', 'buyer_id')
    is_buyer=fields.Boolean()