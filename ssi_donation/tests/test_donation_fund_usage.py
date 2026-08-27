# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestDonationFundUsage(YamlTransactionCase):
    """Scenario tests for ``mixin.donation_fund_consumer``/``donation_fund_usage``.

    ``mixin.donation_fund_consumer`` is an ``AbstractModel`` and cannot
    be instantiated directly, so this suite exercises it through the
    fixture models of module ``test_ssi_donation``. Guard against that
    module not being installed, so this test fails loudly with a clear
    reason instead of an obscure ``KeyError``.
    """

    def test_donation_fund_usage(self):
        """Run the ledger wiring and access-control scenarios."""
        if "test.donation_fund_consumer_one" not in self.env:
            self.skipTest(
                "Model 'test.donation_fund_consumer_one' is not "
                "available - module 'test_ssi_donation' is not "
                "installed."
            )
        self.run_yaml_scenario("test_data_donation_fund_usage.yaml")

    def test_donation_fund_usage_duplicate_model_res_id(self):
        """Reject two ledger rows sharing (model_id, res_id).

        Pure Python -- trigger P5 (L-22: the ``psycopg2.IntegrityError``
        raised by the ``donation_fund_usage`` unique ``_sql_constraints``
        is not one of the 12 exception types ``expect_error`` recognizes
        in YAML).
        """
        analytic_account = self.env["account.analytic.account"].create(
            {"name": "Test Consumer Analytic Duplicate Guard"}
        )
        fund = self.env["donation_fund"].create(
            {
                "name": "Test Fund Duplicate Guard",
                "code": "TDONU098",
                "analytic_account_id": analytic_account.id,
            }
        )
        model = self.env["ir.model"].search(
            [("model", "=", "test.donation_fund_consumer_one")], limit=1
        )
        self.env["donation_fund_usage"].sudo().create(
            {
                "fund_id": fund.id,
                "model_id": model.id,
                "res_id": 999999,
            }
        )
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self.env["donation_fund_usage"].sudo().create(
                {
                    "fund_id": fund.id,
                    "model_id": model.id,
                    "res_id": 999999,
                }
            )

    def test_donation_fund_delete_with_active_usage_rejected(self):
        """Reject deleting a ``donation_fund`` with an active usage row.

        Pure Python -- trigger P5 (L-22: the ``psycopg2.IntegrityError``
        raised by the FK ``RESTRICT`` on ``donation_fund_usage.fund_id``
        is not one of the 12 exception types ``expect_error``
        recognizes in YAML).
        """
        analytic_account = self.env["account.analytic.account"].create(
            {"name": "Test Consumer Analytic Delete Guard"}
        )
        fund = self.env["donation_fund"].create(
            {
                "name": "Test Fund Delete Guard",
                "code": "TDONU099",
                "analytic_account_id": analytic_account.id,
            }
        )
        self.env["test.donation_fund_consumer_one"].create(
            {
                "name": "Doc Delete Guard",
                "state": "done",
                "committed_amount": 10.0,
                "donation_fund_id": fund.id,
            }
        )
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            fund.unlink()
