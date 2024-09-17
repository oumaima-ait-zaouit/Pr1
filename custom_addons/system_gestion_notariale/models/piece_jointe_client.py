from odoo import fields, models, api, _

class PieceJointeClient(models.Model):
    _name = 'sgn.piece_jointe_client'
    _inherit = 'sgn.piece_jointe'
    
    type_pj = fields.Selection([
        ('cin',"Carte d'Identite Nationale"),
        ('passport','Passport'),
        ('ci',"Certificat d'Immatriculation"),
        ('cic',"Carte d'Identité Consulaire"),
        ('jugement',"Jugement de Divorce Définitif"),
        ('acte',"Acte de marriage"),
        ('combattant',"Carte du Combattant / Carte de pupille de la Nation"),
    ], string=_("Type"))
    

    piece_identite_principale = fields.Boolean(string=_("Est elle la piece d'identite principale ?"), default=False)
    adresse = fields.Char(string=_("Adresse"))

    client_id = fields.Many2one('res.partner', string=_("Client"))



