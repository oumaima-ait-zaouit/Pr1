from odoo import models, fields, api

class Client(models.Model) :
    
    _inherit = 'res.partner'

    nationnality_ids = fields.Many2many("sgn.nationality", string="Nationalité")
    date_naissance = fields.Date(string=("Date de Naissance"))
    lieu_naissance = fields.Selection (
        [
            ('maroc', 'Maroc'),
            ('france', 'France'),
            ('tunis', 'Tunisie'),
            ('algerie', 'Algérie'),
            ('espagne', 'Espagne'),
            ('italie', 'Italie'),
            ('allemagne', 'Allemagne'),
            ('royaume_uni', 'Royaume-Uni'),
            ('etats_unis', 'États-Unis'),
            ('canada', 'Canada'),
            ('chine', 'Chine'),
            ('japon', 'Japon'),
            ('inde', 'Inde'),
            ('brazil', 'Brésil'),
            ('australie', 'Australie')], 
        string=("Lieu de Naissance"))

    etat_familiale = fields.Selection (
        [
            ('epoux', 'Epoux / Epouse'),
            ('veuf', 'Veuf / Veuve'),
            ('divorce', 'Divorcé / Divorcée'),
            ('celibataire', 'Célibataire')],
        string=("Etat Familiale"))
    nom_partenaire = fields.Char(string=("Nom du Partenaire"))
    profession = fields.Char(string=("Profession"))

    # @api.onchange('etat_familiale')
    # def onchange_etat_familiale(self):
    #     if self.etat_familiale == 'epoux':
    #         self.nom_partenaire = True  # Hide or clear the field when not 'epoux'
    #     else:
    #         self.nom_partenaire = False