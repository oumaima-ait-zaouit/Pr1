from odoo import models, fields, api, _

class Nationality(models.Model) :
    
    _name = 'sgn.nationality'

    name = fields.Char(string=_("Nom"), required=True)
    can_buy = fields.Boolean(default=False)
    client_id = fields.Many2one('res.partner', string='client')