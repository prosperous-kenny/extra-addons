import json
from odoo import http,_
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
from odoo.addons.phone_validation.tools.phone_validation import phone_sanitize_numbers
import pika
import re

class TigoController(http.Controller):
    @http.route(['/payment/tigo/s2s/create_json_3ds'],auth='public',type='json', csrf=False)
    def tigo_s2s_create_json_3ds(self,verify_validity=False,**post):
        token = False
        
        print(post.get('acquirer_id'))
        phone = post.get('tigo_phone_number')
        sanitized_number = self._check_values(phone)
        tigo_number = sanitized_number[1:]
        
        acquirer = request.env['payment.acquirer'].browse(int(post.get('acquirer_id')))
        
        tigo_phone_number = acquirer.write({'tigo_phone_number':tigo_number})
        
        try:
            if not post.get('partner_id'):
                post = dict(post, partner_id=request.env.user.partner_id.id)
            token = acquirer.s2s_process(post)
            
        except ValidationError as e:
            message = e.args[0]
            if isinstance(message,dict) and 'missing_fields' in message:
                if request.env.user._is_public():
                    message = _("Please sign in to complete the payment")
                    # update message if portal mode = b2b
                    if request.env['ir.config_parameter'].sudo().get_param('auth_signup.allow_uninvited', 'False').lower() == 'false':
                        message += _(" If you don't have any account, ask your salesperson to grant you a portal access. ")
                else:
                    msg = _("The transaction cannot be processed because some contact details are missing or invalid: ")
                    message = msg + ', '.join(message['missing_fields']) + '. '
                    message += _("Please complete your profile. ")
                
            return {
                'error':message
            }
            
        except UserError as e:
            return {
                'error': e.name
            }
            
        if not token:
            res = {
                'result':False
            }
            return res
        
        res = {
            'result':True,
            'id':token.id,
            '3d_secure':False,
            'verified':True
        }
        
        return res
    
    
    
    
    def _check_values(self,phone):
        sanitized_number = None
        if phone:
            if phone.startswith('0'):
                phone = '+255'+phone[1:]
            elif phone.startswith('255'):
                phone = '+'+phone
            sanitized_number = phone_sanitize_numbers([phone], None, None).get(phone, {}).get('sanitized')
            if not sanitized_number:
                raise ValidationError("Ivalid phone number")
        return sanitized_number
    
    #-----------------------------------------------------------------------------
    # calback for web client
    #-----------------------------------------------------------------------------
    @http.route(['/payment/tigo/callback'],type='json',auth='public', csrf=False)
    def tigo_pay(self,*post):
        response = json.loads(re.sub(r"[\([)\]]", "",request.httprequest.data.decode("utf-8")))
        trans = request.env['payment.transaction'].sudo().search([('acquirer_reference','=',response['ref'])])
        
        if response['status']:
            trans._set_transaction_done()
        else:
            trans._set_transaction_cancel()
        
        return response['status']
    
    
    
    
    #------------------------------------------------------------------------
    #callback for mobile client
    #------------------------------------------------------------------------
    @http.route(['/callback/tigo'],type='json',auth="public",methods=['POST'])
    def tigo_callback(self,*post):
        response = re.sub(r"[\([)\]]", "",request.httprequest.data.decode("utf-8"))
        print(response)
        print(json.loads(response))
        print(type(response))

        queue_id = json.loads(response)["ref"]
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

        channel = connection.channel()

        channel.queue_declare(queue=queue_id)

        channel.basic_publish(exchange='', routing_key=queue_id, body=response)

        connection.close()
        return json.loads(response)