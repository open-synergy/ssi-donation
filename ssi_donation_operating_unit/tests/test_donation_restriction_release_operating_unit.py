# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestDonationRestrictionReleaseOperatingUnit(YamlTransactionCase):
    """Cover the Operating Unit field added to
    ``donation_restriction_release`` by this module: propagation to the
    accounting entry, run by a user whose own default Operating Unit
    differs from the document's.
    """

    def test_donation_restriction_release_operating_unit(self):
        """Run the Operating Unit YAML scenarios for
        ``donation_restriction_release``.
        """
        self.run_yaml_scenario("donation_restriction_release_operating_unit.yaml")
