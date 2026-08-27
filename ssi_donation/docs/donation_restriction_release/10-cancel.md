# Cancel Donation Restriction Release

> **Module:** ssi_donation\
> **Model:** `donation_restriction_release`\
> **Menu:** Donation > Restriction Releases\
> **Actor:** user in group `Validator` (`donation_restriction_release_validator_group`)\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User has _Can Cancel_ access right.

## Flow

1. Open the **Donation > Restriction Releases** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the release was **Done**, its journal entry is deleted, the **Move** field is
  cleared, and the Fund's **Amount Released** decreases by this release's Amount.
