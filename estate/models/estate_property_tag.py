from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="This is Tag for an Estate Property"

    name=fields.Char('Property Tag')
    _sql_constraints = [('check_name','UNIQUE(name)','Property Tag should be unique.')]