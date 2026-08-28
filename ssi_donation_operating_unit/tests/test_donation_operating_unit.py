# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestDonationOperatingUnit(YamlTransactionCase):
    """Cover the Operating Unit field added to ``donation`` by this
    module: propagation to the accounting entry (both filled and empty
    Operating Unit, run by a user whose own default Operating Unit
    differs), record rule visibility, the local-group-implies-OU-group
    relation, and the Draft-only editability of ``operating_unit_id``.
    """

    def test_donation_operating_unit(self):
        """Run the Operating Unit YAML scenarios for ``donation``."""
        self.run_yaml_scenario("donation_operating_unit.yaml")
