from odoo import models,fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'This is an Estate Property object.'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availabilty = fields.Date(default=fields.Date.add(fields.Date.today(),months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),('east','East'),('west','West')],default='north')
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',selection=[('New','New'),('Offer Received','Offer Received')
    ,('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Canceled','Canceled')]
    ,default='New',required=True,copy=False)