from odoo import fields, models, api, _

class Paiement(models.Model):
    _name = 'sgn.paiement'

    date_paiement = fields.Date(string=_("Date paiement"))
    name = fields.Selection(
        [
            ('registration','Registration'),
            ('quitus','Quitus Fiscal'),
            ('conservation','Conservation Fonciere'),
            ('honoraires','Honoraires'),
            ('tpi','TPI'),
            ('fraix','Fraix de dossier'),
        ],
        string=_("Type de paiement"))
    
   
    methode_paiement = fields.Selection(
        [
            ('espece','Espece'),
            ('carte','Carte bancaire'),
            ('virement','Virement'),
            ('cheque','Cheque'),
        ],
        string=_("Methode de paiement"))

    montant = fields.Float(string=_("Montant a payer"))
    dossier_id = fields.Many2one("sgn.dossier", string="Dossier")


    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('sgn.paiement.nombre') or _('New')