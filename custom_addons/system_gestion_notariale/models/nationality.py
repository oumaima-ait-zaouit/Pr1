from odoo import models, fields, api, _

class Nationality(models.Model) :
    
    _name = 'sgn.nationality'
    _order = 'sequence'

    name = fields.Char(string=_("Nom"), required=True)
    sequence = fields.Integer("Sequence", default=1)
    can_buy = fields.Boolean(default=False)