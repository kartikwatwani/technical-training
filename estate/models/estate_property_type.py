from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is Estate Property Type."

    name= fields.Char()
    _sql_constraints = [('check_property_type','UNIQUE(name)','Property Type should be unique')]

    property_ids = fields.One2many('estate.property','property_type_id')