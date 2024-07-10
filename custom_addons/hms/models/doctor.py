from odoo import (
    fields, models, _
)

class Doctor(models.Model):

    _name = "hms.doctor"
    _description = "Doctor table"
    _order = "id desc"

    name = fields.Char(string=_("Name"))
    phone = fields.Char(string=_("Phone"))
    speciality = fields.Char(string=_("Speciality"))
    