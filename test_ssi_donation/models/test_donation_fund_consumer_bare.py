# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestDonationFundConsumerBare(models.Model):
    """
    Third fixture model exercising ``mixin.donation_fund_consumer``
    WITHOUT setting any ``_donation_*`` attribute.

    Proves a model that inherits the mixin but never configures the
    committed/realized field names still gets a ``donation_fund_usage``
    row with zero amounts, instead of an ``AttributeError``.
    """

    _name = "test.donation_fund_consumer_bare"
    _description = "Test Donation Fund Consumer - Bare"
    _inherit = ["mixin.donation_fund_consumer"]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
