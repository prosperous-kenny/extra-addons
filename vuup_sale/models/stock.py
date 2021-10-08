from odoo import models,fields,api
class Stock(models.Model):
    _inherit = 'stock.move'
    product_id = fields.Many2one(check_company=False)
    location_id = fields.Many2one(check_company=False)
    