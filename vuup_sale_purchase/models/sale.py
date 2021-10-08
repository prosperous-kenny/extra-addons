from odoo import api, models,fields


class Sale(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        super(Sale,self).action_confirm()

        po_line = self.env['purchase.order.line'].search([('sale_order_id','=',self.id)])

        po_line.order_id.button_confirm()

        return True
