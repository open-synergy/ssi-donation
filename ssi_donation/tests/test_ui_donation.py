# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonation(HttpSavepointCase):
    """Tour tests for the ``donation`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()

        # Shared accounting configuration, reused by every tour below.
        # The Receivable Account is ``reconcile: True`` -- required by
        # Odoo 14's own ``AccountAccount._check_reconcile`` for
        # receivable/payable account types.
        cls.tour_analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "TOUR Donation Analytic",
            }
        )
        cls.tour_fund = cls.env["donation_fund"].create(
            {
                "name": "Tour Donation Fund",
                "code": "TOURDNFD",
                "analytic_account_id": cls.tour_analytic_account.id,
            }
        )
        cls.tour_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Income Account",
                "code": "TOURDNIN",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.tour_receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Receivable Account",
                "code": "TOURDNRC",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.tour_cash_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Cash Account",
                "code": "TOURDNCA",
                "user_type_id": cls.env.ref("account.data_account_type_liquidity").id,
            }
        )
        cls.tour_journal = cls.env["account.journal"].create(
            {
                "name": "Tour Donation Journal",
                "code": "TOURDNJ",
                "type": "general",
                "default_account_id": cls.tour_cash_account.id,
            }
        )
        cls.tour_type = cls.env["donation_type"].create(
            {
                "name": "Tour Donation Type",
                "code": "TOURDNTY",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_income_account.id,
                "receivable_account_id": cls.tour_receivable_account.id,
            }
        )

        # Pre-Condition for the create tour (docs/donation/01-create.md):
        # a donor, picked from the m2o dropdown by its unique name.
        cls.tour_create_donor = cls.env["res.partner"].create(
            {
                "name": "Tour Donation Create Donor",
            }
        )

        # Pre-Condition for the confirm tour (docs/donation/04-confirm.md):
        # a Draft donation, found in the list by its donor's unique name.
        cls.tour_confirm_donor = cls.env["res.partner"].create(
            {
                "name": "Tour Donation Confirm Donor",
            }
        )
        cls.tour_confirm_donation = cls.env["donation"].create(
            {
                "partner_id": cls.tour_confirm_donor.id,
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_fund.id,
                "amount": 100000.0,
                "receipt_method": "cash",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_income_account.id,
            }
        )

        # Pre-Condition for the approve tour (docs/donation/05-approve.md):
        # a donation already in Waiting for Approval, found in the list
        # by its donor's unique name.
        cls.tour_approve_donor = cls.env["res.partner"].create(
            {
                "name": "Tour Donation Approve Donor",
            }
        )
        cls.tour_approve_donation = cls.env["donation"].create(
            {
                "partner_id": cls.tour_approve_donor.id,
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_fund.id,
                "amount": 200000.0,
                "receipt_method": "cash",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_income_account.id,
            }
        )
        cls.tour_approve_donation.action_confirm()

        # Pre-Condition for the cancel tour (docs/donation/10-cancel.md):
        # a Draft donation, found in the list by its donor's unique
        # name, and an active cancellation reason for the wizard.
        cls.tour_cancel_donor = cls.env["res.partner"].create(
            {
                "name": "Tour Donation Cancel Donor",
            }
        )
        cls.tour_cancel_donation = cls.env["donation"].create(
            {
                "partner_id": cls.tour_cancel_donor.id,
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_fund.id,
                "amount": 50000.0,
                "receipt_method": "cash",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_income_account.id,
            }
        )
        cls.tour_cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Donation Cancel Reason",
                "code": "TOURDNCR",
                "global_use": True,
            }
        )

    def test_create(self):
        """Run the create tour for ``donation``.

        IK: docs/donation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``donation``.

        IK: docs/donation/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``donation``.

        IK: docs/donation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``donation``.

        IK: docs/donation/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_cancel",
            login="admin",
        )
