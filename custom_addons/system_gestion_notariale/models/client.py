from odoo import models, fields, api

class Client(models.Model) :
    
    _inherit = 'res.partner'

    nationnality_ids = fields.One2many("sgn.nationality", 'client_id', string="Nationalité")