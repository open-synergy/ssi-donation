# Restart Approval Process Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user in group `Validator` (`donation_validator_group`)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `restart_approval_ok` to the actor's
  group. The **Standard** template shipped with this module additionally requires the
  record's **Approval Template** to be **empty** — this action is meant to recover a
  record whose approval process has no template assigned, not to re-run an
  already-working one.
- **Access:** User has _Can Restart Approval Process_ access right.

## Flow

1. Open the **Donation > Donations** menu.
2. Open the record whose approval process will be restarted.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Any existing approval records for this document are removed.
- The approval process is requested again: an **Approval Template** is matched and new
  approval records are created for each of its approver levels, same as `04-confirm`.
