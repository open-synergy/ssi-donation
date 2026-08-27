# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class DonationRestrictionRelease(models.Model):
    """
    Reclassifies net assets by the amount of donor-restricted fund
    money that has already been realized (actually spent) by its
    consumer records.

    PSAK 45 / ISAK 35 require net assets to be reported split between
    "with donor restriction" and "without donor restriction". Money
    committed/realized against a ``donation_fund`` (tracked in
    ``donation_fund_usage``) never by itself reduces that fund's
    restricted net asset balance -- this document is the deliberate,
    user-initiated act that does: once Done, it posts a balanced
    two-line ``account.move`` between two net asset accounts (never
    touching cash, income, or the fund's own Amount Available), and
    totals into ``donation_fund.amount_released``. Both journal lines
    carry the fund's own analytic account, since a restriction release
    never adds or removes money from the fund -- only its net asset
    classification changes. Cancelling a ``done`` release deletes that
    journal entry again.
    """

    _name = "donation_restriction_release"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.company_currency",
        "mixin.account_move",
        "mixin.account_move_double_line",
    ]
    _description = "Donation Restriction Release"
    _order = "date desc, id desc"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    # Accounting Entry Header Mixin (``mixin.account_move``)
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "move_id"
    _accounting_date_field_name = "date"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"

    # Accounting Move Double Line Mixin (``mixin.account_move_double_line``)
    # -- ``debit_account_id``/``credit_account_id`` already match the
    # mixin's own defaults, so only the label and analytic account
    # need overriding. The analytic account is set on BOTH lines,
    # unlike ``donation`` (credit only) -- a restriction release must
    # not change the fund's analytic balance, so debit and credit
    # cancel out on that dimension.
    _debit_label_field_name = "name"
    _debit_analytic_account_id_field_name = "analytic_account_id"
    _credit_label_field_name = "name"
    _credit_analytic_account_id_field_name = "analytic_account_id"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Accounting date of this restriction release.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="donation_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Donation type this release is recorded under. Supplies "
        "the default Release Journal, Net Assets Released From "
        "Restriction Account, and Net Assets Reclassified Without "
        "Donor Restriction Account. Must have all three configured.",
    )
    fund_id = fields.Many2one(
        string="Fund",
        comodel_name="donation_fund",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Donor-restricted donation fund this release reclassifies "
        "net assets for. Must have Restriction Type 'With Donor "
        "Restriction'.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Amount of net assets to release from restriction. Must "
        "be greater than zero and must not exceed the Fund's "
        "Releasable Amount.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_currency_id",
        store=True,
        help="Currency this document is expressed in. This document "
        "does not support a currency other than the Company "
        "Currency.",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Accounting journal this release's journal entry is "
        "posted through. Defaulted from the selected Type's Release "
        "Journal when Type is picked; may be overridden manually "
        "while still in Draft.",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Net Assets Released From Restriction account, debited "
        "when this release reaches Done. Defaulted from the selected "
        "Type's Net Assets Released From Restriction Account when "
        "Type is picked; may be overridden manually while still in "
        "Draft.",
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Net Assets Reclassified Without Donor Restriction "
        "account, credited when this release reaches Done. Defaulted "
        "from the selected Type's Net Assets Reclassified Without "
        "Donor Restriction Account when Type is picked; may be "
        "overridden manually while still in Draft.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        related="fund_id.analytic_account_id",
        store=True,
        help="Analytic account of the selected Fund. Attached to "
        "BOTH this release's debit and credit journal items -- a "
        "restriction release never adds or removes money from the "
        "fund, only its net asset classification changes, so the "
        "analytic dimension must cancel out.",
    )
    amount_releasable = fields.Monetary(
        string="Releasable Amount",
        currency_field="currency_id",
        compute="_compute_amount_releasable",
        help="Remaining amount of the selected Fund's Amount Realized "
        "not yet released from restriction (Amount Realized minus "
        "Amount Released). Guidance only, not stored -- Amount must "
        "not exceed this value.",
    )
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Free-form note about this restriction release.",
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
        help="Journal entry generated when this release reaches "
        "Done. Deleted again, and this field cleared, when the "
        "release is cancelled.",
    )

    @api.depends(
        "fund_id.amount_realized",
        "fund_id.amount_released",
    )
    def _compute_amount_releasable(self):
        """Derive the still-unreleased portion of Amount Realized.

        :return: nothing; assigns ``amount_releasable``
        """
        for record in self:
            record.amount_releasable = (
                record.fund_id.amount_realized - record.fund_id.amount_released
            )

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        """Default the Journal from the selected Type's Release Journal.

        :return: nothing; assigns ``journal_id``
        """
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.release_journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_debit_account_id(self):
        """Default the Debit Account from the Type's release config.

        :return: nothing; assigns ``debit_account_id``
        """
        self.debit_account_id = False
        if self.type_id:
            self.debit_account_id = self.type_id.net_asset_released_account_id

    @api.onchange(
        "type_id",
    )
    def onchange_credit_account_id(self):
        """Default the Credit Account from the Type's release config.

        :return: nothing; assigns ``credit_account_id``
        """
        self.credit_account_id = False
        if self.type_id:
            self.credit_account_id = self.type_id.net_asset_reclassified_account_id

    @api.constrains("fund_id")
    def _check_fund_restricted(self):
        """Reject a Fund that is not donor-restricted.

        :raises ValidationError: when ``fund_id.restriction_type`` is
            not ``with_restriction``.
        """
        for record in self:
            if record.fund_id and record.fund_id.restriction_type != "with_restriction":
                error_message = """
Document Type: %s
Context: Configure restriction release fund
Database ID: %s
Problem: Fund does not have Restriction Type 'With Donor Restriction'
Solution: Select a Fund with Restriction Type 'With Donor Restriction'
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("type_id")
    def _check_type_release_configured(self):
        """Reject a Type whose release fields are not fully configured.

        :raises ValidationError: when ``type_id`` does not have
            Release Journal, Net Assets Released From Restriction
            Account, and Net Assets Reclassified Without Donor
            Restriction Account all filled.
        """
        for record in self:
            release_type = record.type_id
            if release_type and not (
                release_type.release_journal_id
                and release_type.net_asset_released_account_id
                and release_type.net_asset_reclassified_account_id
            ):
                error_message = """
