from odoo import models, fields, api
import googlemaps
from odoo.exceptions import Warning, ValidationError
import pika
import json
import redis
from uuid import uuid4
import random

class Sale(models.Model):
    _inherit = "sale.order"
    customer_order_status = fields.Char(default="Pending")
    driver_id = fields.Many2one('res.users', string="Driver")
    driver_latitude = fields.Float('Driver_lat', (3, 8),default=0.0)
    driver_longitude = fields.Float('Driver_long', (3, 8),default=0.0)
    driver_order_status = fields.Integer("Driver Order Status",default=0)

    @api.model
    def _generatePickupToken(self):
        token = ""
        for n in range(4):
            token += str(random.randint(0,10))
        return token

    @api.model
    def _generateDeliveryToken(self):
        token = ""
        for n in range(5):
            token += str(random.randint(1,9))
        return token

    pickup_token_confirm = fields.Char("Pickup Token",default= _generatePickupToken)
    delivered_token_confirm = fields.Char("Delivered Token",default=_generateDeliveryToken)


    def receive_order(self):
        order = self.search([('id','=',self.id)])
        order.customer_order_status = "Order Delivered To Vendor"
        return True


    def prepare_order(self):
        order = self.search([('id','=',self.id)])
        order.customer_order_status = "Order prepared by Vendor"
        return True

    def order_ready(self):
        order = self.search([('id','=',self.id)])
        order.customer_order_status = "Order is Ready"
        return True
            

    def find_driver(self):
        distance_array = []
        order = {"name":self.name,"order_id":self.id}
        vendor = self.env["res.users"].search([('company_id','=',self.company_id.id)])
        driver = self.env['res.users'].search([('is_driver', '=', True),('is_online','=',True)])

        if vendor.partner_latitude and vendor.partner_longitude:
            origin = '{},{}'.format(vendor.partner_latitude, vendor.partner_longitude)
            for data in driver:
                if not data.is_ontrip:
                    destination = '{},{}'.format(data.partner_latitude,data.partner_longitude)
                    distance = self.distance_matrix(origin,destination)
                    driver_vendor_distance =  self.driver_location(distance)
                    driver_vendor_distance["order_id"] = self.id
                    driver_vendor_distance["driver_id"] = data.id

                    distance_array.append(driver_vendor_distance)

                elif data.is_ontrip:
                    print("All drivers are on trip,make recursion")

        else:
            print("Please Update your location")

        # sort drivers based on distance from vendor
        sorted_distance = distance_array.sort(key=self.sort_distance)

        #pop the first element of list
        first_distance = distance_array.pop(0)

        # Save remained distance to redis database
        self.save_to_redis(distance_array)

        # send notification to driver
        self.send_to_driver(first_distance)


  


    def distance_matrix(self,origin,destination):
        gmaps = googlemaps.Client(key='AIzaSyCdomGxOD4t7VPHQ7ZHidPLZXo7bYswAr4')
        try:
            distance = gmaps.distance_matrix(origin,destination)
        except:
            raise ValidationError("DistanceMatix API Connection Error")
        return distance


    def driver_location(self,values):

        distance_data = {}
        for data in values["rows"]:

            for distance in data["elements"]:
                distance_data["distance"] = distance["distance"]["text"]
                distance_data["time"] = distance["duration"]["text"]

        return distance_data

    def sort_distance(self,distance_array):
        return float(distance_array["distance"].split()[0])




    def send_to_driver(self,notification):
        products = []
        notification["name"] = self.name
        for product in self.order_line:
            products.append(product["product_id"]["name"])
        notification["product"] = products
        print(notification)

        #start sending notification to driver

        queue_id = str(notification["driver_id"])
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=queue_id)

        channel.basic_publish(exchange='', routing_key=queue_id, body=json.dumps(notification))

        connection.close()

    def save_to_redis(self,values):

        for value in values:
            self.redis_object().rpush(self.name,json.dumps(value))


    def driver_request_cancel(self):

        data = json.loads(self.redis_object().lpop(self.name))

        self.send_to_driver(data)


    def driver_request_accepted(self):

        self.redis_object().delete(self.name)

    #-- Redis Inilized -- 
    def redis_object(self):

        return redis.Redis()