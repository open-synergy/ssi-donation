# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DonationFund(models.Model):
    """
    Represents a donation fund: an envelope of donated money bound to a
    single analytic account, together with whether the donor restricted
    how that money may be used.
    A fund never holds money by itself — the ``donation`` receipt
    document credits the bound analytic account when money comes in
    (reflected here as ``amount_received``), and the document that uses
    the money debits it. This model only carries the dimension
    (``analytic_account_id``) and the donor restriction terms (PSAK 45 /
    ISAK 35: "with donor restriction" vs "without donor restriction");
    ``amount_committed``/``amount_realized`` remain placeholder zero
    since the documents that commit/realize money from a fund are not
    part of this item's scope and are wired up in a later item.
    """

    _name = "donation_fund"
    _inherit = [
        "mixin.master_data",
        "mixin.company_currency",
    ]
    _description = "Donation Fund"
    _order = "name, id"

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        required=True,
        ondelete="restrict",
        help="Analytic account this fund is bound to. This is the sole "
        "boundary between the donation module and every module that "
        "uses donated money: the donation receipt document credits "
        "this analytic account when funds come in, and the "
        "consuming document debits it when funds are used. Each "
        "analytic account may only be bound to one donation fund.",
    )
    restriction_type = fields.Selection(
        string="Restriction Type",
        selection=[
            ("without_restriction", "Without Donor Restriction"),
            ("with_restriction", "With Donor Restriction"),
        ],
        required=True,
        default="without_restriction",
        help="Whether the donor attached conditions to how this fund "
        "may be used (PSAK 45 / ISAK 35). 'With Donor Restriction' "
        "requires a Restriction Note and a Net Asset Account.",
    )
    restriction_note = fields.Text(
        string="Restriction Note",
        help="The donor's restriction terms, in the donor's own words. "
        "Required when Restriction Type is 'With Donor Restriction'.",
    )
    date_start = fields.Date(
        string="Restriction Start Date",
        help="Start of the time window the donor's restriction applies "
        "to. Leave empty when the restriction is not time-bound.",
    )
    date_end = fields.Date(
        string="Restriction End Date",
        help="End of the time window the donor's restriction applies "
        "to. Must not be earlier than Restriction Start Date. Leave "
        "empty when the restriction is not time-bound.",
    )
    net_asset_account_id = fields.Many2one(
        string="Net Asset Account",
        comodel_name="account.account",
        help="Net asset account this fund's balance is carried on. "
        "Required when Restriction Type is 'With Donor Restriction'.",
    )
    donation_ids = fields.One2many(
        string="Donations",
        comodel_name="donation",
        inverse_name="fund_id",
        help="Donation receipt documents pointing to this fund, of "
        "any state. Not shown on any view -- it exists only so "
        "``amount_received`` recomputes when a Donation's state, "
        "Amount, or Fund changes.",
    )
    amount_received = fields.Monetary(
        string="Amount Received",
        currency_field="company_currency_id",
        compute="_compute_amount_received",
        store=True,
        compute_sudo=True,
        help="Total Amount of every ``donation`` document in state "
        "Done that points to this fund.",
    )
    amount_committed = fields.Monetary(
        string="Amount Committed",
        currency_field="company_currency_id",
        compute="_compute_amount_committed",
        store=True,
        compute_sudo=True,
        help="Total amount committed against this fund. Always zero "
        "for now: the document that commits money from a fund is "
        "not part of this item's scope and is wired up in a later "
        "item.",
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="company_currency_id",
        compute="_compute_amount_realized",
        store=True,
        compute_sudo=True,
        help="Total amount already realized (actually spent) against "
        "this fund. Always zero for now: the document that realizes "
        "a commitment is not part of this item's scope and is wired "
        "up in a later item.",
    )
    amount_available = fields.Monetary(
        string="Amount Available",
        currency_field="company_currency_id",
        compute="_compute_amount_available",
        store=True,
        compute_sudo=True,
        help="Remaining amount this fund may still commit (Amount "
        "Received minus Amount Committed).",
    )

    @api.depends(
        "donation_ids.amount",
        "donation_ids.state",
    )
    def _compute_amount_received(self):
        """Sum the Amount of every Done donation pointing to this fund.

        :return: nothing; assigns ``amount_received``
        """
        for record in self:
            result = 0.0
            for donation in record.donation_ids:
                if donation.state == "done":
                    result += donation.amount
            record.amount_received = result

    @api.depends()
    def _compute_amount_committed(self):
        """Return zero until a fund-consuming document exists.

        No real dependency: the document that commits money from a
        fund is not part of this item's scope, so the value is a
        fixed placeholder wired up in a later item.

        :return: nothing; assigns ``amount_committed``
        """
        for record in self:
            record.amount_committed = 0.0

    @api.depends()
    def _compute_amount_realized(self):
        """Return zero until a commitment-realizing document exists.

        No real dependency: the document that realizes a commitment
        against a fund is not part of this item's scope, so the value
        is a fixed placeholder wired up in a later item.

        :return: nothing; assigns ``amount_realized``
        """
        for record in self:
            record.amount_realized = 0.0

    @api.depends("amount_received", "amount_committed")
    def _compute_amount_available(self):
        """Compute the still-uncommitted portion of Amount Received.

        :return: nothing; assigns ``amount_available``
        """
        for record in self:
            record.amount_available = record.amount_received - record.amount_committed

    @api.constrains("analytic_account_id")
    def _check_analytic_account_id(self):
        """Forbid an Analytic Account already bound to another fund.

        The analytic account is the sole interface between this
        module and every module that uses donated money, so a single
        analytic account must never be shared by two funds —
        otherwise a credit/debit posted for one fund could not be
        told apart from one posted for another fund.

        :raises ValidationError: when another ``donation_fund``
            record already uses the same ``analytic_account_id``.
        """
        # No falsy-value guard: ``analytic_account_id`` is ``required``,
        # and its DB column carries a NOT NULL constraint enforced by
        # the actual INSERT/UPDATE, which always runs before this
        # ``@api.constrains`` method (see ``BaseModel.create``/
        # ``write``). A record can therefore never reach this method
        # with an empty ``analytic_account_id``, so such a guard would
        # be dead code.
        for record in self:
            duplicate_count = self.search_count(
                [
                    ("id", "!=", record.id),
                    (
                        "analytic_account_id",
                        "=",
                        record.analytic_account_id.id,
                    ),
                ]
            )
            if duplicate_count > 0:
                error_message = """
Document Type: %s
Context: Configure analytic account
Database ID: %s
Problem: Analytic Account is already used by another Donation Fund
Solution: Select an Analytic Account that is not yet bound to any
Donation Fund
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("restriction_type", "restriction_note")
    def _check_restriction_note(self):
        """Require a Restriction Note on donor-restricted funds.

        :raises ValidationError: when ``restriction_type`` is
            ``with_restriction`` and ``restriction_note`` is empty.
        """
        for record in self:
            if (
                record.restriction_type == "with_restriction"
                and not record.restriction_note
            ):
                error_message = """
