# Reset Document Number — Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user in group `Validator` (`donation_validator_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` grants `manual_number_ok` for state `draft` to
  the actor's group.
- **Access:** User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Donation > Donations** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic document number when it reaches **Done**.
