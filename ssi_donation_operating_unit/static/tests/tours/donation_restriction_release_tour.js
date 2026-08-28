// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation_operating_unit.donation_restriction_release_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/donation_restriction_release/01-create.md (E1 delta --
    // Additional Fields). Navigation (open menu -> New) is taken from
    // the base IK ssi_donation/docs/donation_restriction_release/
    // 01-create.md Flow steps 1-2. "Restriction Releases" is NOT the
    // lowest-sequence child of the app root ("Donations" is), so the
    // ordinary breadcrumb-title gate applies -- no stale-marker trick
    // needed here (unlike the ``donation`` tour above).
    tour.register(
        "ssi_donation_operating_unit_donation_restriction_release_create",
        {
            test: true,
            url: "/web",
        },
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Donation app",
                trigger: '.o_app[data-menu-xmlid="ssi_donation.menu_donation_root"]',
            },
            {
                content: "Open the Restriction Releases menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_donation.donation_restriction_release_menu"]',
            },
            {
                content: "Restriction Releases list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Restriction Releases)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // -- Base Flow 2 -- Click the New button. (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // -- Delta assertion -- the Operating Unit field is
            // visible on the create form, editable (Draft state), and
            // already filled with a default value (not
            // `.o_field_empty`).
            {
                content:
                    "Operating Unit field is visible, editable, and " +
                    "filled with a default",
                trigger:
                    ".o_form_view.o_form_editable " +
                    ".o_field_widget.o_field_many2one[name='operating_unit_id']" +
                    ":not(.o_field_empty)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
