# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonationOperatingUnit(HttpSavepointCase):
    """UI/UX tour test for the Operating Unit field this module adds to
    ``donation`` (E1 delta -- Additional Fields).

    Pairs with IK ``docs/donation/01-create.md`` (delta), backed by the
    base IK ``ssi_donation`` ``docs/donation/01-create.md`` for the
    navigation up to the New button.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the OU-visible admin user and donation fixtures.

        Grants the admin user the multi-operating-unit group and an
        assigned/default Operating Unit, plus the Type/Fund needed to
        open the donation create form.
        """
        super().setUpClass()

        # Pre-Condition: the Operating Unit field is gated by the multi
        # operating unit group (`groups="operating_unit.group_multi_operating_unit"`
        # in the view) -- without it, the field is never rendered and the
        # delta assertion would never find it. The user also needs at
        # least one operating unit assigned so the field has a meaningful
        # (non-empty) default.
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.operating_unit_partner = cls.env["res.partner"].create(
            {"name": "TOUR Donation OU Partner"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR Donation Operating Unit",
                "code": "TDNOU",
                "partner_id": cls.operating_unit_partner.id,
            }
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )
        cls.user_admin.sudo().write(
            {
                "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                "default_operating_unit_id": cls.operating_unit.id,
            }
        )

        # Pre-Condition: supporting data so the Donation create form can
        # be opened -- Type / Fund, following the same fixture pattern as
        # the base module's own tour test (ssi_donation/tests/test_ui_donation.py).
        cls.tour_analytic_account = cls.env["account.analytic.account"].create(
            {"name": "TOUR Donation OU Analytic"}
        )
        cls.tour_fund = cls.env["donation_fund"].create(
            {
                "name": "TOUR Donation OU Fund",
                "code": "TDNOUFD",
                "analytic_account_id": cls.tour_analytic_account.id,
            }
        )
        cls.tour_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation OU Income Account",
                "code": "TDNOUIN",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.tour_receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation OU Receivable Account",
                "code": "TDNOURC",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.tour_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Donation OU Journal",
                "code": "TDNOUJ",
                "type": "general",
            }
        )
        cls.tour_type = cls.env["donation_type"].create(
            {
                "name": "TOUR Donation OU Type",
                "code": "TDNOUTY",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_income_account.id,
                "receivable_account_id": cls.tour_receivable_account.id,
            }
        )

    def test_field_operating_unit(self):
        """IK: docs/donation/01-create.md (E1 delta -- Additional Fields)"""
        self.start_tour(
            "/web",
            "ssi_donation_operating_unit_donation_create",
            login="admin",
        )
