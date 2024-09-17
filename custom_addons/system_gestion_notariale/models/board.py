from odoo import fields,models,api, _

class Board(models.AbstractModel):
    _inherit = 'board.board'

    client_count = fields.Integer(compute='_compute_client_count')
    dossier_count = fields.Integer(compute='_compute_dossier_count')
    propriete_count = fields.Integer(compute='_compute_propriete_count')

    def _compute_client_count(self):
        self.client_count = self.env['res.partner'].search_count([])

    def _compute_dossier_count(self):
        self.dossier_count = self.env['sgn.dossier'].search_count([])

    def _compute_propriete_count(self):
        self.propriete_count = self.env['sgn.propriete'].search_count([])
