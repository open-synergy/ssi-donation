# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestDonationFundConsumerOne(models.Model):
    """
    Fixture model exercising ``mixin.donation_fund_consumer`` with its
    ``_donation_*`` attributes fully configured.

    ``mixin.donation_fund_consumer`` is an ``AbstractModel`` and
    cannot be instantiated directly, so this concrete model -- and
    its sibling ``test.donation_fund_consumer_two`` -- exist purely
    to prove the mixin wires up correctly for any inheriting model,
    without ``donation_fund`` ever naming either of them.
    """

    _name = "test.donation_fund_consumer_one"
    _description = "Test Donation Fund Consumer - One"
    _inherit = ["mixin.donation_fund_consumer"]

    _donation_committed_field_name = "committed_amount"
    _donation_realized_field_name = "realized_amount"

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
    committed_amount = fields.Monetary(
        string="Committed Amount",
        currency_field="currency_id",
    )
    realized_amount = fields.Monetary(
        string="Realized Amount",
        currency_field="currency_id",
    )
