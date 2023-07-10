from odoo import api,models,fields
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
    living_area = fields.Integer("Living Area (sqm)",default=0)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)",default=0)
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('N', 'North'), ('S', 'South'),('E','East'),('W','West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',selection=[('New','New'),('Offer Received','Offer Received')
    ,('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Canceled','Canceled')]
    ,default='New',required=True,copy=False)
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Integer("Best Offer",compute="_compute_best_offer")

    #Relational
    property_type_id = fields.Many2one('estate.property.type',string="Property Type")
    salesperson_id = fields.Many2one('res.users',default=lambda self:self.env.user,string="Salesman")
    buyer_id = fields.Many2one('res.partner',copy=False,string="Buyer")
    tag_ids = fields.Many2many('estate.property.tag',string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area  

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden_state(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = None    