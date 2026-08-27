// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation.donation_restriction_release_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // ── Shared Flow 1 — Open the Donation > Restriction Releases menu.
    //
    // "Restriction Releases" is NOT the lowest-sequence child of the app
    // root ("Donations" is, sequence 10 vs 20), so opening the app lands
    // on "Donations" first and this click mounts a genuinely different
    // action -- the ordinary breadcrumb-title gate applies, no
    // stale-marker trick needed (unlike ssi_donation.donation_tour).
    function openRestrictionReleasesMenu() {
        return [
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
        ];
    }

    // IK: docs/donation_restriction_release/01-create.md
    tour.register(
        "ssi_donation_donation_restriction_release_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openRestrictionReleasesMenu(), [
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

            // ── Flow 3 — Fill in the required fields: Type, Fund,
            // Amount. Date is left at its default (today). Journal,
            // Debit Account, and Credit Account are left at the
            // values Type defaults them to.
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour Restriction Release Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Restriction Release Type)",
                in_modal: false,
            },
            {
                content: "Select the Fund",
                trigger: ".o_field_many2one[name='fund_id'] input",
                run: "text Tour Restriction Release Create Fund",
            },
            {
                content: "Pick the Fund from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Restriction Release Create Fund)",
                in_modal: false,
            },
            {
                content: "Fill in the Amount",
                trigger: ".o_field_widget[name='amount'] input",
                run: "text 40000",
            },

            // ── Flow 4 — Optionally fill in Note.
            {
                content: "Fill in the Note",
                trigger: ".o_field_widget[name='note']",
                run: "text Tour release created by the create tour.",
            },

            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — a new Donation Restriction Release
            // record is created in Draft. The record has no
            // distinctive display name yet (its document number is
            // only assigned at Done), so the gate is the generic
            // "record persisted" one.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation_restriction_release/04-confirm.md
    tour.register(
        "ssi_donation_donation_restriction_release_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openRestrictionReleasesMenu(), [
            // ── Flow 2 — Open the record to confirm.
            {
                content: "Open the release to confirm",
                trigger:
                    ".o_data_row:contains(Tour Restriction Release Confirm Fund) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to Waiting for
            // Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation_restriction_release/05-approve.md
    tour.register(
        "ssi_donation_donation_restriction_release_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openRestrictionReleasesMenu(), [
            // ── Flow 2 — Open the record to approve.
            {
                content: "Open the release to approve",
                trigger:
                    ".o_data_row:contains(Tour Restriction Release Approve Fund) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — the Standard approval template has
            // a single level, so this Approve click is always the
            // final one: status goes straight to Done and the Move
            // field is filled in by the same action. Tour does not
            // assert amounts/balances -- that is unit test territory
            // (skill odoo-development-ui-test).
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // ``move_id`` is a readonly many2one; once filled in
                // 14.0 renders it as `<a class="o_form_uri">` -- an
                // empty readonly m2o has zero size and would fail
                // this gate (skill odoo-development-ui-test
                // selectors.md, "Field readonly yang KOSONG").
                content: "Move field is filled in",
                trigger: ".o_field_widget[name='move_id'] a.o_form_uri",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation_restriction_release/10-cancel.md
    tour.register(
        "ssi_donation_donation_restriction_release_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openRestrictionReleasesMenu(), [
            // ── Flow 2 — Open the record to cancel.
            {
                content: "Open the release to cancel",
                trigger:
                    ".o_data_row:contains(Tour Restriction Release Cancel Fund) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Click the Cancel button. The button's
            // `name` attribute is a numeric action id, not
            // "action_cancel" -- :contains(Cancel) is the only
            // stable selector (skill odoo-development-ui-test
            // patterns.md §H).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            {
                // 14.0 -- do NOT prefix with `.modal`; the trigger
                // is already searched for inside the modal.
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 4 — In the wizard, select the Cancellation
            // Reason.
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Restriction Release Cancel Reason) input",
            },

            // ── Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // ── Flow 6 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
            },

            // ── Post-Condition — Status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
