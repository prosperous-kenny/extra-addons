from odoo import fields, models

class User(models.Model):
    _inherit = 'res.users'
    is_driver = fields.Boolean('Is Driver', default=False)
    is_online = fields.Boolean('Is Driver Online', default=False)
    is_ontrip = fields.Boolean('Is Driver Ontrip', default=False)