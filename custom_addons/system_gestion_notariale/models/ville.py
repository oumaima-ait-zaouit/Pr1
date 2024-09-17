from odoo import fields, models, api, _

class Ville(models.Model):
    _name = 'sgn.ville'

    name = fields.Char(string=_("Ville"))
    region = fields.Selection(
        [
            ('casablanca_settat', 'Casablanca-Settat'),
            ('fes_meknes', 'Fès-Meknès'),
            ('rabat_sale_kenitra', 'Rabat-Salé-Kénitra'),
            ('tanger_tetouan_alhoceima', 'Tanger-Tétouan-Al Hoceïma'),
            ('marrakech_safi', 'Marrakech-Safi'),
            ('souss_massa', 'Souss-Massa'),
            ('draa_tafilalet', 'Drâa-Tafilalet'),
            ('guelmim_oued_noun', 'Guelmim-Oued Noun'),
            ('laayoune_sakia_el_hamra', 'Laâyoune-Sakia El Hamra'),
            ('dakhla_oued_ed_dahab', 'Dakhla-Oued Ed-Dahab'),
            ('oujda_en_nour', 'Oujda-Ennour'),
            ('khenifra_beni_mellal', 'Khénifra-Beni Mellal'),
        ],
        string='Région',
        required=True,
    )