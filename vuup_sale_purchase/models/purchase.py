from odoo import models, api
class Purchase(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _automate_order_confirm(self):
        purchase = self.env['purchase.order'].search(['|',('state','=','draft'),('state','=','sent')])
        if purchase:
            for order in purchase:
                order.button_confirm()
                print(str(order))
        print(str(purchase))
        print("Now it is time to automate")






    
   
        


        
