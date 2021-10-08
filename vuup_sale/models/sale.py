from odoo import models,api,fields

class Sale(models.Model):
    _inherit = 'sale.order.line'
    product_id = fields.Many2one(check_company=False)



class Purchase(models.Model):
    _inherit = 'stock.move'
    product_id = fields.Many2one(check_company=False)