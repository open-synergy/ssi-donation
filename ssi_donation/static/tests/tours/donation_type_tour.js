// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation.donation_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/donation_type/01-create.md
    tour.register(
        "ssi_donation_donation_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Donation > Configuration > Donation
            // Types menu. "Configuration" is a level-2 section menu
            // (with children), so 14.0 renders it clickable with
            // data-menu-xmlid (patterns.md skill
            // odoo-development-ui-test §A).
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Donation app",
                trigger: '.o_app[data-menu-xmlid="ssi_donation.menu_donation_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_donation.menu_donation_configuration"]',
            },
            {
                content: "Open the Donation Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_donation.donation_type_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang --
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Donation Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Donation Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 2 — Click the New button. (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Fill in the required fields: Name, Code,
            // Journal, Income Account, Receivable Account. Code is
            // left as "/" so Flow 6 (Generate Code) has an effect.
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR Donation Type Create",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },
            {
                content: "Select the Journal",
                trigger: ".o_field_many2one[name='journal_id'] input",
                run: "text TOUR Donation Type Journal",
            },
            {
                content: "Pick the Journal from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Type Journal)",
                in_modal: false,
            },
            {
                content: "Select the Income Account",
                trigger: ".o_field_many2one[name='income_account_id'] input",
                run: "text TOUR Donation Type Income Account",
            },
            {
                content: "Pick the Income Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Type Income Account)",
                in_modal: false,
            },
            {
                content: "Select the Receivable Account",
                trigger: ".o_field_many2one[name='receivable_account_id'] input",
                run: "text TOUR Donation Type Receivable Account",
            },
            {
                content: "Pick the Receivable Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Type Receivable Account)",
                in_modal: false,
            },

            // ── Flow 4 — Open the Restriction Release tab and fill
            // in the three release fields as one complete package.
            {
                content: "Open the Restriction Release tab",
                trigger: ".o_notebook .nav-link:contains(Restriction Release)",
            },
            {
                content: "Select the Release Journal",
                trigger: ".o_field_many2one[name='release_journal_id'] input",
                run: "text TOUR Donation Type Release Journal",
            },
            {
                content: "Pick the Release Journal from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Type Release Journal)",
                in_modal: false,
            },
            {
                content: "Select the Net Assets Released Account",
                trigger:
                    ".o_field_many2one[name='net_asset_released_account_id'] input",
                run: "text TOUR Net Assets Released",
            },
            {
                content: "Pick the Net Assets Released Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Net Assets Released)",
                in_modal: false,
            },
            {
                content: "Select the Net Assets Reclassified Account",
                trigger:
                    ".o_field_many2one[name='net_asset_reclassified_account_id'] input",
                run: "text TOUR Net Assets Reclassified",
            },
            {
                content: "Pick the Net Assets Reclassified Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Net Assets Reclassified)",
                in_modal: false,
            },

            // ── Flow 5 — Open the Donor tab. Partner Selection
            // Method defaults to Domain with an empty Partner Domain;
            // leaving it as-is is a valid, fully-visible state.
            {
                content: "Open the Donor tab",
                trigger: ".o_notebook .nav-link:contains(Donor)",
            },
            {
                content: "Partner Selection Method field is displayed",
                trigger: ".o_form_label:contains(Partner Selection Method)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 6 — Click Generate Code in the header to
            // automatically assign a code from the configured
            // sequence.template, since the Code field is still "/".
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Record is saved by Generate Code",
                trigger: ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 7 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — a new Donation Type record is
            // created and active.
            {
                content: "Record is saved",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR Donation Type Create)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
