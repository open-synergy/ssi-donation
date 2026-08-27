# Create Donation

> **Module:** ssi_donation\
> **Model:** `donation`\
> **Menu:** Donation > Donations\
> **Actor:** user in group `User` (`donation_user_group`)

## Pre-Condition

- **Data:** A `donation_type` exists, configured with a Journal, Income Account, and
  Receivable Account.
- **Data:** A `donation_fund` exists that is either not restricted to specific Types, or
  whose Type list includes the Type that will be selected.
- **Data:** A `res.partner` exists to record as the Donor.
- **Access:** User is in group `User`.

## Flow

1. Open the **Donation > Donations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date** _(required)_: Defaults to today; change if the donation was received on a
     different date.
   - **Donor** _(required)_: Select the `res.partner` this donation is received from.
   - **Type** _(required)_: Select the `donation_type` this receipt is recorded under.
     Selecting a Type automatically fills in **Journal** and **Income Account** from the
     Type's configuration.
   - **Fund** _(required)_: Select the `donation_fund` the money is received into. If
     the Type's Allowed Funds list is not empty, the Fund must be one of them.
   - **Amount** _(required)_: Enter the amount donated. Must be greater than zero.
   - **Receipt Method** _(required)_: Defaults to **Cash Received**. Switch to **Pledge
     / Receivable** if the donor has committed to pay but the cash has not arrived yet.
   - **Journal** _(required)_: Defaulted from the selected Type; may be overridden while
     still in Draft.
   - **Income Account** _(required)_: Defaulted from the selected Type; may be
     overridden while still in Draft.
4. Optionally, fill in **Note** with any free-form remark about the donation.
5. Click **Save**.

## Post-Condition

- A new Donation record is created in **Draft** status.
- **Debit Account** is filled in automatically: the Journal's own default account when
  Receipt Method is **Cash Received**, or the Type's Receivable Account when Receipt
  Method is **Pledge / Receivable**.
- **Analytic Account** and **Restriction Type** are copied from the selected Fund and
  shown read-only.
