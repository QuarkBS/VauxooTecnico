from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"
    _order = "name desc"

    name = fields.Char(required = True) 
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute = "_compute_offercount")
    _sql_constraints = [
        ('check_name', 
            'CHECK(Unique(name))', 
            'Type name cannot be repeated!')]

    @api.depends("offer_ids")
    def _compute_offercount(self):
        for record in self:
            record.offer_count = len(record.offer_ids)