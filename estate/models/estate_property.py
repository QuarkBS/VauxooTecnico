from odoo import api, fields, models, exceptions, tools

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Mi primera app en odoo xD"
    _order = "id desc"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default=lambda self: fields.Datetime.add(fields.Datetime.today(),month=3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_area")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(default = 'new',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
    )
    active = fields.Boolean(default = True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string = "Tags ids")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_best_price")

    _sql_constraints = [
        ('check_expected_price', 
            'CHECK(expected_price > 0)', 
            'Expected price must always be a positive value or zero'),
        ('check_selling_price', 
            'CHECK(selling_price >= 0)', 
            'Selling price must always be a positive value or zero')]

    @api.depends("living_area","garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids")
    def _best_price(self):
        for record in self:
            map = record.offer_ids.mapped("price")
            if len(map) > 0:
                record.best_price = max(map)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("Cancelled properties can not be sold.")
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold properties can not be cancelled.")
            else:
                record.state = "cancelled"
        return True

    @api.constrains('selling_price')
    def _assing_selling_price(self):
        for record in self:
            if tools.float_utils.float_compare(record.selling_price, 0.9*record.expected_price, precision_digits=2) < 0:
                raise exceptions.ValidationError("The selling price cannot be lower than 90 percent of the expected price!")

    @api.ondelete(at_uninstall=False)
    def checkdelete(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise exceptions.UserError("Only new or cancelled properties can be deleted!")