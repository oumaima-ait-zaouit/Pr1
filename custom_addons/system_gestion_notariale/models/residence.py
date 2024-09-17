from odoo import models, fields, api

class Residence(models.Model):

    _name = 'sgn.residence'
    _inherit = 'sgn.bien_immobilier'
    
    type_residence = fields.Selection ([
        ('villa','Villa'),
        ('logementsocial','Logement Social'),
        ('appartement','Appartement'),
        ('duplex','Duplex'),
        ('maison','Maison')
        ], 
        string=("Type de Residence")
    )
    is_principal_residence = fields.Selection([
        ('principale', 'Principale'),
        ('secondaire', 'Secondaire'),
    ], default='principale')


   