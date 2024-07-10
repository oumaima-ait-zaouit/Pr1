from odoo import models, fields, _, api


class Document (models.Model):

    _name = "nms.document"
    _order = "id desc"

    document_name = fields.Char(string=_("Name"))
    document_file = fields.Binary(string=_("File"))
    document_annexe = fields.Binary(string=_("Annexe"))
    document_note = fields.Text(string=_("Note"))
    dossier_id = fields.Many2one('nms.dossier', string=_("Dossier"), ondelete='cascade')
    document_state = fields.Selection(
        [
            ('verifié','Verifié'),
            ('encours','En cours'),
            ('rejeté','Rejeté')
        ],
    string=_("Statut de Document"))

@api.onchange('client_type')
def _onchange_client_type(self):
        if self.client_type == 'individual':
            self.client_registration = False
        else:
            self.client_date_of_birth = False
            self.client_identification_document = False   

