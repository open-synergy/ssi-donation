# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonationType(HttpSavepointCase):
    """Tour tests for the ``donation_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records and configuration required by the tour."""
        super().setUpClass()
        # Pre-Condition for the create tour (docs/donation_type/
        # 01-create.md): a Journal, picked from the m2o dropdown by
        # its unique name.
        cls.tour_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Donation Type Journal",
                "code": "TOURDTJ",
                "type": "general",
            }
        )

        # Pre-Condition: an Income Account and a Receivable Account.
        cls.tour_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Type Income Account",
                "code": "TOURDTIN",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.tour_receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Type Receivable Account",
                "code": "TOURDTRC",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )

        # Pre-Condition for the Restriction Release tab (Flow 4): a
        # non-cash/non-bank Release Journal and the two release
        # accounts.
        cls.tour_release_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Donation Type Release Journal",
                "code": "TOURDTRJ",
                "type": "general",
            }
        )
        cls.tour_released_account = cls.env["account.account"].create(
            {
                "name": "TOUR Net Assets Released",
                "code": "TOURDTNAR",
                "user_type_id": cls.env.ref("account.data_account_type_equity").id,
            }
        )
        cls.tour_reclassified_account = cls.env["account.account"].create(
            {
                "name": "TOUR Net Assets Reclassified",
                "code": "TOURDTNAC",
                "user_type_id": cls.env.ref("account.data_account_type_equity").id,
            }
        )

        # Pre-Condition for Generate Code (docs/donation_type/
        # 01-create.md, Flow 6): an active sequence.template for this
        # model is required, or clicking the button raises a
        # UserError instead of assigning a code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Donation Type Code Sequence",
                "code": "ssi_donation.tour.donation_type",
                "prefix": "TOURSEQTYPE",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Donation Type Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("donation_type"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("donation_type", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("donation_type", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``donation_type``.

        IK: docs/donation_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_donation_donation_type_create",
            login="admin",
        )
