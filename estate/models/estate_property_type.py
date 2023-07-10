from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is Estate Property Type."

    name= fields.Char()