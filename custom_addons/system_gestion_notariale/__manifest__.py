{
    'name' : 'Gestion Notariale',
    'version' : '1.0',
    'summary': 'Module pour gérer les activités notariales.',
    'author': 'EKBlocks',
    'depends': [
        'base'
    ],

    'data': [   
        "security/ir.model.access.csv",
        "views/sgn_client_view.xml",
        "views/sgn_nationality_view.xml",
        "menu/client_menu.xml",
    ],
    'license': 'LGPL-3',
    'application': True,


}