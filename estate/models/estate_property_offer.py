from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is offer for an estate property."

    price = fields.Float('Price')
    state = fields.Selection(string='Status', copy=False, selection=[
                              ('accepted', 'Accepted'), ('refused', 'Refused')])

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

    def action_accept_offer(self):
     for offer in self:    
        if('accepted' in self.property_id.offer_ids.mapped('state')):
            raise UserError('An offer has already been accepted and the property is sold.')
        else:
            offer.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'sold' 

    def action_refuse_offer(self):
        for offer in self:

            if(offer.state!='accepted'):
                offer.state = 'refused'
            else:
                raise UserError('This offer has already been accepted.')          
