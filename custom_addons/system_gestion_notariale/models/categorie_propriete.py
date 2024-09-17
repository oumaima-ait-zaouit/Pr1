from odoo import fields, models,_, api
from odoo.exceptions import UserError


class CategoriePropriete(models.Model):
    _name = 'sgn.categorie_propriete'
    _order = 'sequence'
    _inherit = 'mail.thread'

    name = fields.Char(string="Name", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    taux_registration = fields.Float(string=_("Taux de registration"), tracking=True)
    sequence = fields.Integer(string="sequence")

    propriete_ids = fields.One2many('sgn.propriete', 'categorie_propriete', string="propriete", tracking=True)


    @api.model
    def unlink(self):
        for category in self:
            if category.propriete_ids:
                raise UserError("Cette catégorie ne peut pas être supprimée car elle contient des propriétés associées.")
        return super(CategoriePropriete, self).unlink()


    