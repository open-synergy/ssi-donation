// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation.donation_fund_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/donation_fund/01-create.md
    tour.register(
        "ssi_donation_donation_fund_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Donation > Configuration > Donation
            // Funds menu. "Configuration" is a level-2 section menu
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
                content: "Open the Donation Funds menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_donation.donation_fund_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang --
                // bukan sekadar "ada list di layar" (patterns.md §A).
                content: "Donation Funds list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Donation Funds)",
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
            // Analytic Account, Restriction Type. Code is left as "/"
            // so Flow 5 (Generate Code) has an effect. Restriction
            // Type is switched to "With Donor Restriction" so Flow 4
            // is exercised too.
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR Donation Fund Create",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },
            {
                content: "Select the Analytic Account",
                trigger: ".o_field_many2one[name='analytic_account_id'] input",
                run: "text TOUR Donation Fund Analytic",
            },
            {
                content: "Pick the Analytic Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Fund Analytic)",
                in_modal: false,
            },
            {
                content: "Switch Restriction Type to With Donor Restriction",
                trigger: "select.o_field_widget[name='restriction_type']",
                run: "text With Donor Restriction",
            },

            // ── Flow 4 — Restriction Type is "With Donor Restriction":
            // fill in the Restriction Note and Net Asset Account that
            // become visible/required.
            {
                content: "Fill in the Restriction Note",
                trigger: ".o_field_widget[name='restriction_note']",
                run: "text Only for scholarship disbursement.",
            },
            {
                content: "Select the Net Asset Account",
                trigger: ".o_field_many2one[name='net_asset_account_id'] input",
                run: "text TOUR Donation Fund Net Asset Account",
            },
            {
                content: "Pick the Net Asset Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Donation Fund Net Asset Account)",
                in_modal: false,
            },

            // ── Flow 5 — Click Generate Code in the header to
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

            // ── Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — a new Donation Fund record is
            // created and active.
            {
                content: "Record is saved",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR Donation Fund Create)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
