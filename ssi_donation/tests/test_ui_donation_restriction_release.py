# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonationRestrictionRelease(HttpSavepointCase):
    """Tour tests for the ``donation_restriction_release`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tours."""
        super().setUpClass()

        # Shared release accounting configuration (donation_type), reused
        # by every tour below. The Receivable Account is
        # ``reconcile: True`` -- required by Odoo 14's own
        # ``AccountAccount._check_reconcile`` for receivable/payable
        # account types.
        cls.tour_release_journal = cls.env["account.journal"].create(
            {
                "name": "Tour Release Journal",
                "code": "TOURRRJ",
                "type": "general",
            }
        )
        cls.tour_released_account = cls.env["account.account"].create(
            {
                "name": "TOUR Net Assets Released",
                "code": "TOURRRNAR",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )
        cls.tour_reclassified_account = cls.env["account.account"].create(
            {
                "name": "TOUR Net Assets Reclassified",
                "code": "TOURRRNAC",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )
        cls.tour_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR Release Type Income",
                "code": "TOURRRIN",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.tour_receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR Release Type Receivable",
                "code": "TOURRRRC",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.tour_type_journal = cls.env["account.journal"].create(
            {
                "name": "Tour Release Type Journal",
                "code": "TOURRRTJ",
                "type": "general",
            }
        )
        cls.tour_type = cls.env["donation_type"].create(
            {
                "name": "Tour Restriction Release Type",
                "code": "TOURRRTY",
                "journal_id": cls.tour_type_journal.id,
                "income_account_id": cls.tour_income_account.id,
                "receivable_account_id": cls.tour_receivable_account.id,
                "release_journal_id": cls.tour_release_journal.id,
                "net_asset_released_account_id": cls.tour_released_account.id,
                "net_asset_reclassified_account_id": cls.tour_reclassified_account.id,
            }
        )

        # Pre-Condition for the create tour
        # (docs/donation_restriction_release/01-create.md): a
        # donor-restricted Fund with a Releasable Amount comfortably
        # above the amount the tour will type in.
        cls.tour_create_fund = cls._create_restricted_fund("Create")
        cls.env["test.donation_fund_consumer_one"].create(
            {
                "name": "Tour Release Create Consumer",
                "state": "done",
                "realized_amount": 100000.0,
                "donation_fund_id": cls.tour_create_fund.id,
            }
        )

        # Pre-Condition for the confirm tour
        # (docs/donation_restriction_release/04-confirm.md): a Draft
        # release, found in the list by its Fund's unique name.
        cls.tour_confirm_fund = cls._create_restricted_fund("Confirm")
        cls.env["test.donation_fund_consumer_one"].create(
            {
                "name": "Tour Release Confirm Consumer",
                "state": "done",
                "realized_amount": 100000.0,
                "donation_fund_id": cls.tour_confirm_fund.id,
            }
        )
        cls.tour_confirm_release = cls.env["donation_restriction_release"].create(
            {
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_confirm_fund.id,
                "amount": 30000.0,
                "journal_id": cls.tour_release_journal.id,
                "debit_account_id": cls.tour_released_account.id,
                "credit_account_id": cls.tour_reclassified_account.id,
            }
        )

        # Pre-Condition for the approve tour
        # (docs/donation_restriction_release/05-approve.md): a release
        # already in Waiting for Approval, found in the list by its
        # Fund's unique name.
        cls.tour_approve_fund = cls._create_restricted_fund("Approve")
        cls.env["test.donation_fund_consumer_one"].create(
            {
                "name": "Tour Release Approve Consumer",
                "state": "done",
                "realized_amount": 100000.0,
                "donation_fund_id": cls.tour_approve_fund.id,
            }
        )
        cls.tour_approve_release = cls.env["donation_restriction_release"].create(
            {
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_approve_fund.id,
                "amount": 20000.0,
                "journal_id": cls.tour_release_journal.id,
                "debit_account_id": cls.tour_released_account.id,
                "credit_account_id": cls.tour_reclassified_account.id,
            }
        )
        cls.tour_approve_release.action_confirm()

        # Pre-Condition for the cancel tour
        # (docs/donation_restriction_release/10-cancel.md): a Draft
        # release, found in the list by its Fund's unique name, and an
        # active cancellation reason for the wizard.
        cls.tour_cancel_fund = cls._create_restricted_fund("Cancel")
        cls.env["test.donation_fund_consumer_one"].create(
            {
                "name": "Tour Release Cancel Consumer",
                "state": "done",
                "realized_amount": 100000.0,
                "donation_fund_id": cls.tour_cancel_fund.id,
            }
        )
        cls.tour_cancel_release = cls.env["donation_restriction_release"].create(
            {
                "type_id": cls.tour_type.id,
                "fund_id": cls.tour_cancel_fund.id,
                "amount": 10000.0,
                "journal_id": cls.tour_release_journal.id,
                "debit_account_id": cls.tour_released_account.id,
                "credit_account_id": cls.tour_reclassified_account.id,
            }
        )
        cls.tour_cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Restriction Release Cancel Reason",
                "code": "TOURRRCR",
                "global_use": True,
            }
        )

    @classmethod
    def _create_restricted_fund(cls, suffix):
        """Create a donor-restricted Fund unique to one tour scenario.

        :param suffix: short scenario label used to keep the Fund's
            name, code, and its own Analytic/Net Asset Account codes
            unique across scenarios (e.g. ``"Create"``).
        :return: the created ``donation_fund`` record
        """
        analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "TOUR Release %s Analytic" % suffix,
            }
        )
        net_asset_account = cls.env["account.account"].create(
            {
                "name": "TOUR Release %s Fund Net Asset" % suffix,
                "code": ("TOURRR%sNA" % suffix)[:16],
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )
        return cls.env["donation_fund"].create(
            {
                "name": "Tour Restriction Release %s Fund" % suffix,
                "code": ("TOURRR%sFD" % suffix)[:16],
                "analytic_account_id": analytic_account.id,
                "restriction_type": "with_restriction",
                "restriction_note": "Tour restriction note.",
                "net_asset_account_id": net_asset_account.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``donation_restriction_release``.

        IK: docs/donation_restriction_release/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_restriction_release_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``donation_restriction_release``.

        IK: docs/donation_restriction_release/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_restriction_release_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``donation_restriction_release``.

        IK: docs/donation_restriction_release/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_restriction_release_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``donation_restriction_release``.

        IK: docs/donation_restriction_release/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_restriction_release_cancel",
            login="admin",
        )
