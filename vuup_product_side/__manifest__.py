{
    "name":"Side Dish",
    "description": "Addition dish on product sale",
    "depends":['vuup_product'],
    "application": False,
    "data":[
           "security/ir.model.access.csv",
           "views/product_sides_menu.xml",
           "views/product.xml"
    ]
}