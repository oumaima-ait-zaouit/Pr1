from odoo import fields, models, _, api

class Client(models.Model):

    _name = "nms.client"
    _description = "This serves as a good base for all client types, ensuring common attributes and methods are centralized."
    _inherit = "mail.thread"
    _order = "id desc"

    client_name = fields.Char(string=_("Name"))
    client_image = fields.Binary(string=_("Image"))
    client_address = fields.Char(string=_("Address"))
    client_email = fields.Char(string=_("Email"))
    client_phone_number = fields.Char(string=_("Phone Number"))
    client_type = fields.Selection(
        [
            ('individual', 'Individual'),
            ('organization', 'Organization')
        ], 
        string=_("Client Type"))

    #--------------Individual Info------------------------------

    client_date_of_birth = fields.Date(string=_("Date of Birth"))
    client_identification_document = fields.Binary(string=_("Identification Document"))
    client_nationalite = fields.Selection(
        [
            ('fr', _('French')),
            ('us', _('American')),
            ('es', _('Spanish')),
            ('br', _('British')),
            ('gr', _('German')),
            ('it', _('Italian')),
            ('ma', _('Moroccan')),
            ('cn', _('Chinese')),
            ('tn', _('Tunisian')),
            ('sn', _('Senegalese'))
        ],
    )

    #--------------Organization Info------------------------------

    client_registration = fields.Char(string=_("Registration Number"))
    
    
@api.onchange('client_type')
def _onchange_client_type(self):
        if self.client_type == 'individual':
            self.client_registration = False
        else:
            self.client_date_of_birth = False
            self.client_identification_document = False
    




    
    
    

