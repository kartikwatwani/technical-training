from odoo import api, models, fields

from odoo.exceptions import UserError, ValidationError

from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):

    _name = 'estate.property'

    _description = 'This is an Estate Property object.'

    name = fields.Char("Title", required=True)

    description = fields.Text("Description")

    postcode = fields.Char("Postcode")

    date_availability = fields.Date("Available From", default=fields.Date.add(
        fields.Date.today(), months=3), copy=False)

    expected_price = fields.Float("Expected Price", required=True)

    selling_price = fields.Float("Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer("Bedrooms", default=2)

    living_area = fields.Integer("Living Area (sqm)", default=0)

    facades = fields.Integer("Facades")

    garage = fields.Boolean("Garage")

    garden = fields.Boolean("Garden")

    garden_area = fields.Integer("Garden Area (sqm)", default=0)

    garden_orientation = fields.Selection(string='Garden Orientation',

                                          selection=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West')])

    active = fields.Boolean(default=True)

    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), (
        'offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], default='new', required=True, copy=False)

    total_area = fields.Integer(

        "Total Area (sqm)",
        compute="_compute_total_area",

        help="Total area computed by summing the living area and the garden area",
    )

    best_price = fields.Integer("Best Offer", compute="_compute_best_offer")

    # Relational

    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")

    salesperson_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user, string="Salesman")

    buyer_id = fields.Many2one('res.partner', copy=False, string="Buyer")

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string="Offers")

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price > 0)',
                         'The expected price should be greater than 0.'),

                        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price of a property should be greater than 0.')]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden_state(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        print('Check selling price called')
        for record in self:
            if (not float_is_zero(record.selling_price, precision_rounding=0.01)
                    and float_compare(record.selling_price, 0.9*record.expected_price, precision_rounding=0.01) < 0):
                raise ValidationError(
                    'Selling Price cannot be less than '+str(0.9*record.expected_price))

    def mark_as_sold(self):
        for record in self:
            if (record.state == 'canceled'):
                raise UserError('Canceled property cannot be marked as sold')
            else:
                record.state = 'sold'
        return True

    def mark_as_canceled(self):
        for record in self:
            if (record.state == 'sold'):
                raise UserError('Sold property cannot be marked as canceled.')
            else:
                record.state = 'canceled'

        return True
