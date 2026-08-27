# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DonationFundUsage(models.Model):
    """
    One ledger row recording the committed/realized money a single
    consumer record draws from a ``donation_fund``.

    Rows are created, updated, and deleted exclusively by
    ``mixin.donation_fund_consumer`` (through ``sudo()``) as its
    inheriting models' records change -- never directly by a user
    (see the module's ACL). The pair (``model_id``, ``res_id``)
    names the consumer record without this model ever importing or
    referencing that model's name, which is what lets
    ``donation_fund.amount_committed``/``amount_realized`` total
    contributions from any number of unrelated consumer models.
    """

    _name = "donation_fund_usage"
    _description = "Donation Fund Usage"
    _order = "fund_id, model_id, res_id"

    fund_id = fields.Many2one(
        string="Donation Fund",
        comodel_name="donation_fund",
        required=True,
        ondelete="restrict",
        help="Donation fund this usage row draws committed/realized "
        "money from. Restricted (not cascaded) so a fund still "
        "referenced by a live consumer record cannot be deleted "
        "out from under it -- consistent with how ``donation`` "
        "itself points back to this fund.",
    )
    model_id = fields.Many2one(
        string="Consumer Model",
        comodel_name="ir.model",
        required=True,
        ondelete="cascade",
        help="Model of the consumer record that owns this usage row.",
    )
    res_id = fields.Integer(
        string="Consumer Record ID",
        required=True,
        help="Database ID of the consumer record that owns this "
        "usage row, on the model named by Consumer Model.",
    )
    state = fields.Char(
        string="Consumer State",
        help="State value copied as-is from the consumer record, "
        "kept for reference/filtering only -- it does not by "
        "itself decide whether Amount Committed counts toward the "
        "fund's total; that filtering already happened when this "
        "row's Amount Committed was last written.",
    )
    amount_committed = fields.Monetary(
        string="Amount Committed",
        currency_field="currency_id",
        help="Amount committed by the consumer record, zeroed out "
        "whenever its state falls outside the consumer model's "
        "own ``_donation_committed_states``.",
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="currency_id",
        help="Amount already realized (actually spent) by the " "consumer record.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        help="Company of the consumer record, copied at write time.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
        help="Currency Amount Committed/Realized are expressed in.",
    )

    _sql_constraints = [
        (
            "model_res_id_uniq",
            "unique(model_id, res_id)",
            "A consumer record may only have one Donation Fund Usage row.",
        ),
    ]
