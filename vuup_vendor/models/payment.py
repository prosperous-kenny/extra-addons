from odoo import models,fields
import googlemaps
from odoo.exceptions import Warning, ValidationError

class Payment(models.Model):
    _inherit = 'payment.transaction'
    customer_order_status = fields.Char(default="Pending")
    company_id = fields.Many2one('res.company', string="Vendor")
    order_id = fields.One2many('sale.order.line',string='Order Line', related='sale_order_ids.order_line')
    driver_id = fields.Many2one('res.users', string="Driver")
    driver_latitude = fields.Float('Driver_lat', (3,8))
    driver_longitude = fields.Float('Driver_long', (3,8))

    def receive_order(self):
        order = self.search([('reference','=',self.reference)])
        order.customer_order_status = "Order Delivered To Vendor"
        return True


    def prepare_order(self):
        order = self.search([('reference','=',self.reference)])
        order.customer_order_status = "Order prepared by Vendor"
        return True

    def order_ready(self):
        order = self.search([('reference','=',self.reference)])
        order.customer_order_status = "Order is Ready"
        return True

    def find_driver(self):
        distance_data = []
        order = {"reference":self.reference,"order_id":self.id}
        driver = self.env['res.users'].search([('is_driver', '=', True)])
        for data in driver:
            if data.partner_latitude or data.partner_longitude:
                origin = '{},{}'.format(self.env.user.partner_latitude,self.env.user.partner_longitude)
                destination = '{},{}'.format(data.partner_latitude,data.partner_longitude)
                distance = self.distance_matrix(origin,destination)
                send_order = self.set_driver_data(distance)
                send_order['driver_id'] = data.id
                send_order['driver_name'] = data.name

            distance_data.append(send_order)
        print("Data:"+str(distance_data))
        # print("Order: "+ str(order))


    def distance_matrix(self,origin,destination):
        gmaps = googlemaps.Client(key='AIzaSyCdomGxOD4t7VPHQ7ZHidPLZXo7bYswAr4')
        try:
            distance = gmaps.distance_matrix(origin,destination)
            print(str(distance))
        except:
            raise ValidationError("DistanceMatix API Connection Error")
        return distance

    def set_driver_data(self,driver_location):
        distance_data = {}
        for location in driver_location['rows']:
            for data in location["elements"]:
                distance_data["distance"] = data["distance"]["text"]
                distance_data["duration"] = data["duration"]["text"]
        return distance_data

    # def send_to_driver(self,order,driver_id):


# class Sale(models.Model):
#     _inherit = 'sale.order'
#     payment_id = fields.Many2one('payment.transaction',string="Order Payment", related='order_id')
        