from odoo import models, fields, api, _

class Nationalite(models.Model) :
    _name = 'sgn.nationalite'
    _inherit = 'mail.thread'
    _order = 'sequence'

    name = fields.Char(string=_("Nom"), required=True, tracking=True)
    sequence = fields.Integer(string=_("Sequence"), default=1)
    can_buy = fields.Boolean(string=_("Peux Avoir un terrain agricole ?"),default=False, required=True, tracking=True)