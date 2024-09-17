from odoo import fields, models, api, _

class RelationAcheteurVendeur(models.Model):
    _name = "sgn.relation"
    _inherit = 'mail.thread'

    name = fields.Char(string=_("Nom de la realtion"), tracking=True)
    is_exonere = fields.Boolean(string=_("Nom de la realtion"), default=False, tracking=True)