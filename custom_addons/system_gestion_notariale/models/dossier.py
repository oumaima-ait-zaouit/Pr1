from odoo import models,fields, api, _
from datetime import *
from odoo.exceptions import ValidationError
# import pytz

class Dossier(models.Model):
    _name = 'sgn.dossier'
    _inherit = 'mail.thread'

    name = fields.Char(string="Nombre", readonly=True, copy=False, default=lambda self: _('New'))
    # active = fields.Boolean(string='Active', default=True)
    statut = fields.Selection([
        ('encoure', 'En cours'),
        ('terminer', 'Terminé'),
        ('archive', 'Archivé'),
        ('annule', 'Annulé')
    ], string=_("Statut de dossier"), default="encoure", tracking=True)
    date_termination = fields.Date(string=_("Date de Termination"), readonly=True, tracking=True)
    date_annulation = fields.Date(string=_("Date d'annulation"), readonly=True, tracking=True)
    prix_vente = fields.Float(string=_("Prix de vente"), tracking=True, required=True)
    service = fields.Selection (
        [
            ('vente', 'Vente'),
            ('donation', 'Donation'),
        ],
        string=("Service"), tracking=True, required=True)
    langue_acte = fields.Selection(
        [
            ('arabe', 'Arabe'),
            ('francaise', 'Française'),   
        ],
        string="Langue", tracking=True, required=True)

    notaire_responsabilite_tpi = fields.Boolean(string=_("Est ce que le notaire est responsable sur la declaration de la TPI ?"), default=False, tracking=True)
    acheteur_id = fields.Many2one('res.partner', string=_("Acheteur"), tracking=True, required=True)
    acheteur_identifiant = fields.Char(string="Identifiant Principal", compute="_compute_acheteur_identifiant", store=True, tracking=True)
    acheteur_type_identifiant = fields.Char(string="Type de Pièce d'Identité", compute="_compute_acheteur_identifiant", store=True, tracking=True)
    acheteur_nationalite_ids = fields.Many2one(related='acheteur_id.nationalite_ids', string="Nationalité", readonl=True, tracking=True)

    vendeur_identifiant = fields.Char(string="Identifiant Principal", compute="_compute_vendeur_identifiant", store=True, tracking=True)
    vendeur_type_identifiant = fields.Char(string="Type de Pièce d'Identité", compute="_compute_vendeur_identifiant", store=True, tracking=True)
    vendeur_nationalite_ids = fields.Many2one(related='vendeur_id.nationalite_ids', string="Nationalité", readonly=True, tracking=True)
    vendeur_id = fields.Many2one('res.partner', string=_("Vendeur"), tracking=True, required=True)

    relation_acheteur_vendeur = fields.Selection (
        [
            ('aucun', 'Aucune'),
            ('pere', 'Relation Parentale Directe'),
            ('fils', "Relation Directe d'Enfant"),
            ('frere', 'Relation Fraternelle'),
        ],
        string=("Relation Acheteur/Vendeur"), tracking=True, required=True)

    description = fields.Text(string=_("Description"), tracking=True)
    
    propriete_id =fields.Many2one('sgn.propriete', string=_("Propriete"), ondelete='restrict', unique=True, tracking=True, required=True)
    propriete_type = fields.Selection(related='propriete_id.type_propriete', string="Type", readonly=True, tracking=True)
    propriete_conservation = fields.Many2one(related='propriete_id.conservation_fonciere_id', string="Conservation Fiscale", readonly=True, tracking=True)
    propriete_categorie = fields.Many2one(related='propriete_id.categorie_propriete', string="Categorie", readonly=True, tracking=True)
    phase_id = fields.Many2one('sgn.phase', string=_("Phases"), compute="_compute_phase_id", tracking=True)
    propriete_residence_statut = fields.Selection(related='propriete_id.statut_residence', string="Classification", readonly=True, tracking=True)
    propriete_terrain_statut = fields.Selection(related='propriete_id.statut_terrain', string="Classification", readonly=True, tracking=True)
    # phase_id = fields.Many2one('sgn.phase', string=_("Phases"))
    historique_phase_ids = fields.One2many("sgn.historique.phase", inverse_name="dossier_id", string=_("Historique de phase"), tracking=True) 
    historique_paiement_ids = fields.One2many("sgn.paiement", inverse_name="dossier_id", string=_("Paiement"), tracking=True) 
    payment_ids = fields.One2many("sgn.historique.phase", inverse_name="dossier_id", tracking=True) 
    piece_jointe_ids = fields.One2many('sgn.piece_jointe_dossier', inverse_name='dossier_id', string=_("Pieces Jointes"), tracking=True)

    phase_statut = fields.Selection(
        [
            ('encoure', 'En cours'),
            ('prete_aux_payment', 'Prête aux paiement'),
            ('paye', 'Payée'),
            ('termine', 'Terminée')
        ],
        string=_("Statut de la phase"), tracking=True)
    # depot_cdg = fields.Boolean(string=_("Deposé à la CDG ?"))
    depos_cdg = fields.Boolean(string=_("Deposé à la CDG ?"), default=False, tracking=True)      
    date_depos = fields.Date(string=_("Date de Depos"), tracking=True)
    paiement_by_notaire = fields.Selection(
        [
            ('devant','Devant le notaire'),
            ('entre','entre les parties prenants'),
        ],
        string=_("Montant a été payé"), tracking=True, required=True)

    
    honoraires_notariale = fields.Float(string="Honoraire notariales", compute="_compute_notary_fees", tracking=True)
    pourcentage_honoraire_notariale = fields.Float(string="Pourcentage des Fraix notariales", tracking=True)

    # total = fields.Float(string="Total", compute="_compute_total")
    total_ht = fields.Float(string="Total", compute="_compute_total_ht", readonly=True, tracking=True)
    total_unpaid = fields.Float(string="Total des Impayé", compute="_compute_total_unpaid", tracking=True)
    total_ttc = fields.Float(string="Total", readonly=True, compute="_compute_total_ttc", tracking=True)
    total_paied = fields.Float(string="Total de Paiement", compute="_compute_total_paied", tracking=True)
    montant_tva = fields.Float(string="Montant TVA", compute="_compute_montant_tva", tracking=True)
    pourcentage_tva = fields.Float(string="Taux TVA", compute="_compute_montant_tva", tracking=True)
    montant_concervation_fonciere = fields.Float(string="Montant de la Concervation Fonciere", compute="_compute_montant_concervation", tracking=True)
    pourcentage_concervation_fonciere = fields.Float(string="Pourcentage de la Concervation Fonciere", compute="_compute_pourcentage_concervation_from_settings", tracking=True)
    montant_registration = fields.Float(string="Montant de la Registration", compute="_compute_montant_registration", tracking=True)
    pourcentage_registration = fields.Float(string="Pourcentage de Registration", related='propriete_id.categorie_propriete.taux_registration', tracking=True)

    benefice = fields.Float(string=_("Benefice Immobilière"), compute='_compute_benefice', store=True, readonly=True, tracking=True)
    tpi_pourcentage = fields.Float(string=_("Taux TPI"), compute="_compute_pourcentage_tpi", store=True, readonly=True, tracking=True)
    tpi_montant = fields.Float(string="Montant TPI", compute="_compute_tpi_amount", store=True, readonly=True, tracking=True)
    cotisation_minimale = fields.Float(string=_("Cotisation minimale"), compute="_compute_cotisation_minimale", tracking=True)
    montant_a_payer_tpi = fields.Float(string=_("Montant de la TPI"), compute="_compute_montant_a_payer_tpi", tracking=True)
    montant_a_payer_tpi1 = fields.Float(string=_("Montant de la TPI"), default=0.0, tracking=True)
    fraix_dossier = fields.Float(string=_("Frais de dossier (timbres, copies…)"), tracking=True)
    

    @api.depends('acheteur_id')
    def _compute_acheteur_identifiant(self):
        for dossier in self:
            primary_identity_doc = self.env['sgn.piece_jointe_client'].search([
                ('client_id', '=', dossier.acheteur_id.id),
                ('piece_identite_principale', '=', True)
            ], limit=1)
            if primary_identity_doc:
                dossier.acheteur_identifiant = primary_identity_doc.identifiant
                dossier.acheteur_type_identifiant = dict(primary_identity_doc._fields['type_pj'].selection).get(primary_identity_doc.type_pj)
            else:
                dossier.acheteur_identifiant = ""
                dossier.acheteur_type_identifiant = ""

    @api.depends('vendeur_id')
    def _compute_vendeur_identifiant(self):
        for dossier in self:
            primary_identity_doc = self.env['sgn.piece_jointe_client'].search([
                ('client_id', '=', dossier.vendeur_id.id),
                ('piece_identite_principale', '=', True)
            ], limit=1)
            if primary_identity_doc:
                dossier.vendeur_identifiant = primary_identity_doc.identifiant
                dossier.vendeur_type_identifiant = dict(primary_identity_doc._fields['type_pj'].selection).get(primary_identity_doc.type_pj)
            else:
                dossier.vendeur_identifiant = ""
                dossier.vendeur_type_identifiant = ""

    @api.depends("historique_paiement_ids")
    def _compute_total_paied(self):
        for rec in self:
            rec.total_paied = sum([p.montant for p in rec.historique_paiement_ids])

    
    @api.depends("honoraires_notariale", "prix_vente", "pourcentage_honoraire_notariale")
    def _compute_notary_fees(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            minimum_fraix_notariale = float(param_env.get_param('module.minimum_fraix_notariale', default=0.0))
            prix_vente_minimal_pour_honoraires_fixes = float(param_env.get_param('module.prix_vente_minimal_pour_honoraires_fixes', default=0.0))

            if record.prix_vente <= prix_vente_minimal_pour_honoraires_fixes:
                record.honoraires_notariale = minimum_fraix_notariale
            elif record.prix_vente > prix_vente_minimal_pour_honoraires_fixes:
                    record.honoraires_notariale = record.pourcentage_honoraire_notariale * (record.prix_vente / 100)


    @api.depends("honoraires_notariale")
    def _compute_montant_tva(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            taux_tva = float(param_env.get_param('module.taux_tva', default=0.0))
            record.montant_tva = record.honoraires_notariale * (taux_tva / 100)
            record.pourcentage_tva = taux_tva

    

    @api.depends("prix_vente")
    def _compute_montant_concervation(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            taux_concervation = float(param_env.get_param('module.taux_concervation', default=0.0))
            record.montant_concervation_fonciere = record.prix_vente * (taux_concervation / 100)


    @api.depends("montant_a_payer_tpi", 'honoraires_notariale', 'historique_phase_ids.montant', 'fraix_dossier', 'montant_concervation_fonciere')
    def _compute_total_ht(self):
        for rec in self:
            total_amount_phases = sum([phase.montant for phase in rec.historique_phase_ids])
            rec.total_ht = total_amount_phases + rec.montant_a_payer_tpi + rec.honoraires_notariale + rec.fraix_dossier + rec.montant_concervation_fonciere


    @api.depends("montant_a_payer_tpi", 'honoraires_notariale', 'historique_phase_ids.montant', 'fraix_dossier', 'montant_tva', 'montant_concervation_fonciere')
    def _compute_total_ttc(self):
        for rec in self:
            total_amount_phases = sum([phase.montant for phase in rec.historique_phase_ids])
            rec.total_ttc = total_amount_phases + rec.montant_a_payer_tpi + rec.honoraires_notariale + rec.fraix_dossier + rec.montant_tva + rec.montant_concervation_fonciere

    
    
    @api.depends("total_ttc", "total_paied")
    def _compute_total_unpaid(self):
        for rec in self:
            rec.total_unpaid = rec.total_ttc - rec.total_paied


    @api.depends("propriete_id", "prix_vente")
    def _compute_montant_registration(self):
        for record in self:
            taux_registration = record.propriete_id.categorie_propriete.taux_registration
            record.montant_registration = record.prix_vente * (taux_registration / 100)


    @api.depends("historique_phase_ids.phase_id")
    def _compute_phase_id(self):
        for rec in self:
            historic_phases = rec.env["sgn.historique.phase"].search([('dossier_id', '=', rec.id)], order="create_date desc")
            last_phase = historic_phases[0] if historic_phases else False
            last_phase =  last_phase.phase_id if last_phase else False
            rec.phase_id = last_phase



    @api.depends('propriete_id.prix_revient_actualise', 'prix_vente')
    def _compute_benefice(self):
        for record in self:
            record.benefice = record.prix_vente - record.propriete_id.prix_revient_actualise


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sgn.dossier.nombre') or _('New')
        return super(Dossier, self).create(vals)

    def termine_phase_action(self):
        for rec in self:
            rec.phase_statut = 'termine'
        
    def action_print_payment_list(self):
        return self.env.ref('system_gestion_notariale.report_paiement_list_action').report_action(self)

    def action_print_acte(self):
        return self.env.ref('system_gestion_notariale.report_acte_print_action').report_action(self)

    def action_print_minute(self):
        return self.env.ref('system_gestion_notariale.report_minute_print_action').report_action(self)

    def action_print_releve_affaire(self):
        return self.env.ref('system_gestion_notariale.releve_affaire_list_action').report_action(self)


    

    @api.depends('prix_vente')
    def _compute_pourcentage_concervation_from_settings(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            taux_concervation = float(param_env.get_param('module.taux_concervation'))
            record.pourcentage_concervation_fonciere = taux_concervation

    @api.depends('prix_vente')
    def _compute_pourcentage_registration_from_settings(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            taux_concervation = float(param_env.get_param('module.taux_concervation'))
            record.pourcentage_concervation_fonciere = taux_concervation


    is_exempt = fields.Boolean(default=False, compute='_compute_pourcentage_tpi', store=True, string="Exonération ?")

    @api.onchange('propriete_id.statut_residence', 'propriete_id.type_propriete', 'prix_vente', 'relation_acheteur_vendeur', 'service', 'propriete_id.date_aquisition', 'is_exempt')
    @api.depends('propriete_id.statut_residence', 'propriete_id.type_propriete', 'prix_vente', 'relation_acheteur_vendeur', 'service', 'propriete_id.date_aquisition', 'is_exempt')
    def _compute_pourcentage_tpi(self):
        for record in self:
            param_env = self.env['ir.config_parameter'].sudo()

            taux_tpi_residence_secondaire = float(param_env.get_param('module.taux_tpi_residence_secondaire', default=0.0))
            taux_tpi_terrain = float(param_env.get_param('module.taux_tpi_terrain', default=0.0))
            taux_tpi_fond_commerce = float(param_env.get_param('module.taux_tpi_fond_commerce', default=0.0))
            taux_tpi_residence_principale = float(param_env.get_param('module.taux_tpi_residence_principale', default=0.0))

            # Check exemption conditions
            is_exempt = False
            record.is_exempt = False

            # 1. Check if prix_vente <= 140000 dh
            if record.service == 'vente' and record.prix_vente and record.prix_vente <= 140000:
                is_exempt = True
                record.is_exempt = True


            # 2. Check if relation_acheteur_vendeur != 'aucun'
            if record.relation_acheteur_vendeur and record.relation_acheteur_vendeur != 'aucun':
                is_exempt = True
                record.is_exempt = True


            # 3. Check if service = 'donation' and prix_vente > 4,000,000 dh
            if record.service == 'donation' and record.prix_vente and record.prix_vente < 4000000:
                is_exempt = True
                record.is_exempt = True

            # 4. Check if statut_residence = 'principale' and date difference >= 5 years
            if record.propriete_id.statut_residence == 'principale' and record.propriete_id.date_aquisition:
                date_acquisition = record.propriete_id.date_aquisition
                today = date.today()
                # Check if 5 years (or more) have passed since the acquisition date
                if (today - date_acquisition).days > 5 * 365:
                    record.is_exempt = True
                    is_exempt = True

            if is_exempt:
                record.tpi_pourcentage = 0.0
                record.cotisation_minimale = 0.0
            else:
                # Calculate TPI percentage based on property type
                if record.propriete_id.type_propriete == 'residence':
                    if record.propriete_id.statut_residence == 'principale':
                        record.tpi_pourcentage = taux_tpi_residence_principale
                    elif record.propriete_id.statut_residence == 'secondaire':
                        record.tpi_pourcentage = taux_tpi_residence_secondaire
                    else:
                        record.tpi_pourcentage = 0.0
                elif record.propriete_id.type_propriete == 'terrain':
                    record.tpi_pourcentage = taux_tpi_terrain
                elif record.propriete_id.type_propriete == 'fonds_de_commerce':
                    record.tpi_pourcentage = taux_tpi_fond_commerce
                else:
                    record.tpi_pourcentage = 0.0


    @api.onchange('tpi_pourcentage', 'benefice', 'is_exempt')
    @api.depends('tpi_pourcentage', 'benefice', 'is_exempt')
    def _compute_tpi_amount(self):
        for record in self:
            if record.is_exempt:
                record.tpi_montant = 0
            else:
                record.tpi_montant = record.benefice * (record.tpi_pourcentage / 100)


    @api.onchange('prix_vente', 'is_exempt')
    @api.depends('prix_vente', 'is_exempt')
    def _compute_cotisation_minimale(self):
        for record in self:
            if record.is_exempt:
                record.cotisation_minimale = 0
            else:
                param_env = self.env['ir.config_parameter'].sudo()

                taux_cotisation_minimale = float(param_env.get_param('module.taux_cotisation_minimale', default=0.0))
                record.cotisation_minimale = record.prix_vente * (taux_cotisation_minimale / 100)


    @api.depends('tpi_montant', 'cotisation_minimale', 'is_exempt')
    def _compute_montant_a_payer_tpi(self):
        for record in self:
            if record.is_exempt:
                record.montant_a_payer_tpi = 0
            else:
                record.montant_a_payer_tpi = max(record.tpi_montant, record.cotisation_minimale)


    @api.constrains('propriete_id')
    def _check_unique_propriete(self):
        for record in self:
            if record.propriete_id:
                # Search for any existing dossier with the same property and a status of "en cours" or "terminé"
                existing_dossiers = self.search([
                    ('propriete_id', '=', record.propriete_id.id),
                    ('id', '!=', record.id),
                    ('statut', 'in', ['encoure', 'termine'])  # Only consider "en cours" or "terminé" status
                ])
                
                if existing_dossiers:
                    raise ValidationError("La propriété sélectionnée est déjà associée à un dossier.")


    @api.constrains('historique_phase_ids')
    def _check_pieces_jointes_status(self):
        for dossier in self:
            # Retrieve the last phase added to this dossier based on ID (assuming higher ID is the latest)
            last_phase = dossier.historique_phase_ids.sorted('id', reverse=True)[:1]
            
            # Check if the last phase has a `date_fin` set
            if last_phase and last_phase.date_fin:
                # Fetch all related pieces jointes for the dossier
                all_pieces_jointes = (
                    dossier.piece_jointe_ids 
                    # dossier.mapped('piece_jointe_propriete_ids.piece_jointe_propriete_ids') +
                    # dossier.mapped('piece_jointe_client_ids.piece_jointe_client_ids')
                )
                
                # Ensure all pieces jointes are validated
                for piece_jointe in all_pieces_jointes:
                    if piece_jointe.statut != 'valide':
                        raise ValidationError("Toutes les pièces jointes doivent être validées avant de passer à une nouvelle phase.")


    # @api.constrains('historique_phase_ids')
    # def check_phase_transition(self):
    #     for dossier in self:
    #         # Fetch the most recently added historique_phase for this dossier
    #         last_historique_phase = self.env['sgn.historique.phase'].search(
    #             [('dossier_id', '=', dossier.id)],
    #             order='id desc',  # Assuming 'id' can be used to fetch the latest record
    #             limit=1
    #         )

    #         # Check if the last historique_phase has a date_fin
    #         if last_historique_phase and not last_historique_phase.date_fin:
    #             # Check all related pieces jointes for the dossier
    #             related_piece_jointe_dossier = self.env['sgn.piece_jointe_dossier'].search([('dossier_id', '=', dossier.id)])
    #             if any(piece_jointe.statut == 'encours' for piece_jointe in related_piece_jointe_dossier):
    #                 raise ValidationError("Tous les 'pieces jointes' du dossier doivent être validés avant de pouvoir définir la date de fin de la phase.")
                
                # # Check all related pieces jointes for propriete
                # related_piece_jointe_propriete = self.env['sgn.piece_jointe_propriete'].search([('dossier_id', '=', dossier.id)])
                # if any(piece_jointe.state == 'en_cours' for piece_jointe in related_piece_jointe_propriete):
                #     raise ValidationError("Tous les 'pieces jointes' de la propriété doivent être validés avant de pouvoir définir la date de fin de la phase.")
                
                # # Check all related pieces jointes for client
                # related_piece_jointe_client = self.env['sgn.piece_jointe_client'].search([('dossier_id', '=', dossier.id)])
                # if any(piece_jointe.state == 'en_cours' for piece_jointe in related_piece_jointe_client):
                #     raise ValidationError("Tous les 'pieces jointes' du client doivent être validés avant de pouvoir définir la date de fin de la phase.")


    # @api.onchange('relation_acheteur_vendeur')
    # def _onchange_relation_acheteur_vendeur(self):
    #         """Handle the change of relation between buyer and seller."""
    #         if self.relation_acheteur_vendeur and self.relation_acheteur_vendeur != 'aucun':
    #             # Set TPI values to zero
    #             self.benefice = 0
    #             self.tpi_pourcentage = 0
    #             self.tpi_montant = 0
    #             self.montant_a_payer_tpi = 0
    #             self.cotisation_minimale = 0
                
    #             # Display warning message
    #             return {
    #                 'warning': {
    #                     'title': _("Exonération de la TPI"),
    #                     'message': _("La TPI est exonérée car la relation entre le vendeur et l'acheteur est: %s. ") % dict(self._fields['relation_acheteur_vendeur'].selection).get(self.relation_acheteur_vendeur),
    #                     'type': 'notification'
    #                 }
    #             }

    # @api.onchange('prix_vente')
    # def _onchange_prix_vente(self):
    #         """Handle the change of relation between buyer and seller."""
    #         if self.benefice < 140000:
    #             # Set TPI values to zero
    #             self.benefice = 0
    #             self.tpi_pourcentage = 0
    #             self.tpi_montant = 0
    #             self.montant_a_payer_tpi = 0
    #             self.cotisation_minimale = 0
                
    #             # Display warning message
    #             return {
    #                 'warning': {
    #                     'title': _("Exonération de la TPI"),
    #                     'message': _("La TPI est exonérée car le prix de vente est inférieur à 140 000 DH"),
    #                     'type': 'notification'
    #                 }
    #             }


    # def _update_phase_statut(self):
    # # Check if phase_id is set before updating the status
    #     if not self.phase_id:
    #         self.phase_statut = '-'
    #     else:
    #         # Default status
    #         self.phase_statut = 'encoure'

    #         # Update status based on conditions
    #         if self.date_fin:
    #             self.phase_statut = 'termine'
    #         elif self.is_paid:
    #             self.phase_statut = 'paye'
    #         elif self.montant_valide:
    #             self.phase_statut = 'prete_aux_payment'
    #         elif self.date_debut:
    #             self.phase_statut = 'encoure'
