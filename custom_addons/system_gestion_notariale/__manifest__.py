{
    'name' : 'Gestion Notariale',
    'version' : '1.0',
    'summary': 'Module pour gérer les activités notariales.',
    'author': 'EKBlocks',
    'depends': ['base', 'web', 'mail', 'board', 'project_todo'],

    'assets': {
        'web.assets_backend': [
            # 'system_gestion_notariale/static/src/css/sgn_dossier_style.css',
            'system_gestion_notariale/static/src/css/sgn_service_style.css',
            # 'system_gestion_notariale/static/src/js/combo.js',
            # Include JS if needed for interactivity
        ],
    },

    'data': [   
        # views_section
        "views/sgn_client_view.xml",
        "views/sgn_nationalite_view.xml",
        "views/sgn_propriete_view.xml",
        "views/sgn_categorie_propriete_view.xml",
        "views/sgn_dossier_view.xml",
        "views/sgn_phase_view.xml",
        "views/sgn_settings_view.xml",
        "views/sgn_custom_dashboard_view.xml",
        "views/sgn_dashboard.xml",
        "views/sgn_ville_view.xml",
        "views/sgn_conservation_view.xml",
        "views/sgn_acte_view.xml",
        

        "views/css_loader.xml",

        # security_section
        "security/ir.model.access.csv",
        "security/ir.model.access.xml",
        "security/admin_notaire_groupe.xml",
        "security/assistant_notaire_groupe.xml",

        # menu_section
        "menu/menu.xml",

        

        # sequence_section
        "data/sequence_propriete.xml",
        "data/sequence_dossier.xml",

        #repport
        "repport/dossier/acte_repport.xml",
        "repport/dossier/acte_template.xml",
        "repport/dossier/paiement_repport.xml",
        "repport/dossier/paiement_template.xml",
        "repport/dossier/releve_affaire_repport.xml",
        "repport/dossier/releve_affaire_template.xml",
        "repport/dossier/minute_repport.xml",
        "repport/dossier/minute_template.xml",
     
        
    ],
    
    'license': 'LGPL-3',
    'application': True,


}