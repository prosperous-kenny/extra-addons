{
    "name":"Vuup",
    "description":"Manage Vendor products, Sales, purchase and Accounting in Multicompany Form",
    "depends":['stock','payment','sale_management'],
    "application":True,
    "data":[
             "security/vuup_app_security.xml",
             "security/ir.model.access.csv",
             "views/vuup_menu.xml",
             "views/vuup_order.xml",
             "views/sale.xml"
         ]
    
     }
