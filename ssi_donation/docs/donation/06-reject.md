# Reject Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user registered as approver on the pending approval level, via the\
> **Standard** approval template, group `Validator` (`donation_validator_group`)\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `reject_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The **Standard** approval template shipped with this module has a single
  level, approved by any member of group `Validator` — so any registered approver may
  reject at that level.
- **Access:** User has _Can Reject_ access right.

## Flow

1. Open the **Donation > Donations** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- The pending approval record is marked **Rejected**.
