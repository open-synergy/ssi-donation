# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class Donation(models.Model):
    """
    Represents the receipt of a single donation from a donor into one
    donation fund.

    This is the document that finally credits the side of the ledger
    ``donation_fund`` itself never touches: opening/approving it does
    nothing to accounting, but reaching ``done`` books a two-line
    ``account.move`` -- debiting either the cash journal's default
    account (``receipt_method`` ``cash``) or the donation type's
    Receivable Account (``receipt_method`` ``pledge``), and crediting
    the donation type's Income Account with the fund's own analytic
    account attached. That analytic account is the sole boundary
    between this module and every module that later spends the money
    (see ``donation_fund``), so this document is what finally makes
    ``donation_fund.amount_received`` a real, non-placeholder number.
    Cancelling a ``done`` donation deletes that journal entry again.
    """

    _name = "donation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.company_currency",
        "mixin.account_move",
        "mixin.account_move_double_line",
    ]
    _description = "Donation"
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
    # -- only the two attributes that differ from the mixin's own
    # defaults need overriding here.
    _debit_label_field_name = "name"
    _credit_account_id_field_name = "income_account_id"
    _credit_analytic_account_id_field_name = "analytic_account_id"
    _credit_label_field_name = "name"

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
        help="Accounting date of this donation receipt.",
    )
    partner_id = fields.Many2one(
        string="Donor",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Donor this donation is received from.",
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
        help="Donation type this receipt is recorded under. Supplies "
        "the default Journal, Income Account, Receivable Account, "
        "and the set of Funds this donation may be assigned to.",
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
        help="Donation fund the money is received into. Must be one "
        "of the selected Type's Allowed Funds, unless that list is "
        "empty. Its Analytic Account is credited when this donation "
        "reaches Done.",
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
        help="Amount donated. Must be greater than zero.",
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
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Free-form note about this donation, e.g. how the donor "
        "wishes to be acknowledged.",
    )
    receipt_method = fields.Selection(
        string="Receipt Method",
        selection=[
            ("cash", "Cash Received"),
            ("pledge", "Pledge / Receivable"),
        ],
        required=True,
        default="cash",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="How this donation is received. 'Cash Received' debits "
        "the Journal's own default account -- the money is already "
        "in hand. 'Pledge / Receivable' debits the Type's Receivable "
        "Account instead -- the donor has committed to pay, but the "
        "cash has not arrived yet.",
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
        help="Accounting journal this donation's journal entry is "
        "posted through. Defaulted from the selected Type when Type "
        "is picked; may be overridden manually while still in Draft.",
    )
    income_account_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Contribution revenue account credited when this "
        "donation reaches Done. Defaulted from the selected Type "
        "when Type is picked; may be overridden manually while still "
        "in Draft.",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
        compute="_compute_debit_account_id",
        store=True,
        compute_sudo=True,
        help="Account debited when this donation reaches Done. The "
        "Journal's own default account when Receipt Method is 'Cash "
        "Received'; the Type's Receivable Account when Receipt "
        "Method is 'Pledge / Receivable'.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        related="fund_id.analytic_account_id",
        store=True,
        help="Analytic account of the selected Fund. Attached to this "
        "donation's own credit journal item, never its debit item -- "
        "the analytic dimension belongs to the income/expense side, "
        "not to cash or receivables.",
    )
    restriction_type = fields.Selection(
        string="Restriction Type",
        related="fund_id.restriction_type",
        store=True,
        help="Donor restriction terms of the selected Fund, copied "
        "here so reports can split unrestricted and donor-restricted "
        "donations without joining to ``donation_fund``.",
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
        help="Journal entry generated when this donation reaches "
        "Done. Deleted again, and this field cleared, when the "
        "donation is cancelled.",
    )

    @api.depends(
        "receipt_method",
        "journal_id",
        "journal_id.default_account_id",
        "type_id",
        "type_id.receivable_account_id",
    )
    def _compute_debit_account_id(self):
        """Derive the debit account from the Receipt Method.

        :return: nothing; assigns ``debit_account_id``
        """
        for record in self:
            result = False
            if record.receipt_method == "cash":
                result = record.journal_id.default_account_id
            elif record.receipt_method == "pledge":
                result = record.type_id.receivable_account_id
            record.debit_account_id = result

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        """Default the Journal from the selected Type.

        :return: nothing; assigns ``journal_id``
        """
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_income_account_id(self):
        """Default the Income Account from the selected Type.

        :return: nothing; assigns ``income_account_id``
        """
        self.income_account_id = False
        if self.type_id:
            self.income_account_id = self.type_id.income_account_id

    @api.constrains("amount")
    def _check_amount(self):
        """Reject an Amount that is not strictly positive.

        :raises ValidationError: when ``amount`` is zero or negative.
        """
        for record in self:
            if record.amount <= 0.0:
                error_message = """
Document Type: %s
Context: Configure donation amount
Database ID: %s
Problem: Amount is zero or negative
Solution: Enter an Amount greater than zero
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("fund_id", "type_id")
    def _check_fund_allowed(self):
        """Reject a Fund outside the Type's Allowed Funds.

        An empty Allowed Funds list on the Type means every Fund is
        allowed, so this only rejects when the list is non-empty and
        the selected Fund is not in it.

        :raises ValidationError: when ``type_id.allowed_fund_ids`` is
            non-empty and does not contain ``fund_id``.
        """
        for record in self:
            allowed = record.type_id.allowed_fund_ids
            if allowed and record.fund_id not in allowed:
                error_message = """
Document Type: %s
Context: Configure donation fund
Database ID: %s
Problem: Fund is not one of the selected Type's Allowed Funds
Solution: Select a Fund listed in the Type's Allowed Funds, or add
this Fund to the Type's Allowed Funds
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("date", "fund_id")
    def _check_date_within_fund_window(self):
        """Reject a Date outside the Fund's restriction time window.

        A Fund without ``date_start``/``date_end`` set is not
        time-bound, so this only rejects when the relevant bound is
        actually filled on the Fund and the Date falls outside it.

        :raises ValidationError: when ``date`` is earlier than
            ``fund_id.date_start`` or later than ``fund_id.date_end``.
        """
        for record in self:
            fund = record.fund_id
            if not (record.date and fund):
                continue
            if fund.date_start and record.date < fund.date_start:
                error_message = """
Document Type: %s
Context: Configure donation date
Database ID: %s
Problem: Date is earlier than the Fund's Restriction Start Date
Solution: Pick a Date on or after the Fund's Restriction Start Date
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
            if fund.date_end and record.date > fund.date_end:
                error_message = """
Document Type: %s
Context: Configure donation date
Database ID: %s
Problem: Date is later than the Fund's Restriction End Date
Solution: Pick a Date on or before the Fund's Restriction End Date
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
        """Create and post this donation's ``account.move``.

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
        """Delete this donation's ``account.move``, if any.

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
