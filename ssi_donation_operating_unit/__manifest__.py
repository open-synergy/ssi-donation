# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Donation + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_donation",
        "ssi_operating_unit_mixin",
        "account_operating_unit",
        "web_tour",
    ],
    "data": [
        "security/res_group/donation.xml",
        "security/res_group/donation_restriction_release.xml",
        "security/ir_rule/donation.xml",
        "security/ir_rule/donation_restriction_release.xml",
        "view/donation.xml",
        "view/donation_restriction_release.xml",
        "view/assets.xml",
    ],
    "demo": [],
}
