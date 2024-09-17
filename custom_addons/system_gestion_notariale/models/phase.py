from odoo import fields, models, api, _

class Phase(models.Model):
    _name = 'sgn.phase'
    _order = 'ordre'
    _inherit = 'mail.thread'

    name = fields.Char(string=_("Nom"), tracking=True)
    ordre = fields.Integer(string=_("Ordre"), tracking=True)
    is_paid = fields.Boolean(string="Est il payable ?", default=False, tracking=True)
    dossier_id = fields.Many2one('sgn.dossier', string=_("Dossier"), tracking=True)