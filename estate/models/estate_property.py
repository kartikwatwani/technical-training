from odoo import models,fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'This is an Estate Property object.'

    name = fields.Char("Title",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",default=fields.Date.add(fields.Date.today(),months=3),copy=False)
    expected_price = fields.Float("Expected Price",required=True)
    selling_price = fields.Float("Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer("Bedrooms",default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),('east','East'),('west','West')],default='north')
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',selection=[('New','New'),('Offer Received','Offer Received')
    ,('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Canceled','Canceled')]
    ,default='New',required=True,copy=False)

    #Relational
    property_type_id = fields.Many2one('estate.property.type',string="Property Type")
    salesperson_id = fields.Many2one('res.users',default=lambda self:self.env.user,string="Salesman")
    buyer_id = fields.Many2one('res.partner',copy=False,string="Buyer")
    tag_ids = fields.Many2many('estate.property.tag',string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")