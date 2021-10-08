from odoo import fields, models

class Category(models.Model):
    _inherit = 'product.category'
    company_id = fields.Many2one('res.company',string='Vendor')
    category_image = fields.Binary('Image', required=True)


# class Product(models.Model):
#     _inherit = 'product.product'
#     side_id = fields.Many2one('product.side','Sides')