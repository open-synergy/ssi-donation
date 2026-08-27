# Approve Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user registered as approver on the pending approval level, via the\
> **Standard** approval template, group `Validator` (`donation_validator_group`)\
> **State:** `confirm` → `done` (when this is the final pending approval level)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The **Standard** approval template shipped with this module has a single
  level, approved by any member of group `Validator` — so approving is always the final
  level unless the template has been reconfigured with more levels.
- **Access:** User has _Can Approve_ access right.

## Flow

1. Open the **Donation > Donations** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If this was the final pending approval level, this donation has no separate "Done"
  button to click: the system transitions status directly to **Done** as part of the
  same Approve action, and:
  - A balanced two-line journal entry is created and posted in the selected Journal,
    crediting the Income Account and debiting the Debit Account (see `01-create.md`).
    The credit line carries the selected Fund's Analytic Account; the debit line carries
    no analytic account.
  - The **Move** field on the form is filled in with the created journal entry, and
    clicking it opens that `account.move` record.
