from odoo import models, api, fields

class Company(models.Model):
    _inherit = 'res.company'
    website_size_x = fields.Integer('Size X', default=1)
    website_size_y = fields.Integer('Size Y',default=1)
    website_style_ids = fields.Many2many('product.style', string='Styles')