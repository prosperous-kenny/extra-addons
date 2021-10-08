import requests
from requests.auth import HTTPBasicAuth
from odoo.exceptions import UserError
from odoo import http,_
import json
class TigoApi():
  
    def __init__(self,acquirer,amount):
        if acquirer.state == 'enabled':
            self.login_url = acquirer.tigo_login_url
            self.bill_url = acquirer.tigo_bill_url
            self.username = acquirer.tigo_username
            self.password = acquirer.tigo_password
            self.ref = acquirer.tigo_ref
            self.amount = amount,
            self.msisdn = acquirer.tigo_phone_number
            self.remarks = acquirer.tigo_payment_remarks
            self.callback = acquirer.tigo_callback_url
            
          
    def tigo_login(self):
        # headers = {'X-API-KEY':'Yw4dPFwlycveznM8IFgBc8iUMCueYKZk'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.login_url,auth=HTTPBasicAuth(self.username,self.password),headers=headers)
        return response

    def tigo_bill(self):
        payload = {
                'ref': self.ref,
                'msisdn': self.msisdn,
                'amount': self.amount,
                'remarks': self.remarks,
                'callback': self.callback
                    }
        
        login = self.tigo_login()
        
        if login.status_code != 200:
            raise UserError(_("Payment Login Error %s" % login.reason))
        
        token = json.loads(login.text)['access_token']
        headers = {
                'Content-type':'Application/json',
                'Accept':'Application/json',
                'Authorization':'Bearer '+ token
                    }
            
        response = requests.post(self.bill_url,json=payload,headers=headers)
        
        if response.status_code != 200:
            raise UserError(_("Payment bill Error %s " % response.reason))
        
        
        return {
            'status_code': response.status_code,
            'response': json.loads(response.text)
        }
            
