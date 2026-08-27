# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestDonationFundConsumerTwo(models.Model):
    """
    Second fixture model exercising ``mixin.donation_fund_consumer``,
    deliberately configured differently from
    ``test.donation_fund_consumer_one``.

    Its committed/realized field names are spelled differently
    (``commit_value``/``realize_value``) and its
    ``_donation_committed_states`` only includes ``done`` (not
    ``open``), proving each inheriting model configures the mixin
    independently and ``donation_fund`` can total contributions from
    two unrelated models on the same fund without knowing either
    model's name.
    """

    _name = "test.donation_fund_consumer_two"
    _description = "Test Donation Fund Consumer - Two"
    _inherit = ["mixin.donation_fund_consumer"]

    _donation_committed_field_name = "commit_value"
    _donation_realized_field_name = "realize_value"
    _donation_committed_states = ("done",)

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    commit_value = fields.Monetary(
        string="Commit Value",
        currency_field="currency_id",
    )
    realize_value = fields.Monetary(
        string="Realize Value",
        currency_field="currency_id",
    )
