// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_donation.donation_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // ── Shared Flow 1 — Open the Donation > Donations menu.
    //
    // "Donations" is the lowest-sequence child of the app root, so
    // opening the app already lands on it: clicking the "Donations"
    // menu item afterwards reloads the IDENTICAL action. That reload
    // creates nothing new in the DOM for a breadcrumb-title gate to
    // wait on, so it is gated with a stale-marker instead (skill
    // odoo-development-ui-test patterns.md §T).
    function openDonationsMenu() {
        return [
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
                    // Stale-marker gate: this click reloads the same
                    // action the app landing already shows.
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
        ];
    }

    // IK: docs/donation/01-create.md
    tour.register(
        "ssi_donation_donation_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
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

            // ── Flow 3 — Fill in the required fields: Donor, Type,
            // Fund, Amount. Date and Receipt Method are left at
            // their defaults (today / Cash Received). Journal and
            // Income Account are left at the values Type defaults
            // them to.
            {
                content: "Select the Donor",
                trigger: ".o_field_many2one[name='partner_id'] input",
                run: "text Tour Donation Create Donor",
            },
            {
                content: "Pick the Donor from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Donation Create Donor)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour Donation Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Donation Type)",
                in_modal: false,
            },
            {
                content: "Select the Fund",
                trigger: ".o_field_many2one[name='fund_id'] input",
                run: "text Tour Donation Fund",
            },
            {
                content: "Pick the Fund from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Donation Fund)",
                in_modal: false,
            },
            {
                content: "Fill in the Amount",
                trigger: ".o_field_widget[name='amount'] input",
                run: "text 100000",
            },

            // ── Flow 4 — Optionally fill in Note.
            {
                content: "Fill in the Note",
                trigger: ".o_field_widget[name='note']",
                run: "text Tour donation created by the create tour.",
            },

            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — a new Donation record is created
            // in Draft. The record has no distinctive display name
            // yet (its document number is only assigned at Done),
            // so the gate is the generic "record persisted" one.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation/04-confirm.md
    tour.register(
        "ssi_donation_donation_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
            // ── Flow 2 — Open the record to confirm.
            {
                content: "Open the donation to confirm",
                trigger:
                    ".o_data_row:contains(Tour Donation Confirm Donor) .o_data_cell:first",
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

    // IK: docs/donation/05-approve.md
    tour.register(
        "ssi_donation_donation_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
            // ── Flow 2 — Open the record to approve.
            {
                content: "Open the donation to approve",
                trigger:
                    ".o_data_row:contains(Tour Donation Approve Donor) .o_data_cell:first",
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

            // ── Post-Condition — the Standard approval template
            // has a single level, so this Approve click is always
            // the final one: status goes straight to Done and the
            // Move field is filled in by the same action.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation/10-cancel.md
    tour.register(
        "ssi_donation_donation_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
            // ── Flow 2 — Open the record to cancel.
            {
                content: "Open the donation to cancel",
                trigger:
                    ".o_data_row:contains(Tour Donation Cancel Donor) .o_data_cell:first",
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
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Donation Cancel Reason) input",
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

    // IK: docs/donation/06-reject.md
    tour.register(
        "ssi_donation_donation_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
            // ── Flow 2 — Open the record to reject.
            {
                content: "Open the donation to reject",
                trigger:
                    ".o_data_row:contains(Tour Donation Reject Donor) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/donation/12-restart.md
    tour.register(
        "ssi_donation_donation_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openDonationsMenu(), [
            // ── Flow 2 — Open the record to restart.
            {
                content: "Open the donation to restart",
                trigger:
                    ".o_data_row:contains(Tour Donation Restart Donor) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
