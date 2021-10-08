from odoo import models, fields

class Company(models.Model):
    _inherit = 'res.company'
    company_latitude = fields.Float('Geo latitude',(3,8))
    company_longitude = fields.Float('Geo longitude',(3,8))