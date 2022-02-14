from email.policy import default
from odoo import models,fields,api,_
# from python import pudb
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


# Estate Property class

class EstateProperty(models.Model):
    _name='estate.property'
    _description='This is my real estate property Module class'
    _order="expected_price desc"

    # def _default_description(self):
    #     if self.env.context.get('is_my_property'):
    #         return self.env.user.name + "'s Property"
    
    def _get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name + "'s Property"
 
    ref_seq = fields.Char(string="Reference ID",default="New")
    name = fields.Char(string="Title", default="Unknown", required=True)

    # def _default_description(self):
    #     return self.env['res.users'].search([('user_id','=',self.env.uid)])
        

    description = fields.Text(default=_get_description)
    postcode = fields.Char()
    # lambda function use for take the any data from without declaring the function body here I use this for take date and time from
    date_availability = fields.Date(default=lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    validity = fields.Integer(default=7,compute="_get_validity",search='_search_validity')
    image=fields.Image()

# Selection fields
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')        
        ])
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
    
# Relational fiels
    owner_id  = fields.Many2one('res.partner')
    property_type_id = fields.Many2one('estate.property.type', ondelete="restrict")
    property_tag_ids=fields.Many2many('estate.property.tag')
    salesman_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')

# Computed and inverse fields
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_invert_deaddate")
    best_price = fields.Float(compute="_compute_best_price", store=True)
    total_area=fields.Integer(compute="_compute_total_area",inverse="_inverse_area")


# python decorator methods

    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.garden_area + record.living_area


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability, days=record.validity)
            
            # date_availability
    def _invert_deaddate(self):
        for record in self:
            record.validity = int((record.date_deadline - record.date_availability).days)


    @api.depends('property_offer_ids.price')
    def _compute_best_price(self): # Recordset [ Collection  of records]
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    @api.depends('property_offer_ids.status')
    def _compute_sold(self):
        for record in self:
            sold_price = 0
            buyer_name = None
            for offer in record.property_offer_ids:
                    if offer.status == 'accepted':
                        sold_price = offer.price
                        buyer_name = offer.partner_id 
            record.selling_price = sold_price
            record.buyer_id = buyer_name

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None


    @api.onchange('date_availability')
    def _start_end_date(self):
        for record in self:
            if record.date_availability:
                record.date_deadline=record.date_availability + relativedelta(days=30)


    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")
                # return{
                #     'warnning':{
                #         'title':"Incorrect Area Entered",
                #         'message':"Please etnter garden area less then the living area !"
                #         }
                # }

    @api.constrains('date_availability', 'date_deadline')
    def _check_instructor(self):
        if self.date_availability > self.date_deadline:
            raise UserError(_("Deadline Date must be less then Availibity Date."))


    @api.model
    def create(self, vals):
        # vals is a dict of all fields with values or default values  -> insert
        if vals.get('ref_seq', 'New') == 'New':
            vals['ref_seq'] = self.env['ir.sequence'].next_by_code('property.seq')

        t =  super(EstateProperty, self).create(vals)
        return t
    
    # Inverse method for computed method
    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    @api.depends('date_deadline') #Inverse validity
    def _set_validity(self):
        for record in self:
            record.date_deadline = record.date_availability + relativedelta(days=record.validity)

    @api.depends('date_availability', 'date_deadline') #compute validity
    def _get_validity(self):
        for record in self:
            if record.date_deadline and record.date_availability:
                diff = record.date_deadline - record.date_availability
                record.validity = diff.days
            else:
                record.validity = 7

    


# Methods for button actions
    def action_sold(self):
        # print("\n\n In action sold")
        for record in self:
            if record.state=='cancel':
                raise UserError("Cancel Property cannot be sold")
            record.state = 'sold'
            # return some action 

    def action_cancel(self):
        for record in self:
            if record.state=='sold':
                raise UserError("Sold Property cannot be canceled")
            record.state = 'cancel'


    def open_offers(self):
        view_id_all = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_all, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }

    def open_confirm_offers(self):
        print ("\n\ncontext is ::: ", self.env.context)
        view_id_accept = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_accept, 'tree']],
            # "res_id": 2,
            # "target":"new",
            "domain": [('property_id', '=', self.id),('status','=','accepted')]
            }
# Search method for computed field

    def _search_validity(self, operator, value):
        self.env.cr.execute("SELECT id from estate_property where date_availability::DATE - date_deadline::DATE %s %s" %(operator, value))
        ids = self.env.cr.fetchall()
        return [('id', 'in', [id[0] for id in ids])]
    

 
# Res partner view




#Property type class
class Property_type(models.Model):
    _name='estate.property.type'
    _description='This is property type.'

    name=fields.Char()
    property_ids=fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count =  len(record.offer_ids)


# Property tage class
class Property_tag(models.Model):
    _name='estate.property.tag'
    _description='This is tag of the properties'

    name=fields.Char()
    color=fields.Integer()


# Property offer class
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'),('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id',store=True)


    # def action_accepted(self):
    #     # Open the view only if we find the duplicate price or same price
    #     for record in self:
    #         # record.price
    #         same_price = []
    #         for rec in record.property_id.property_offer_ids:
    #             if rec.price == record.price and rec.id != record.id:
    #                 same_price.append(rec)

    #         if same_price:
    #             # view_id = self.env.ref('estate.estate_property_offer_tree').id
    #             partner_ids = [record.partner_id.id]
    #             for r in same_price:
    #                 partner_ids.append(r.partner_id.id)
    #             return {
    #                 "name": "Confirm Accept",
    #                 "type": "ir.actions.act_window",
    #                 "res_model": "confirm.accept",
    #                 "views": [[False, 'form']],
    #                 # "res_id": 2,
    #                 "target": "new",
    #                 "context" : {'default_selected_partner_id' : record.partner_id.id, 'partners': partner_ids},
    #                 "domain": [('selected_partner_id', 'in', partner_ids)]
    #             }
    #         else:
    #             pass


    def action_refused(self):
        for record in self:
            record.status = 'refuse'

    def action_accepted(self):
        for record in self:
            record.status = 'accepted'
