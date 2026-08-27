# Create Donation Type

> **Module:** ssi_donation\
> **Model:** `donation_type`\
> **Menu:** Donation > Configuration > Donation Types\
> **Actor:** user in group `Donation Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** An `account.journal` exists to use as Journal.
- **Data:** An `account.account` exists to use as Income Account.
- **Data:** An `account.account` exists to use as Receivable Account.
- **Access:** User is in group `Donation Type`.

## Flow

1. Open the **Donation > Configuration > Donation Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the type (e.g. "Cash Donation").
   - **Code** _(required)_: Enter a unique code identifying this type, or enter **/** to
     assign it later using **Generate Code**.
   - **Journal** _(required)_: Select the `account.journal` the donation receipt
     document of this type is posted through.
   - **Income Account** _(required)_: Select the contribution revenue `account.account`
     credited when a donation of this type is received.
   - **Receivable Account** _(required)_: Select the contribution receivable
     `account.account` debited when a donation of this type is recorded as a pledge.
   - Optionally, select one or more **Allowed Funds**. Leave empty to allow every
     `donation_fund`.
4. Open the **Restriction Release** tab to configure how a donor restriction under this
   type is released. This is optional, but the three fields form one package: filling in
   one of them requires filling in all three.
   - **Release Journal**: Select the `account.journal` used to post the net asset
     reclassification entry. It cannot be a Cash or Bank journal.
   - **Net Assets Released From Restriction Account**: Select the debit-side
     `account.account` of the release entry.
   - **Net Assets Reclassified Without Donor Restriction Account**: Select the
     credit-side `account.account` of the release entry.
5. Open the **Donor** tab to see which donors this type may be used with. **Partner
   Selection Method** _(required)_ defaults to **Domain** with an empty **Partner
   Domain** (matches every donor) — leave it as-is to allow every donor, or change it:
   - **Manual**: fill in **Partners**.
   - **Domain**: fill in **Partner Domain**.
   - **Python Code**: fill in **Partner Python Code**.
6. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `donation_type`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
7. Click **Save**.

## Post-Condition

- A new Donation Type record is created and active.
- The three Restriction Release fields are either all filled or all empty.
