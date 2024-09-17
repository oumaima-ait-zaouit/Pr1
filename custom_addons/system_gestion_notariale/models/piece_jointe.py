from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date

class PieceJointe(models.Model):
    _name = 'sgn.piece_jointe'
    

    identifiant = fields.Char(string=("Nombre Identifiant"), required=True)    
    fichier = fields.Binary(string=_("Fichier"), required=True)
    date_expiration = fields.Date(string=_("Date d'éxpiration"))
    
    statut = fields.Selection([
        ('encours','En Cours'),
        ('valide','Validée'),
    ], required=True)

    @api.constrains('date_expiration')
    def _check_date(self):
        for record in self:
            if record.date_expiration and record.date_expiration < date.today():
                raise ValidationError("La date d'expiration doit être supérieure ou égale à la date d'aujourd'hui.")
