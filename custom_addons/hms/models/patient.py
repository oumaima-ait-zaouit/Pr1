from odoo import (
    fields, models, _
)

class Patient(models.Model):

    _name = "hms.patient"
    _description = "Patient table"
    _order = "id desc"

    name = fields.Char(string=_("Name"))
    phone = fields.Char(string=_("Phone"))
    address = fields.Char(string=_('Address'))
    gender = fields.Selection([('male','Male'), ('female','Female')])
    medical_record_number = fields.Char(string=_('Medical Record Number'))
    blood_type = fields.Selection([('O_negative', 'O negative'), ('A negative', 'A negative'), ('B_negative', 'B negative'), ('AB_negative', 'AB negative')])

