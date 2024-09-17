from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class Propriete(models.Model):
    _name = 'sgn.propriete'
    _inherit = 'mail.thread'

    name = fields.Char(string="Nombre", readonly=True, copy=False, default=lambda self: _('New'))
    surface = fields.Float(string="Surface", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    date_aquisition = fields.Date(string="Date d'aquisition", required=True, tracking=True)
    prix_aquisition_initial = fields.Float(string="Prix d'aquisition", tracking=True)
    prix_revient_actualise = fields.Float(string='Prix de revien actualisé', compute='_compute_prix_revient_actualise', store=True, readonly=True)


    depenses = fields.Float(string=_("Montant de depenses"), tracking=True)
    interets = fields.Boolean(string=_("Y a t-il des interets ?"), defaulte=False, tracking=True)
    mantants_interets = fields.Float(string=_("Mantant d'interets"), tracking=True)
    adresse = fields.Char(string="Adresse", required=True)
    statut_residence = fields.Selection([
        ('principale', 'Principale'),
        ('secondaire', 'Secondaire'),
    ], string=_("Classification Residence"), required=True, tracking=True)
    statut_terrain = fields.Selection([
        ('urbain', 'Urbain'),
        ('rural', 'Rural'),
    ], string=_("Classification Terrain"), required=True, tracking=True)
    type_propriete = fields.Selection([
        ('residence', 'Residence'),
        ('terrain', 'Terrain'),
        ('fond_de_commerce', 'Fond de Commerce')
    ], required=True, tracking=True)

    dossier_id = fields.Many2one('sgn.dossier', string=_("Dossier"), ondelete='cascade', unique=True)

    # conservation_fonciere = fields.Selection(
    # [
    #     ('casablanca', 'Casablanca'),
    #     ('rabat', 'Rabat'),
    #     ('marrakech', 'Marrakech'),
    #     ('tanger', 'Tanger'),
    #     ('fes', 'Fès'),
    #     ('meknes', 'Meknès'),
    #     ('oujda', 'Oujda'),
    #     ('agadir', 'Agadir'),
    #     ('tetouan', 'Tétouan'),
    #     ('safi', 'Safi'),
    #     ('kenitra', 'Kénitra'),
    #     ('nador', 'Nador'),
    #     ('laayoune', 'Laâyoune'),
    #     ('mohammedia', 'Mohammedia'),
    #     ('beni_mellal', 'Beni Mellal'),
    #     ('temara', 'Témara'),
    #     ('khouribga', 'Khouribga'),
    #     ('el_jadida', 'El Jadida'),
    #     ('ouarzazate', 'Ouarzazate'),
    #     ('taza', 'Taza'),
    # ],
    # string="Conservation Foncière")
    conservation_fonciere_id = fields.Many2one('sgn.conservation',string="Conservation Foncière", tracking=True, required=True)
    categorie_propriete = fields.Many2one('sgn.categorie_propriete', string=_("Categorie"), tracking=True, required=True)
    owner_id = fields.Many2many('res.partner','propriete_ids', string=_("Proprietaires"), tracking=True, required=True)
    piece_jointe_ids = fields.One2many('sgn.piece_jointe_propriete', inverse_name='propriete_id', string=_("Pieces Jointes"), tracking=True)


    # @api.depends('owner_id')
    # def _compute_owner_identifiant(self):
    #     for propriete in self:
    #         primary_identity_prop = self.env['sgn.piece_jointe_client'].search([
    #             ('client_id', '=', propriete.owner_id.id),
    #             ('piece_identite_principale', '=', True)
    #         ], limit=1)
    #         if primary_identity_prop:
    #             propriete.owner_identite = primary_identity_prop.identifiant
    #             propriete.owner_type_piece_identite = dict(primary_identity_prop._fields['name'].selection).get(primary_identity_prop.name)
    #         else:
    #             propriete.owner_identite = ""
    #             propriete.owner_type_piece_identite = ""


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sgn.propriete.nombre') or _('New')
        return super(Propriete, self).create(vals)


    @api.constrains('piece_jointe_ids')
    def _check_piece_titre(self):
        for propriete in self:
            has_titre = any(piece.name == 'titre' for piece in propriete.piece_jointe_ids)
            if not has_titre:
                raise ValidationError(_("Vous devez ajouter le titre de votre propriété."))


    @api.constrains('piece_jointe_ids')
    def _check_piece_certificat_propriete(self):
        for propriete in self:
            has_certificat_propriete = any(piece.name == 'certificat' for piece in propriete.piece_jointe_ids)
            if not has_certificat_propriete:
                raise ValidationError(_("Vous devez ajouter le certificat de propriété."))


    @api.constrains('piece_jointe_ids', 'type_propriete', 'categorie_propriete', 'owner_id')
    def _check_piece_vna_propriete(self):
        for propriete in self:
            if propriete.type_propriete == 'terrain' and propriete.categorie_propriete:
                if propriete.categorie_propriete.name == 'Terrain Nu' and propriete.owner_id:
                    if propriete.owner_id.nationalite_ids:      
                        for nationality in propriete.owner_id.nationalite_ids:
                            if not nationality.can_buy:
                                has_vna_propriete = any(piece.name == 'vna' for piece in propriete.piece_jointe_ids)
                                if not has_vna_propriete:
                                    raise ValidationError(_("Vous devez ajouter l'attestation de VNA de propriété."))


    @api.constrains('type_propriete', 'categorie_propriete', 'owner_id')
    def _check_foreign_ownership_agricultural_land(self):
        """Check if a foreign owner is trying to purchase agricultural land without a VNA certificate."""
        for record in self:
            if record.type_propriete == 'terrain' and record.categorie_propriete:
                if record.categorie_propriete.name == 'Terrain Agricole':
                    if record.owner_id and record.owner_id.nationalite_ids:
                        # Check if any nationality prohibits buying agricultural land
                        for nationality in record.owner_id.nationalite_ids:
                            if not nationality.can_buy:
                                # Raise a validation error if the owner cannot buy agricultural land
                                raise ValidationError(
                                    _("Ce client ne peut pas posséder un terrain agricole car il est de nationalité %s.") % nationality.name
                                )


    @api.depends('prix_aquisition_initial', 'depenses', 'mantants_interets')
    def _compute_prix_revient_actualise(self):
        for record in self:
            coefficient_reevaluation = float(self.env['ir.config_parameter'].get_param('module.coefficient_reevaluation'))
            taux_forfaitaire = float(self.env['ir.config_parameter'].get_param('module.taux_forfaitaire', default=15))

            valeur_forfaitaire = record.prix_aquisition_initial * (taux_forfaitaire / 100)       
            prix_revient_total = record.prix_aquisition_initial + valeur_forfaitaire + record.depenses + record.mantants_interets
            record.prix_revient_actualise = prix_revient_total * coefficient_reevaluation


    





    
    
   




    

