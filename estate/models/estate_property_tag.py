from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="This is Tag for an Estate Property"
    
    name=fields.Char('Property Tag')