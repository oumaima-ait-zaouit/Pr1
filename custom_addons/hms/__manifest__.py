{
    'name': 'Hospital management system',
    'version': '1.0',
    'author': 'EKBlocks',
    'summary': 'Hos App.',
    'depends': [
        'base',
    ],
    'data': [   
        "views/hms_patient_view.xml",
        "views/hms_doctor_view.xml",
        'security/ir.model.access.csv',
        "menus/hms_menu.xml",
    ],
    'license': 'LGPL-3',
    'application': True,
}