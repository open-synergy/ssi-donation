# Create Donation Restriction Release

> **Module:** ssi_donation\
> **Model:** `donation_restriction_release`\
> **Menu:** Donation > Restriction Releases\
> **Actor:** user in group `User` (`donation_restriction_release_user_group`)

## Pre-Condition

- **Data:** A `donation_type` exists, fully configured for release: Release Journal, Net
  Assets Released From Restriction Account, and Net Assets Reclassified Without Donor
  Restriction Account all filled.
- **Data:** A `donation_fund` exists with Restriction Type **With Donor Restriction**,
  and its Releasable Amount (Amount Realized minus Amount Released) is greater than
  zero. Amount Realized is populated by that Fund's usage records from a consumer
  document (`ssi_donation` does not ship a consumer document itself).
- **Access:** User is in group `User`.

## Flow

1. Open the **Donation > Restriction Releases** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type** _(required)_: Select the `donation_type` this release is recorded under.
     Selecting a Type automatically fills in **Journal**, **Debit Account**, and
     **Credit Account** from the Type's release configuration.
   - **Fund** _(required)_: Select the donor-restricted `donation_fund` this release
     reclassifies net assets for.
   - **Amount** _(required)_: Enter the amount to release from restriction. Must be
     greater than zero and must not exceed the selected Fund's Releasable Amount.
   - **Date** _(required)_: Defaults to today; change if the release should be recorded
     on a different accounting date.
   - **Journal** _(required)_: Defaulted from the selected Type; may be overridden while
     still in Draft.
   - **Debit Account** _(required)_: Defaulted from the selected Type; may be overridden
     while still in Draft.
   - **Credit Account** _(required)_: Defaulted from the selected Type; may be
     overridden while still in Draft.
4. Optionally, fill in **Note** with any free-form remark about the release.
5. Click **Save**.

## Post-Condition

- A new Donation Restriction Release record is created in **Draft** status.
- **Releasable Amount** and **Analytic Account** are shown read-only, copied from the
  selected Fund.
