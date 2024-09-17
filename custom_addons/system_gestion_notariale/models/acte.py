from odoo import models, fields, api, _

class Acte(models.Model):
    _name = 'sgn.acte'


    name = fields.Char(string="Nombre", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    create_date  = fields.Datetime(string="date de creation")
    langue =  fields.Selection(
    [
        ('arabic', 'Arabic'),
        ('english', 'English'),
        ('french', 'French'),
    ],
    string="Langue d'acte")

    # client_ids = fields.One2many('res.partner','acte_id', string="Clients", readonly=True)
    # nationalite_ids = fields.One2many ('res.partner','acte_id', string="Nationalite", readonly=True)
    # propriete_id = fields.Many2one('sgn.propriete', string="Propriete", ondelete='cascade', unique=True, readonly=True)
    # dossier_id = fields.Many2one('sgn.dossier', string="Dossier", ondelete='cascade', unique=True)



    # # Fields from Dossier
    # dossier_name = fields.Char(string="Dossier N°", related='dossier_id.name', store=True, readonly=True)
    # dossier_prix_vente = fields.Float(related='dossier_id.prix_vente', store=True, readonly=True)
    # dossier_service = fields.Selection(related='dossier_id.service', store=True, readonly=True)
    # dossier_tpi = fields.Boolean(related='dossier_id.notaire_responsabilite_tpi', store=True, readonly=True)
    
    # dossier_vendeur = fields.Char(related='dossier_id.vendeur_id.name', store=True, readonly=True)
    # # vendeur_titre = fields.Char(related='dossier_id.vendeur_id.titre', store=True, readonly=True)
    # vendeur_sexe = fields.Selection(related='dossier_id.vendeur_id.sexe', store=True, readonly=True)
    # vendeur_nationalite = fields.Char(related='dossier_id.vendeur_id.nationalite_ids.name', store=True, readonly=True)
    # vendeur_date_naissance = fields.Date(related='dossier_id.vendeur_id.date_naissance', store=True, readonly=True)
    # vendeur_lieu_naissance = fields.Selection(related='dossier_id.vendeur_id.lieu_naissance', store=True, readonly=True)
    # vendeur_piece_jointe = fields.Selection(related='dossier_id.vendeur_id.piece_jointe_ids.type_pj', store=True, readonly=True)
    # vendeur_piece_jointe_identifiant = fields.Char(related='dossier_id.vendeur_id.piece_jointe_ids.identifiant', store=True, readonly=True)
    # vendeur_piece_jointe_date_expiration = fields.Date(related='dossier_id.vendeur_id.piece_jointe_ids.date_expiration', store=True, readonly=True)
    # vendeur_profession = fields.Char(related='dossier_id.vendeur_id.function', store=True, readonly=True)

    # dossier_acheteur = fields.Char(related='dossier_id.acheteur_id.name', store=True, readonly=True)
    # achteur_tittre = fields.Char(related='dossier_id.acheteur_id.titre', store=True, readonly=True)

    # acheteur_lieu_naissance = fields.Selection(related='dossier_id.acheteur_id.lieu_naissance', store=True, readonly=True)
    # prix_aquisition_initiale = fields.Float(related='dossier_id.propriete_id.prix_aquisition_initial')

    


    
    # dossier_vendeur = fields.Char(related='dossier_id.vendeur_ids.name', store=True)
    # dossier_notary_fees = fields.Char(related='dossier_id.notary_fees', store=True)
    # dossier_tpi = fields.Char(related='dossier_id.notaire_responsabilite_tpi', store=True)


    # Fields from Client
    # client_name = fields.Char(string="Client Name", related='dossier_id.client_ids.name', store=True)
    # client_nationality = fields.Char(string="Client Nationality", related='client_ids.nationalite_ids.name', store=True)
    # client_email = fields.Char(string="Client Email", related='client_ids.email', store=True)
    # client_phone = fields.Char(string="Client Phone", related='client_ids.phone', store=True)


    # Fields from Propriete
    # propriete_name = fields.Char(string="Propriete Name", related='propriete_id.name', store=True)
    # propriete_surface = fields.Float(string="Propriete Surface", related='propriete_id.surface', store=True)
    # propriete_adresse = fields.Char(string="Propriete Location", related='propriete_id.adresse', store=True)


    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('sgn.acte.nombre') or _('New')
    #     return super(Acte, self).create(vals)
