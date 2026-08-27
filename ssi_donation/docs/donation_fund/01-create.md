# Create Donation Fund

> **Module:** ssi_donation\
> **Model:** `donation_fund`\
> **Menu:** Donation > Configuration > Donation Funds\
> **Actor:** user in group `Donation Fund`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** An `account.analytic.account` exists to bind this fund to, and is not yet
  bound to another Donation Fund.
- **Data:** An `account.account` exists to use as Net Asset Account, if the fund will be
  created with a donor restriction.
- **Access:** User is in group `Donation Fund`.

## Flow

1. Open the **Donation > Configuration > Donation Funds** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the fund (e.g. "Alumni Scholarship
     Endowment 2026").
   - **Code** _(required)_: Enter a unique code identifying this fund, or enter **/** to
     assign it later using **Generate Code**.
   - **Analytic Account** _(required)_: Select the `account.analytic.account` this fund
     is bound to. An analytic account already bound to another Donation Fund cannot be
     selected again.
   - **Restriction Type** _(required)_: Select **With Donor Restriction** to record a
     donor-imposed condition on this fund, or leave the default **Without Donor
     Restriction**.
4. When **Restriction Type** is **With Donor Restriction**:
   - **Restriction Note** _(required)_: Enter the donor's restriction terms.
   - **Net Asset Account** _(required)_: Select the `account.account` this fund's
     balance is carried on.
   - Optionally, fill in **Restriction Start Date** and **Restriction End Date** to
     bound the restriction to a time window. If both are filled, the End Date cannot be
     earlier than the Start Date.
5. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `donation_fund`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
6. Click **Save**.

## Post-Condition

- A new Donation Fund record is created and active.
- **Amount Received**, **Amount Committed**, **Amount Realized**, and **Amount
  Available** are all **0.00** — these are computed from documents that do not exist yet
  and are wired up in a later item.
