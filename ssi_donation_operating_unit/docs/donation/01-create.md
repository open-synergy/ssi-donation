# Create Donation

> **Module:** ssi_donation_operating_unit **Extends:** ssi_donation — model `donation`,
> aksi `01-create`

## Additional Pre-Condition

- **Module:** The `operating_unit` module is installed.
- **Data:** At least one active `operating.unit` record exists.
- **Access:** Only a user in group `operating_unit.group_multi_operating_unit` sees and
  can edit the Operating Unit field described below; a user outside that group creates
  the donation exactly as documented in the base IK, with the field hidden.

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: The operating unit this donation belongs to. Defaults to the
  creating user's default operating unit (`default_operating_unit_id`); may be changed
  while still in Draft. Becomes read-only once the donation leaves Draft.

## Modified — Record Visibility

- The Donation list is now filtered by operating unit (record rule). A user in group
  `Operating Unit` only sees donations whose Operating Unit is among the operating units
  assigned to them. This is not a Flow step.

## Additional Post-Condition

- When the donation later reaches **Done** (see base IK `ssi_donation`
  `docs/donation/05-approve.md`), the `account.move` created for it — and both of its
  journal items (debit and credit) — carries the same Operating Unit as the donation,
  regardless of the default operating unit of the user who confirms/approves it.