Document Type: %s
Context: Configure donor restriction
Database ID: %s
Problem: Restriction Note is required when Restriction Type is
'With Donor Restriction'
Solution: Fill in the Restriction Note, or change Restriction Type to
'Without Donor Restriction'
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("restriction_type", "net_asset_account_id")
    def _check_net_asset_account_id(self):
        """Require a Net Asset Account on donor-restricted funds.

        :raises ValidationError: when ``restriction_type`` is
            ``with_restriction`` and ``net_asset_account_id`` is
            empty.
        """
        for record in self:
            if (
                record.restriction_type == "with_restriction"
                and not record.net_asset_account_id
            ):
                error_message = """
Document Type: %s
Context: Configure donor restriction
Database ID: %s
Problem: Net Asset Account is required when Restriction Type is
'With Donor Restriction'
Solution: Fill in the Net Asset Account, or change Restriction Type to
'Without Donor Restriction'
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        """Forbid a Restriction End Date earlier than the Start Date.

        :raises ValidationError: when both dates are filled and
            ``date_end`` is earlier than ``date_start``.
        """
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end < record.date_start
            ):
                error_message = """
Document Type: %s
Context: Configure restriction time window
Database ID: %s
Problem: Restriction End Date is earlier than Restriction Start Date
Solution: Pick a Restriction End Date on or after the Restriction
Start Date
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
