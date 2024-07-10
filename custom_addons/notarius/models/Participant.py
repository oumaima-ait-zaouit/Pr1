from odoo import fields, models, _, api

class Participant(models.Model):
    _name = "nms.participant"
    _inherit = "res.partner"