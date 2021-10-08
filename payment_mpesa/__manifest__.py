{
    'name': 'Mobile Payment: Vodacom Mpesa',
    'description': 'Payment Acquirer: Vodacom Mpesa implementation',
    'depends': ['payment'],
    'installable': True,
    'data': [
        'views/payment_view.xml',
        'views/payment_mpesa_templates.xml',
        'data/payment_acquirer_data.xml',

    ]
}