from odoo import fields, models, api

class ProductRecipe(models.Model):
    _name = 'product.side'
    _description = 'Side Dish'
    name = fields.Char('Name')
    company_id = fields.Many2one("res.company",'Vendor')



