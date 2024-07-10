from odoo import fields, models, _

class Dossier(models.Model):

    _name = "nms.dossier"
    _order = "id desc"

    dossier_state = fields.Selection(
        [
            ('en cours','En cours'),
            ('validé','Validé'),
            ('annulé','Annulé'),
            ('archivé','Archivé')
        ], 

        string=_("Statut de Dossier"))

    dossier_date_creation = fields.Date(string=_("Date de Creation"))
    dossier_date_validation = fields.Date(string=_("Date de Validation"))
    dossier_date_annulation = fields.Date(string=_("Date d'annulation"))
    client_id = fields.Many2many('nms.client', string=_("Client"), ondelete='cascade')
    phase_ids = fields.One2many('nms.phase', 'pahse_id', string=_("Phases"))
    document_ids = fields.One2many('nms.document', 'dossier_id', string=_("Documents"))



@api.onchange('service_id')
def _onchange_service_id(self):
    if self.service_id and self.service_id.type_service != 'vente_immobilier':
        # Masquer le champ bien_immobilier_id en vidant son domaine
        return {'domain': {'bien_immobilier_id': [('id', '=', False)]}}
    else:
        # Réinitialiser le domaine du champ bien_immobilier_id pour le montrer à nouveau
        return {'domain': {}}

