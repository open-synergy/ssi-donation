# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DonationType(models.Model):
    """
    Represents a mechanism donations of a given kind are received and
    booked through (e.g. cash, transfer, pledge). ``donation_fund``
    only carries the analytic dimension and the donor restriction
    terms of a fund; it deliberately holds no accounting
    configuration, because the same fund can receive money through
    several mechanisms whose journals and accounts differ. This model
    is the missing piece: it holds the journal and accounts a
    donation receipt document of this type posts to, the journal and
    account pair used when a donor restriction is later released, and
    which funds/donors this type may be used with.
    """

    _name = "donation_type"
    _inherit = [
        "mixin.master_data",
        "mixin.company_currency",
        "mixin.res_partner_m2o_configurator",
    ]
    _description = "Donation Type"
    _order = "name, id"

    _res_partner_m2o_configurator_insert_form_element_ok = True
    _res_partner_m2o_configurator_form_xpath = "//page[@name='donor']"

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        ondelete="restrict",
        help="Journal the donation receipt document of this type is " "posted through.",
    )
    income_account_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        help="Contribution revenue account credited when a donation of "
        "this type is received.",
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        help="Contribution receivable account debited when a donation "
        "of this type is recorded as a pledge, before the cash is "
        "actually received.",
    )
    release_journal_id = fields.Many2one(
        string="Release Journal",
        comodel_name="account.journal",
        ondelete="restrict",
        help="Journal used to post the net asset reclassification entry "
        "when a donor restriction under this type is released. Must "
        "not be a Cash or Bank journal — releasing a restriction "
        "never involves an actual cash movement.",
    )
    net_asset_released_account_id = fields.Many2one(
        string="Net Assets Released From Restriction Account",
        comodel_name="account.account",
        ondelete="restrict",
        help="Debit side account of the restriction release entry.",
    )
    net_asset_reclassified_account_id = fields.Many2one(
        string="Net Assets Reclassified Without Donor Restriction " "Account",
        comodel_name="account.account",
        ondelete="restrict",
        help="Credit side account of the restriction release entry.",
    )
    allowed_fund_ids = fields.Many2many(
        string="Allowed Funds",
        comodel_name="donation_fund",
        relation="rel_donation_type_2_fund",
        column1="type_id",
        column2="fund_id",
        help="Donation funds this type may be used with. Leave empty "
        "to allow every fund.",
    )

    @api.constrains("release_journal_id")
    def _check_release_journal_id(self):
        """Forbid a Cash or Bank journal as the Release Journal.

        Releasing a donor restriction only reclassifies net assets
        between two accounts — it never involves an actual cash
        movement, so posting it through a Cash or Bank journal would
        wrongly imply money moved.

        :raises ValidationError: when ``release_journal_id.type`` is
            ``cash`` or ``bank``.
        """
        for record in self:
            if record.release_journal_id and record.release_journal_id.type in (
                "cash",
                "bank",
            ):
                error_message = """
Document Type: %s
Context: Configure release journal
Database ID: %s
Problem: Release Journal is a Cash or Bank journal
Solution: Select a journal that is not of type Cash or Bank
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains(
        "release_journal_id",
        "net_asset_released_account_id",
        "net_asset_reclassified_account_id",
    )
    def _check_release_fields_complete(self):
        """Require the three release fields to be filled as one package.

        Release Journal, Net Assets Released From Restriction Account,
        and Net Assets Reclassified Without Donor Restriction Account
        together configure how a restriction release is booked. A
        type only partially configured for release must not reach a
        release document, so it is rejected here instead.

        :raises ValidationError: when at least one of the three
            fields is filled but not all three are.
        """
        for record in self:
            release_fields = (
                record.release_journal_id,
                record.net_asset_released_account_id,
                record.net_asset_reclassified_account_id,
            )
            filled_count = len([field for field in release_fields if field])
            if filled_count not in (0, len(release_fields)):
                error_message = """
Document Type: %s
Context: Configure restriction release
Database ID: %s
Problem: Release Journal, Net Assets Released From Restriction
Account, and Net Assets Reclassified Without Donor Restriction
Account must be filled together
Solution: Fill in all three release fields, or leave all three empty
""" % (
                    self._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
