# Restart Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user in group `Validator` (`donation_validator_group`)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Donation > Donations** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
