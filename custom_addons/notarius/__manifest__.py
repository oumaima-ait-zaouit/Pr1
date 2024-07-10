{
    'name' : 'Notarius',
    'version' : '1.0',
    'summary': 'Notary App test test',
    'depends': [
        'base','mail', 'contacts'
    ],

    'data': [   
        "security/ir.model.access.csv",
        "views/nms_client_view.xml",
        "menu/nms_menu.xml",
    ],
    'license': 'LGPL-3',
    'application': True,

    

}