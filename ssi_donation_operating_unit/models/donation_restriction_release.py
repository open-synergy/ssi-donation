# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DonationRestrictionRelease(models.Model):
    """
    Extends Donation Restriction Release with single operating unit
    support, restricting each release to one operating unit and
    propagating that operating unit to the ``account.move`` header and
    both of its journal items (debit and credit) posted when the
    release reaches Done.
    """

    _name = "donation_restriction_release"
    _inherit = [
        "donation_restriction_release",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    def _prepare_standard_move(self):
        """Add ``operating_unit_id`` to the ``account.move`` header values.

        Extends ``mixin.account_move``'s ``_prepare_standard_move()``:
        the move created for this release carries the same Operating
        Unit as the release itself. The release is the sole source of
        truth for this value, so an empty ``operating_unit_id`` is
        copied through empty as well -- no guard.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        res = super()._prepare_standard_move()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _prepare_standard_ml(self, direction):
        """Add ``operating_unit_id`` to the debit/credit line values.

        Extends ``mixin.account_move_double_line``'s
        ``_prepare_standard_ml(direction)``: both the debit and the
        credit journal item generated for this release carry the same
        Operating Unit as the release itself.

        :param direction: either ``"debit"`` or ``"credit"``
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_standard_ml(direction)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
