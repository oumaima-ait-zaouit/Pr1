from odoo import fields, models, api, _

class PieceJointePropriete(models.Model):
    _name = 'sgn.piece_jointe_propriete'
    _inherit = 'sgn.piece_jointe'
    
    name = fields.Selection([
        ('titre','Titre'),
        ('facture',"Facture d'eau et d'electricite"),
        ('certificat','certificat de proprieté'),
        ('vna','VNA'),
    ], string=_("Type"), required=True)
    date_creation = fields.Date(string=_("Date de création"))
    lieu_creation = fields.Char(string=_("Lieu de création"))

    propriete_id = fields.Many2one('sgn.propriete', string=_("Propriete"))