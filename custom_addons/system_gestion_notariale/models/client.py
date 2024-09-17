from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Client(models.Model):
    _inherit = ['res.partner']

    nationalite_ids = fields.Many2one("sgn.nationalite", string="Nationalité", tracking=True, required=True)
    date_naissance = fields.Date(string="Date de Naissance", tracking=True, required=True)
    sexe = fields.Selection(
        [
            ('feminin', 'Feminin'),
            ('masculin', 'Masculin'),   
        ],
        string="Sexe", tracking=True, required=True)
    
    date_start = fields.Date(string="Date de debut", tracking=True)
    titre = fields.Char(string="Title", compute="_compute_titre")
    lieu_naissance1 = fields.Many2one('sgn.ville',string="Lieu de Naissance", tracking=True, required=True)
    lieu_naissance = fields.Selection(
        [
            ('nador', 'Nador'),
            ('essaouira', 'Essaouira'),
        ],
        string="Lieu de Naissance", tracking=True, required=True
    )
    etat_familiale = fields.Selection(
        [
            ('epoux', 'Marié / Mariée'),
            ('veuf', 'Veuf / Veuve'),
            ('divorce', 'Divorcé / Divorcée'),
            ('celibataire', 'Célibataire')
        ],
        string="Etat Familiale", tracking=True, required=True
    )
    nom_partenaire = fields.Char(string="Nom du Partenaire", tracking=True)
    date_marriage = fields.Date(string="Date de marriage", tracking=True)
    lieu_marriage1 = fields.Many2one('sgn.ville',string="Lieu de marriage", tracking=True, required=True)
    lieu_marriage = fields.Selection(
        [
            ('nador', 'Nador'),
            ('essaouira', 'Essaouira'),
        ],
        string="Lieu de marriage", tracking=True, required=True
    )
    marriage_musulman = fields.Boolean(string="Marriage selon la loi musulman", default=True, tracking=True)
    combattant  = fields.Boolean(string="Combattant  ou pupilles dela Nation", default=False, tracking=True)
    
    dossier_count = fields.Integer(
        string='Dossiers Count',
        compute='_compute_dossier_count',
        readonly=True,
        tracking=True
    )

    acte_marriage = fields.Boolean(string="Acte de marriage", default=False, tracking=True)


    dossier_a_ids = fields.One2many('sgn.dossier', 'acheteur_id', string="Dossiers", tracking=True)
    dossier_v_ids = fields.One2many('sgn.dossier', 'vendeur_id', string="Dossiers", tracking=True)

    acte_sous_article49 = fields.Boolean(string="Acte est soumis a l'article 49 de code de la famille ?", default=False, tracking=True)
    propriete_ids = fields.Many2many('sgn.propriete', string='Proprietes', tracking=True)
    piece_jointe_ids = fields.One2many('sgn.piece_jointe_client', inverse_name='client_id', string="Pieces Jointes")

    @api.depends('dossier_a_ids', 'dossier_v_ids')
    def _compute_dossier_count(self):
        for record in self:
            record.dossier_count = len(record.dossier_a_ids) + len(record.dossier_v_ids)

    @api.onchange('etat_familiale')
    def onchange_etat_familiale(self):
        if self.etat_familiale == 'epoux':
            self.nom_partenaire = ''
        else:
            self.nom_partenaire = False

    @api.depends('sexe', 'etat_familiale')
    def _compute_titre(self):
        for record in self:
            if record.sexe == 'masculin':
                record.titre = "Monsieur"
            elif record.sexe == 'feminin':
                if record.etat_familiale == 'celibataire':
                    record.titre = "Mademoiselle"
                else:
                    record.titre = "Madame"


    
    @api.constrains('piece_jointe_ids')
    def _check_piece_identite_principale(self):
        for client in self:
            has_main_id = any(piece.piece_identite_principale for piece in client.piece_jointe_ids)
            if not has_main_id:
                raise ValidationError(_("Vous devez ajouter une pièce d'identité principale (CIN, passeport, etc.)."))


    @api.constrains('combattant', 'piece_jointe_ids')
    def _check_combattant_document(self):
        for client in self:
            if client.combattant:
                has_combattant_doc = any(piece.type_pj == 'combattant' for piece in client.piece_jointe_ids)
                if not has_combattant_doc:
                    raise ValidationError(_("Vous devez ajouter un document de type 'Carte du Combattant / Carte de pupille de la Nation' car le champ 'Combattant' est coché."))


    @api.constrains('etat_familiale', 'piece_jointe_ids')
    def _check_divorce_document(self):
        for client in self:
            if client.etat_familiale == 'divorce':
                has_divorce_doc = any(piece.type_pj == 'jugement' for piece in client.piece_jointe_ids)
                if not has_divorce_doc:
                    raise ValidationError(_("Vous devez ajouter le Jugement de Divorce Définitif car le client est en situation familiale de 'Divorcé / Divorcée'."))


    @api.constrains('acte_marriage', 'piece_jointe_ids')
    def _check_acte_marriage_document(self):
        for client in self:
            if client.etat_familiale == 'epoux' and client.acte_marriage:
                has_acte_marriage_doc = any(piece.type_pj == 'acte' for piece in client.piece_jointe_ids)
                if not has_acte_marriage_doc:
                    raise ValidationError(_("Vous devez ajouter un document de type 'Acte de marriage' car le champ 'Acte de marriage' est coché."))


    
                
    
