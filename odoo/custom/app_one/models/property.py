from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"

    name = fields.Char(required=True, size=20)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date()
    expect_price = fields.Float(digits=(0, 3))
    selling_price = fields.Float(digits=(0, 3))
    diff_in_price = fields.Float(compute="_compute_diff_in_price")
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orietation = fields.Selection(
        [("north", "north"), ("south", "south"), ("east", "east"), ("west", "west")]
    )
    status = fields.Selection(
        [("draft", "draft"), ("pending", "pending"), ("sold", "sold")],
    )
    owner = fields.Many2one("owner")
    owner_address = fields.Char(related="owner.address")
    owner_phone = fields.Char(related="owner.phone")
    tag_ids = fields.Many2many("tag")

    @api.constrains("bedrooms")
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Please enter a valid value for bedrooms.")

    def action_draft(self):
        for rec in self:
            print("inside draft method")
            rec.status = "draft"

    def action_sold(self):
        for rec in self:
            print("inside sold method")
            rec.status = "sold"

    def action_pending(self):
        for rec in self:
            print("inside pendings method")
            rec.status = "pendings"

    @api.depends("selling_price", "expect_price")
    def _compute_diff_in_price(self):
        for rec in self:
            rec.diff_in_price = rec.selling_price - rec.expect_price
