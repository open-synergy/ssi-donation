# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinDonationFundConsumer(models.AbstractModel):
    """
    Generic wiring point for any model that draws committed or
    realized money out of a ``donation_fund``.

    A model inherits this mixin and sets the ``_donation_*`` class
    attributes to name its own fields; the mixin then keeps a single
    ``donation_fund_usage`` ledger row for each of its records in
    sync on ``create``/``write``/``unlink``. ``donation_fund`` totals
    ``amount_committed``/``amount_realized`` from that ledger, so it
    never has to know the name of any consumer model -- a new
    fund-consuming feature only needs to inherit this mixin and set
    a handful of attributes, without ``donation_fund`` or this
    module changing at all.
    """

    _name = "mixin.donation_fund_consumer"
    _description = "Donation Fund Consumer Mixin"

    _donation_committed_field_name = False
    _donation_realized_field_name = False
    _donation_state_field_name = "state"
    _donation_committed_states = ("open", "done")

    donation_fund_id = fields.Many2one(
        string="Donation Fund",
        comodel_name="donation_fund",
        ondelete="restrict",
        help="Donation fund this record draws committed/realized "
        "money from. Leave empty when this record does not use any "
        "Donation Fund.",
    )
    donation_analytic_account_id = fields.Many2one(
        string="Donation Analytic Account",
        comodel_name="account.analytic.account",
        related="donation_fund_id.analytic_account_id",
        store=True,
        compute_sudo=True,
        help="Analytic account of Donation Fund, exposed here so "
        "this record can be filtered/reported on the same "
        "dimension its Donation Fund is bound to.",
    )

    @api.model
    def create(self, vals):
        """Create the record, then sync its Donation Fund ledger row.

        Overridden so every model that inherits this mixin gets its
        ``donation_fund_usage`` ledger row for free, without writing
        a single line of wiring code itself.

        :param vals: values for the new record
        :return: the newly created record
        """
        record = super().create(vals)
        record.sudo()._donation_fund_usage_refresh()
        return record

    def write(self, vals):
        """Write the record, then re-sync its ledger row if relevant.

        Only refreshes the ledger row when a field that feeds it
        actually changed (``donation_fund_id``, or the committed/
        realized/state field named by this model's ``_donation_*``
        attributes), so unrelated writes stay cheap.

        :param vals: values to write
        :return: True, as returned by the base ``write``
        """
        relevant_fields = self._donation_fund_usage_relevant_fields()
        should_refresh = any(field_name in vals for field_name in relevant_fields)
        result = super().write(vals)
        if should_refresh:
            self.sudo()._donation_fund_usage_refresh()
        return result

    def unlink(self):
        """Delete the record's ledger row, then the record itself.

        The ledger row is removed first so ``donation_fund`` never
        totals a usage row for a consumer record that no longer
        exists.

        :return: True, as returned by the base ``unlink``
        """
        self.sudo()._donation_fund_usage_unlink()
        return super().unlink()

    def _donation_fund_usage_relevant_fields(self):
        """List the fields whose change should refresh the ledger row.

        :return: a list of field names declared on this model
        """
        result = ["donation_fund_id"]
        for field_name in (
            self._donation_committed_field_name,
            self._donation_realized_field_name,
            self._donation_state_field_name,
        ):
            if field_name:
                result.append(field_name)
        return result

    def _donation_fund_usage_model(self):
        """Look up the ``ir.model`` record naming this model.

        :return: an ``ir.model`` recordset, empty if not found
        """
        return self.env["ir.model"].sudo().search([("model", "=", self._name)], limit=1)

    def _donation_fund_usage_unlink(self):
        """Delete this record's ``donation_fund_usage`` row, if any.

        :return: nothing
        """
        model = self._donation_fund_usage_model()
        if not model:
            return
        Usage = self.env["donation_fund_usage"].sudo()  # pylint: disable=invalid-name
        Usage.search(
            [
                ("model_id", "=", model.id),
                ("res_id", "in", self.ids),
            ]
        ).unlink()

    def _donation_fund_usage_refresh(self):
        """Create/update/delete this record's ``donation_fund_usage`` row.

        Deletes the row when ``donation_fund_id`` is empty; otherwise
        creates or updates the single row keyed by ``(model_id,
        res_id)`` with the committed/realized amounts and state read
        off this record through the ``_donation_*_field_name``
        attributes. Runs under ``sudo()`` from the caller so a user
        without direct write access to ``donation_fund_usage`` can
        still trigger this through an ordinary document edit.

        :return: nothing
        """
        Usage = self.env["donation_fund_usage"].sudo()  # pylint: disable=invalid-name
        model = self._donation_fund_usage_model()
        for record in self:
            usage = Usage.search(
                [
                    ("model_id", "=", model.id),
                    ("res_id", "=", record.id),
                ],
                limit=1,
            )
            if not record.donation_fund_id:
                usage.unlink()
                continue
            values = record._prepare_donation_fund_usage()
            if usage:
                usage.write(values)
            else:
                values.update(
                    {
                        "model_id": model.id,
                        "res_id": record.id,
                    }
                )
                Usage.create(values)

    def _prepare_donation_fund_usage(self):
        """Build the ``donation_fund_usage`` values for this record.

        Reads the committed/realized amounts and state off this
        record through the ``_donation_*_field_name`` attributes. An
        attribute left at its default ``False`` yields zero, not an
        error. The committed amount is zeroed out when this record's
        state is outside ``_donation_committed_states``, so
        ``donation_fund.amount_committed`` never needs to know any
        consumer model's own state machine.

        :return: dict of ``donation_fund_usage`` values, without
            ``model_id``/``res_id``
        """
        self.ensure_one()
        state = False
        if self._donation_state_field_name:
            state = getattr(self, self._donation_state_field_name, False)
        committed = 0.0
        if self._donation_committed_field_name and (
            state in self._donation_committed_states
        ):
            committed = getattr(self, self._donation_committed_field_name)
        realized = 0.0
        if self._donation_realized_field_name:
            realized = getattr(self, self._donation_realized_field_name)
        return {
            "fund_id": self.donation_fund_id.id,
            "state": state or False,
            "amount_committed": committed,
            "amount_realized": realized,
            "company_id": self.env.company.id,
            "currency_id": self.env.company.currency_id.id,
        }
