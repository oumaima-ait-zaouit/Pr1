from odoo import fields, models, api, _

class PieceJointeDossier(models.Model):
    _name = 'sgn.piece_jointe_dossier'
    _inherit = 'sgn.piece_jointe'
    
    name = fields.Selection([
        ('ordre','Ordre de mission'),
        ('mention',"Mention d'enregistrement"),
        ('quitus','Quitus Fiscale'),
        ('promis',"Promis de Vente"),
        ('procuration',"Procuration"),
        ('vna',"VNA"),
    ], string=_("Type"))

    dossier_id = fields.Many2one('sgn.dossier', string=_("Dossier"))