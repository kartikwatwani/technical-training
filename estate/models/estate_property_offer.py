from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is offer for an estate property."

    price = fields.Float('Price')
    status = fields.Selection(string='Status', copy=False, selection=[
                              ('Accepted', 'Accepted'), ('Refused', 'Refused')])

    validity = fields.Integer('Validity (in days)', default=7)
    date_deadline = fields.Date('Deadline date', compute="_compute_deadline",inverse="_compute_validity")
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string="Property ID")

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _compute_validity(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
