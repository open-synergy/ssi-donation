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

    def test_donation_fund_usage_write_override(self):
        """Run the ledger wiring scenarios for a ``_write()``-override consumer."""
        if "test.donation_fund_consumer_rewrite" not in self.env:
            self.skipTest(
                "Model 'test.donation_fund_consumer_rewrite' is not "
                "available - module 'test_ssi_donation' is not "
                "installed."
            )
        self.run_yaml_scenario("test_data_donation_fund_usage_write_override.yaml")

    def test_donation_fund_usage_write_override_reentrancy_regression(self):
        """Reproduce the ``_write()`` reentrancy this issue fixes.

        Pure Python -- trigger P5 (L-22: the duplicate-row
        ``psycopg2.IntegrityError`` this reentrancy causes on the
        old ``_donation_fund_usage_refresh()`` is not one of the 12
        types ``expect_error`` recognizes in YAML, and forcing the
        exact flush window that exposes it needs
        ``invalidate_cache()``, which has no YAML action).

        ``test.donation_fund_consumer_rewrite`` overrides the
        private ``_write()`` -- the same pattern
        ``school_scholarship_funding_source`` uses in
        ``ssi_school_scholarship_donation`` (PR #78) for stored
        compute fields, which Odoo 14 flushes by calling
        ``_write()`` directly rather than ``write()``.  Invalidating
        the cache before ``write()`` forces
        ``_prepare_donation_fund_usage()``'s read of
        ``realized_amount`` (untouched by this write) to miss the
        cache; the resulting ``_read()`` flushes this record's other
        pending column values through the overridden ``_write()``,
        which re-enters ``_donation_fund_usage_refresh()`` and
        creates the ledger row while the outer call still holds the
        empty ``usage`` recordset it captured before that reentrant
        call ran. On the old code the outer call then creates a
        second row for the same ``(model_id, res_id)``, raising the
        unique constraint's ``IntegrityError``; the fix re-fetches
        ``usage`` after ``_prepare_donation_fund_usage()`` runs, so
        the outer call sees the row the reentrant call already
        created and updates it instead of creating a duplicate.
        """
        if "test.donation_fund_consumer_rewrite" not in self.env:
            self.skipTest(
                "Model 'test.donation_fund_consumer_rewrite' is not "
                "available - module 'test_ssi_donation' is not "
                "installed."
            )
        analytic_account = self.env["account.analytic.account"].create(
            {"name": "Test Consumer Analytic Reentrancy"}
        )
        fund = self.env["donation_fund"].create(
            {
                "name": "Test Fund Reentrancy",
                "code": "TDONU102",
                "analytic_account_id": analytic_account.id,
            }
        )
        consumer = self.env["test.donation_fund_consumer_rewrite"].create(
            {"name": "Doc Consumer Reentrancy", "state": "draft"}
        )
        consumer.invalidate_cache()
        consumer.write(
            {
                "state": "done",
                "committed_amount": 100.0,
                "donation_fund_id": fund.id,
            }
        )
        usage_rows = (
            self.env["donation_fund_usage"]
            .sudo()
            .search(
                [
                    (
                        "model_id.model",
                        "=",
                        "test.donation_fund_consumer_rewrite",
                    ),
                    ("res_id", "=", consumer.id),
                ]
            )
        )
        self.assertEqual(len(usage_rows), 1)
        self.assertEqual(usage_rows.amount_committed, 100.0)

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
