# Approve Donation Restriction Release

> **Module:** ssi_donation\
> **Model:** `donation_restriction_release`\
> **Menu:** Donation > Restriction Releases\
> **Actor:** user registered as approver on the pending approval level, via the\
> **Standard** approval template, group `Validator`
> (`donation_restriction_release_validator_group`)\
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

1. Open the **Donation > Restriction Releases** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If this was the final pending approval level, this release has no separate "Done"
  button to click: the system transitions status directly to **Done** as part of the
  same Approve action, and:
  - A balanced two-line journal entry is created and posted in the selected Journal,
    debiting the Debit Account and crediting the Credit Account (see `01-create.md`).
    Both lines carry the selected Fund's Analytic Account, since a restriction release
    never adds or removes money from the Fund — only its net asset classification
    changes.
  - The **Move** field on the form is filled in with the created journal entry, and
    clicking it opens that `account.move` record.
  - The Fund's **Amount Released** increases by this release's Amount.
  - The Fund's **Amount Available** does **not** change. A restriction release only
    reclassifies net assets already realized by the Fund's consumer documents; it does
    not add, remove, or commit any money — this is the detail most often confused with a
    release affecting how much of the Fund's money is still available to commit.
