# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiDonationRestrictionReleaseOperatingUnit(HttpSavepointCase):
    """UI/UX tour test for the Operating Unit field this module adds to
    ``donation_restriction_release`` (E1 delta -- Additional Fields).

    Pairs with IK ``docs/donation_restriction_release/01-create.md``
    (delta), backed by the base IK ``ssi_donation``
    ``docs/donation_restriction_release/01-create.md`` for the
    navigation up to the New button.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the OU-visible admin user and release fixtures.

        Grants the admin user the multi-operating-unit group and an
        assigned/default Operating Unit, plus the Type fully configured
        for release, needed to open the release create form.
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
            {"name": "TOUR Donation Release OU Partner"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR Donation Release Operating Unit",
                "code": "TDRLOU",
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

        # Pre-Condition: supporting data so the Restriction Release
        # create form can be opened -- a Type fully configured for
        # release, following the same fixture pattern as the base
        # module's own tour test
        # (ssi_donation/tests/test_ui_donation_restriction_release.py).
        cls.tour_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Donation Release OU Journal",
                "code": "TDRLOUJ",
                "type": "general",
            }
        )
        cls.tour_released_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Release OU Released Account",
                "code": "TDRLOURL",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )
        cls.tour_reclassified_account = cls.env["account.account"].create(
            {
                "name": "TOUR Donation Release OU Reclassified Account",
                "code": "TDRLOURC",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_non_current_assets"
                ).id,
            }
        )
        cls.tour_type = cls.env["donation_type"].create(
            {
                "name": "TOUR Donation Release OU Type",
                "code": "TDRLOUTY",
                "journal_id": cls.tour_journal.id,
                "income_account_id": cls.tour_released_account.id,
                "receivable_account_id": cls.tour_released_account.id,
                "release_journal_id": cls.tour_journal.id,
                "net_asset_released_account_id": cls.tour_released_account.id,
                "net_asset_reclassified_account_id": cls.tour_reclassified_account.id,
            }
        )

    def test_field_operating_unit(self):
        """IK: docs/donation_restriction_release/01-create.md

        (E1 delta -- Additional Fields)
        """
        self.start_tour(
            "/web",
            "ssi_donation_operating_unit_donation_restriction_release_create",
            login="admin",
        )