Document Type: %s
Context: Configure restriction release type
Database ID: %s
Problem: Type is not configured for restriction release
Solution: Fill in Release Journal, Net Assets Released From
Restriction Account, and Net Assets Reclassified Without Donor
Restriction Account on the selected Type
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("amount")
    def _check_amount(self):
        """Reject an Amount that is not strictly positive.

        :raises ValidationError: when ``amount`` is zero or negative.
        """
        for record in self:
            if record.amount <= 0.0:
                error_message = """
Document Type: %s
Context: Configure restriction release amount
Database ID: %s
Problem: Amount is zero or negative
Solution: Enter an Amount greater than zero
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("amount", "fund_id")
    def _check_amount_releasable(self):
        """Reject an Amount exceeding the Fund's Releasable Amount.

        :raises ValidationError: when ``amount`` is greater than
            ``amount_releasable``.
        """
        for record in self:
            if record.amount > record.amount_releasable:
                error_message = """
Document Type: %s
Context: Configure restriction release amount
Database ID: %s
Problem: Amount exceeds the Fund's Releasable Amount
Solution: Enter an Amount not greater than the Fund's Releasable
Amount
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.model
    def _get_policy_field(self):
        """Register this model's policy fields with ``mixin.policy``.

        :return: list of policy field names
        """
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.post_done_action()
    def _10_create_accounting_entry(self):
        """Create and post this release's ``account.move``.

        Creates the header move and its balanced debit/credit pair
        of lines through ``mixin.account_move_double_line``, then
        posts the move. A no-op when ``move_id`` is already set, so
        this hook is safe to run only once per transition.

        :return: nothing
        """
        self.ensure_one()
        if self.move_id:
            return True
        self._create_standard_move()  # Mixin
        self._create_standard_ml()  # Mixin
        self._post_standard_move()  # Mixin

    @ssi_decorator.post_cancel_action()
    def _10_delete_accounting_entry(self):
        """Delete this release's ``account.move``, if any.

        :return: nothing
        """
        self.ensure_one()
        self._delete_standard_move()  # Mixin

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        """Reconfigure the statusbar's visible states on the form view.

        :param view_arch: the parsed form view architecture
        :return: the (possibly modified) view architecture
        """
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
