# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonationFund(HttpSavepointCase):
    """Tour tests for the ``donation_fund`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tour."""
        super().setUpClass()
        # Pre-Condition for the create tour (docs/donation_fund/
        # 01-create.md): an analytic account, picked from the m2o
        # dropdown by its unique name.
        cls.tour_analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "TOUR Donation Fund Analytic",
            }
        )

        # Pre-Condition for the "With Donor Restriction" branch of the
        # tour (Flow 4): a Net Asset Account, picked from the m2o
        # dropdown by its unique name.
        cls.tour_net_asset_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Fund Net Asset Account",
                "code": "TOURNA001",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )

        # Pre-Condition for Generate Code (docs/donation_fund/
        # 01-create.md, Flow 5): an active sequence.template for this
        # model is required, or clicking the button raises a
        # UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Donation Fund Code Sequence",
                "code": "ssi_donation.tour.donation_fund",
                "prefix": "TOURSEQFUND",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Donation Fund Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("donation_fund"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("donation_fund", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("donation_fund", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``donation_fund``.

        IK: docs/donation_fund/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_fund_create",
            login="admin",
        )
