{
    'name':"Real Estate",
    'category':'Sales',
    'author':'Himanshu Rohit',
    'application':True,
    'data':[
        'security/ir.model.access.csv',
        'security/estate_security.xml',
        'views/estate_property_view.xml',
        'views/estate_property_menus_action.xml',
        'views/template.xml',
        'wizard/offer_wizard_view.xml',
    ],
    'depends': ['base'],
}