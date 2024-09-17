from odoo import fields, models, api, _

class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    coefficient_reevaluation = fields.Float(string=_("Coefficient de Reevaluation"))
    taux_forfaitaire = fields.Float(string=_("Taux forfaitaire"))
    taux_tpi_residence_principale = fields.Float(string=_("Taux TPI Residence principale"))
    taux_tpi_residence_secondaire = fields.Float(string=_("Taux TPI Residence secondaire"))
    taux_tpi_terrain = fields.Float(string=_("Taux TPI Terrain"))
    taux_tpi_fond_commerce = fields.Float(string=_("Taux TPI Fond de Commerce"))
    taux_cotisation_minimale = fields.Float(string=_("Taux Cotisation minimale"))
    taux_tva = fields.Float(string=_("Coefficient de Reevaluation"))
    taux_tpi_sans_profit = fields.Float(string=_("Taux TPI sans profit"))
    taux_tpi_fond_commerce =  fields.Float(string=_("Taux TPI fond Commerce"))
    minimum_fraix_notariale = fields.Float(string=_("Minimum des Fraix Notariales"))
    prix_vente_minimal_pour_honoraires_fixes = fields.Float(string=_("Prix de vente minimale"))
    taux_concervation = fields.Float(string=_("Taux de Concervation Fonciere"))


    def set_values(self):
        super(Settings, self).set_values()
        self.env['ir.config_parameter'].set_param('module.coefficient_reevaluation', self.coefficient_reevaluation)
        self.env['ir.config_parameter'].set_param('module.taux_forfaitaire', self.taux_forfaitaire)
        self.env['ir.config_parameter'].set_param('module.taux_tpi_residence_principale', self.taux_tpi_residence_principale)
        self.env['ir.config_parameter'].set_param('module.taux_tpi_residence_secondaire', self.taux_tpi_residence_secondaire)
        self.env['ir.config_parameter'].set_param('module.taux_tpi_terrain', self.taux_tpi_terrain)
        self.env['ir.config_parameter'].set_param('module.taux_tpi_fond_commerce', self.taux_tpi_fond_commerce)
        self.env['ir.config_parameter'].set_param('module.taux_cotisation_minimale', self.taux_cotisation_minimale)
        self.env['ir.config_parameter'].set_param('module.taux_tva', self.taux_tva)
        self.env['ir.config_parameter'].set_param('module.minimum_fraix_notariale', self.minimum_fraix_notariale)
        self.env['ir.config_parameter'].set_param('module.prix_vente_minimal_pour_honoraires_fixes', self.prix_vente_minimal_pour_honoraires_fixes)
        self.env['ir.config_parameter'].set_param('module.taux_concervation', self.taux_concervation)
        

    @api.model
    def get_values(self):
        res = super(Settings, self).get_values()
        res.update(
            coefficient_reevaluation=float(self.env['ir.config_parameter'].sudo().get_param('module.coefficient_reevaluation', default=0.0)),
            taux_forfaitaire=float(self.env['ir.config_parameter'].get_param('module.taux_forfaitaire', default=15.0)),
            taux_tpi_residence_principale=float(self.env['ir.config_parameter'].get_param('module.taux_tpi_residence_principale', default=5.0)),
            taux_tpi_residence_secondaire=float(self.env['ir.config_parameter'].get_param('module.taux_tpi_residence_secondaire', default=20.0)),
            taux_tpi_terrain=float(self.env['ir.config_parameter'].get_param('module.taux_tpi_terrain', default=5.0)),
            taux_tpi_fond_commerce=float(self.env['ir.config_parameter'].get_param('module.taux_tpi_fond_commerce', default=7.0)),
            taux_cotisation_minimale=float(self.env['ir.config_parameter'].get_param('module.taux_cotisation_minimale', default=3.0)),
            taux_tva=float(self.env['ir.config_parameter'].get_param('module.taux_tva', default=0.0)),
            minimum_fraix_notariale=float(self.env['ir.config_parameter'].get_param('module.minimum_fraix_notariale', default=0.0)),
            prix_vente_minimal_pour_honoraires_fixes=float(self.env['ir.config_parameter'].get_param('module.prix_vente_minimal_pour_honoraires_fixes', default=0.0)),
            taux_concervation=float(self.env['ir.config_parameter'].get_param('module.taux_concervation', default=0.0)),
            
        )
        return res