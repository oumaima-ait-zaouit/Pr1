from odoo import fields, models, _

class Phase (models.Model):
    _name = "nms.phase"
    _order = "id desc"

    phase_name = fields.Char(string=_("Name"))
    phase_state = fields.Selection(
        [
            ('en cours','En cours'),
            ('terminé','Terminé')
        ],
    string=_("Etat de la phase"))