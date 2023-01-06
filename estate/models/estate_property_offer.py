from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    create_date = fields.Date(default=fields.Datetime.today())
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )
    _sql_constraints = [("check_price", "CHECK(price > 0)", "Price must always be a positive value!")]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.validity is not False:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.validity is not False:
                record.validity = int((record.date_deadline - record.create_date).days)

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        for record in self.env["estate.property"].browse(vals["property_id"]).offer_ids:
            if vals["price"] < record.price:
                raise exceptions.ValidationError("Your price offer is lower than the current offers!")

        propertystate = self.env["estate.property"].browse(vals["property_id"])
        propertystate.state = "offer received"
        return super().create(vals)
