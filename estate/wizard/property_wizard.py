from odoo import api, fields, models, _

class property_wizard(models.TransientModel):
    _name = "property.wizard"

    #tag_id = fields.Many2many('estate.property.tags')

    price = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Name')


    def action_add_offer(self):
        activeIds = self.env.context.get('active_ids')
        data={
                'price':self.price,
                'partner_id':self.partner_id,
        }
        for x in activeIds:
            self.env['estate.property.offer'].create({'price':self.price ,'partner_id': self.partner_id.id,'property_id':x})
        return True