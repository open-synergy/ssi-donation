# Confirm Donation Restriction Release

> **Module:** ssi_donation\
> **Model:** `donation_restriction_release`\
> **Menu:** Donation > Restriction Releases\
> **Actor:** user in group `User` (`donation_restriction_release_user_group`)\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Access:** User has _Can Confirm_ access right.

## Flow

1. Open the **Donation > Restriction Releases** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
