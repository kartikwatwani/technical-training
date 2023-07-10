from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is offer for an estate property."

    
    price = fields.Float('Price')
    status = fields.Selection(string='Status', copy=False, selection=[
                              ('Accepted', 'Accepted'), ('Refused', 'Refused')])
    partner_id = fields.Many2one('res.partner',string='Partner')
    property_id = fields.Many2one('estate.property',string="Property ID")
