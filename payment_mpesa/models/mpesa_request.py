import requests
from requests.auth import HTTPBasicAuth
from odoo.exceptions import UserError
from odoo import http, _
import json


class MpesaApi():

    def __init__(self, acquirer,amount):
        if acquirer.state == 'enabled':
            self.login_url = acquirer.vodacom_login_url
            self.bill_url = acquirer.vodacom_bill_url
            self.username = acquirer.vodacom_username
            self.password = acquirer.vodacom_password
            self.ref = acquirer.vodacom_ref
            self.amount = amount,
            self.msisdn = acquirer.vodacom_phone_number
            self.remarks = acquirer.vodacom_payment_remarks
            self.callback = acquirer.vodacom_callback_url

    def mpesa_login(self):
        # headers = {'X-API-KEY': 'Yw4dPFwlycveznM8IFgBc8iUMCueYKZk'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.login_url, auth=HTTPBasicAuth(self.username, self.password), headers=headers)
        return response

    def mpesa_bill(self):
        payload = {
            'ref': self.ref,
            'msisdn': self.msisdn,
            'amount': self.amount,
            'remarks': self.remarks,
            'callback': self.callback
        }

        login = self.mpesa_login()

        if login.status_code != 200:
            raise UserError(_("Payment Login Error %s" % login.reason))

        token = json.loads(login.text)['access_token']
        headers = {
            'Content-type': 'Application/json',
            'Accept': 'Application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.post(self.bill_url, json=payload, headers=headers)

        if response.status_code != 200:
            raise UserError(_("Payment bill Error %s " % response.reason))

        return {
            'status_code': response.status_code,
            'response': json.loads(response.text)
        }

