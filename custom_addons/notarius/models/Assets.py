from odoo import fields,models,_

class Asset(models.Model):
    _name = "nms.asset"
    _order = "id desc"


    asset_name = fields.Char(string=_("Asset"))
    asset_type = fields.Char(string=_("tType"))