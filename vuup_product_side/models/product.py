from odoo import models, api, fields

class Product(models.Model):
    _inherit = 'product.template'
    side_dish_id = fields.Many2many('product.side')