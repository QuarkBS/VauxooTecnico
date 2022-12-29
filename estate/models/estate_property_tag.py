from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name desc"

    name = fields.Char(required = True)
    color = fields.Integer()

    _sql_constraints    =    [
        ('uniq_name',
            'UNIQUE (name)',
            'Tag name cannot be repeated!')]