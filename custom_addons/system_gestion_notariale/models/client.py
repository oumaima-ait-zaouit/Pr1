from odoo import models, fields, api

class Client(models.Model) :
    
    _inherit = 'res.partner'

    nationnality_ids = fields.Many2many("sgn.nationality", string="Nationalité")