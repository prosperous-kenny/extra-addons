{
    'name':'Mobile Payment: Tigo Pesa',
    'description':'Payment Acquirer: Tigo Pesa implementation',
    'depends':['payment'],
    'installable': True,
    'data':[
          'views/payment_view.xml',
          'views/payment_tigopesa_templates.xml',
          'data/payment_acquirer_data.xml',
          
    ]
}