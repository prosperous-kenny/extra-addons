from datetime import datetime
from requests import status_codes
from odoo import models, fields, api
from uuid import uuid4
from .mpesa_request import MpesaApi
import logging

_logger = logging.getLogger(__name__)


class PaymentMpesa(models.Model):
    _inherit = 'payment.acquirer'
    provider = fields.Selection(selection_add=[('mpesa', 'Vodacom Mpesa')])
    vodacom_login_url = fields.Char('Login Url')
    vodacom_bill_url = fields.Char('Bill Url')
    vodacom_username = fields.Char('username')
    vodacom_password = fields.Char('password')
    vodacom_phone_number = fields.Char('Mpesa phone number')
    vodacom_ref = fields.Char('Ref')
    vodacom_payment_remarks = fields.Char('Remarks')
    vodacom_callback_url = fields.Char('Callback')

    def mpesa_s2s_form_process(self, data):
        if not data.get('partner_id') and data.get('acquirer_id'):
            raise ValueError("Payment Form contain invalid fields")

        payment_token = self.env['payment.token'].sudo().create({
            'acquirer_ref': uuid4(),
            'partner_id': int(data['partner_id']),
            'acquirer_id': int(data['acquirer_id'])
        })
        return payment_token

    def mpesa_s2s_form_validate(self, data):
        error = dict()

        required_fields = ['vodacom_phone_number', 'acquirer_id', 'partner_id']

        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        return False if error else True


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def mpesa_s2s_do_transaction(self, **post):
        self.ensure_one()
        transaction = MpesaApi(self.acquirer_id,self.amount)
        res = transaction.mpesa_bill()
        print("MpesaApi: " + str(res))
        return self.mpesa_s2s_validate_tree(res)

    def mpesa_s2s_validate_tree(self, tree):
        return self._mpesa_s2s_validate(tree)

    def _mpesa_s2s_validate(self, tree):
        if self.state not in ['draft', 'pending']:
            _logger.warning("Mpesa: trying to validate an already validated tx (ref %s) % self.reference")
            return True
        status_code = tree.get('status_code')

        if status_code == 200:
            init_state = self.state
            self.write({
                'acquirer_reference': tree.get('response').get('uid'),
                'date': fields.Datetime.now()
            })

            if init_state != 'done':
                self.execute_callback()

        return True





