from odoo import fields, models, api, _

class HistoriquePhase(models.Model):
    _name = 'sgn.historique.phase'
    _order = 'sequence asc'
    _inherit = 'mail.thread'

    # name = fields.Char(string=_("Nom"))
    date_debut = fields.Date(string="Date début", tracking=True)
    date_fin = fields.Date(string="Date fin", tracking=True)
    # amount = fields.Monetary(string="Montant")
    montant = fields.Float(string="Montant", compute="_compute_montant", store=True, readonly=False, tracking=True)
    montant_valide = fields.Boolean(string=_("Montant Validé"), default=False, tracking=True)
    phase_id = fields.Many2one('sgn.phase', string=_("Phase"), tracking=True)
    sequence = fields.Integer(compute="_compute_sequence", store=True, tracking=True)
    dossier_id = fields.Many2one('sgn.dossier', string=_("Dossier"), tracking=True)
    # currency_id = fields.Many2one('res.currency', string='Devise', tracking=True, default=lambda self: self.env.ref('base.MAD'))
    phase_is_paid = fields.Boolean("is_paid", compute="_compute_is_paid", tracking=True)
    is_paid = fields.Boolean(string=_("Paiement effectué à la direction ?"), tracking=True)
    phase_selection_ids = fields.Json(compute="_compute_phase_selection", tracking=True)


    
    @api.depends('phase_selection_ids', 'dossier_id')
    def _compute_montant(self):
        for record in self:
            if record.dossier_id:
                # Mapping phase names to the corresponding field names in Dossier
                phase_to_field = {
                    'TPI': 'montant_a_payer_tpi',
                    'Registration': 'montant_registration',
                    'Conservation fonciere': 'montant_concervation_fonciere'
                }
                field_name = phase_to_field.get(record.phase_id.name)
                if field_name:
                    record.montant = getattr(record.dossier_id, field_name, 0.0)
                else:
                    record.montant = 0.0
            else:
                record.montant = 0.0


    @api.onchange("phase_id")
    @api.depends("phase_id")
    def _compute_sequence(self):
        for rec in self:
            rec.sequence = rec.phase_id.ordre

    @api.depends("phase_id")
    @api.onchange("phase_id")
    def _compute_is_paid(self):
        for rec in self:
            rec.phase_is_paid = rec.phase_id.is_paid

    # @api.onchange("dossier_id.historique_phase_ids")
    @api.depends("dossier_id.historique_phase_ids")
    def _compute_phase_selection(self):
        phases_ids = [hs.phase_id.name for hs in self.dossier_id.historique_phase_ids]
        self.phase_selection_ids = [f.name for f in self.env["sgn.phase"].search([('name', 'not in', phases_ids)])]


    @api.model
    def create(self, vals):
        historique = super(HistoriquePhase, self).create(vals)
        historique._update_phase_statut()
        return historique

    def write(self, vals):
        res = super(HistoriquePhase, self).write(vals)
        self._update_phase_statut()
        return res

    def _update_phase_statut(self):
        if self.dossier_id:
            # Check if phase_id is set before updating the status
            if not self.phase_id:
                phase_statut = '-'
            else:
                phase_statut = 'encoure'  # Default status

                if self.date_fin:
                    phase_statut = 'termine'
                elif self.is_paid:
                    phase_statut = 'paye'
                elif self.montant_valide:
                    phase_statut = 'prete_aux_payment'
                elif self.date_debut:
                    phase_statut = 'encoure'

            self.dossier_id.phase_statut = phase_statut
