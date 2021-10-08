from odoo import fields, models, api

class Order(models.Model):
    _name = 'order.driver'
    _description = "Order Driver"
    distance = fields.Char()
    driver_id = fields.Integer()
    driver_name = fields.Char()
    duration = fields.Char()
    order_id = fields.Integer()
