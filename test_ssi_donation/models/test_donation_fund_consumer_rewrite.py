# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestDonationFundConsumerRewrite(models.Model):
    """
    Fourth fixture model exercising ``mixin.donation_fund_consumer``,
    reproducing a consumer that overrides the private ``_write()``
    method rather than the public ``write()``.

    Overriding ``_write()`` is a legitimate, real-world pattern --
    used by ``ssi_school_scholarship_donation``'s
    ``school_scholarship_funding_source`` because Odoo 14's
    ``Model.flush()`` recomputes/flushes stored fields by calling
    ``_write()`` directly, never ``write()`` (``odoo/models.py``).
    Whenever ``_donation_fund_usage_refresh()`` reads a field of
    this record that is not yet in cache while some of its column
    values are still pending in ``env.all.towrite``, the ensuing
    flush reaches the database through this override instead of
    through the mixin's own ``write()`` override -- exactly as it
    does for that real consumer.
    """

    _name = "test.donation_fund_consumer_rewrite"
    _description = "Test Donation Fund Consumer - Write Override"
    _inherit = ["mixin.donation_fund_consumer"]

    _donation_committed_field_name = "committed_amount"
    _donation_realized_field_name = "realized_amount"

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    committed_amount = fields.Monetary(
        string="Committed Amount",
        currency_field="currency_id",
    )
    realized_amount = fields.Monetary(
        string="Realized Amount",
        currency_field="currency_id",
    )

    def _write(self, vals):
        """Write raw column values, then refresh the donation ledger.

        Reproduces the ``_write()``-override pattern real consumers
        use when their committed/realized amount is a stored
        compute field: Odoo 14's ``Model.flush()`` recomputes such
        fields by calling ``_write()`` directly, bypassing the
        mixin's own ``write()`` override entirely, so ``_write()``
        is the only hook that observes that flush.

        :param vals: raw column values being written
        :return: True, as returned by the base ``_write``
        """
        result = super()._write(vals)
        self.sudo()._donation_fund_usage_refresh()
        return result
