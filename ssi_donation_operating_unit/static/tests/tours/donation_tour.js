// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation_operating_unit.donation_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/donation/01-create.md (E1 delta -- Additional Fields)
    // Navigation (open menu -> New) is taken from the base IK
    // ssi_donation/docs/donation/01-create.md Flow steps 1-2 -- see
    // scope-and-boundaries.md skill odoo-development-ui-test §1 ("Backing
    // dua-file: tour extension = base IK ∪ delta IK"). The delta assertion
    // comes from this module's own IK: the Operating Unit field is visible
    // on the create form AND already filled with the acting user's default
    // operating unit, for a user in the operating_unit.group_multi_operating_unit
    // group. The tour stops there; it does not fill the remaining fields,
    // save, or confirm (E1 delta-only).
    tour.register(
        "ssi_donation_operating_unit_donation_create",
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
                content: "Open the Donations menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_donation.donation_menu"]',
                run: function (actions) {
                    // Stale-marker gate: "Donations" is the lowest-sequence
                    // child of the app root, so opening the app already
                    // lands on it -- this click reloads the SAME action
                    // (skill odoo-development-ui-test patterns.md §T).
                    $(".o_control_panel").addClass("oe_tour_stale");
                    actions.click();
                },
            },
            {
                content: "Donations action is (re)mounted",
                trigger: ".o_control_panel:not(.oe_tour_stale)",
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

            // -- Delta assertion -- the Operating Unit field is visible on
            // the create form, editable (Draft state), and already filled
            // with a default value (not `.o_field_empty`).
            {
                content:
                    "Operating Unit field is visible, editable, and filled with a default",
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
