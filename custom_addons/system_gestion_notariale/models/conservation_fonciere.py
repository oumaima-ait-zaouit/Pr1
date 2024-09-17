from odoo import fields, models, api, _


class ConservationFonciere(models.Model):
    _name = 'sgn.conservation'
    _inherit = 'mail.thread'

    name = fields.Char(string='Nom de la Conservation Foncière', required=True, tracking=True)
    adresse = fields.Char(string='Adresse', tracking=True)
    telephone = fields.Char(string='Téléphone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    responsable = fields.Char(string='Responsable', tracking=True)

    ville = fields.Many2one('sgn.ville',string='Ville', tracking=True)
    propriete_ids = fields.One2many('sgn.propriete', 'conservation_fonciere_id', string="propriete", tracking=True)
    