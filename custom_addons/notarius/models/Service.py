from odoo import fields, models, _

class Service(models,Model):

    _name = "nms.service"
    _descriptio = "testets"
    _order = "id desc"

    service_title = fields.Char(string=_("Title"))
    service_amount = fields.Float(string=_("Amount"))
    service_payed_amount = fields.Char(string=_("Payed Amount"))
    service_unpayed_amount = fields.Char(string=_("Unpayed Amount"))
    service_notary_fees = fields.Float(string=_("Nortary fees"))
    service_acte_required = fields.Boolean(string=_("Acte is required ?"))