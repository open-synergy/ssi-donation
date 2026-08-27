# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestDonationRestrictionRelease(YamlTransactionCase):
    """Scenario tests for ``donation_restriction_release``."""

    def test_donation_restriction_release(self):
        """Run the workflow, accounting, and constraint scenarios."""
        self.run_yaml_scenario("test_data_donation_restriction_release.yaml")
