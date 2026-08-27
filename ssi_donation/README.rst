.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========
Donation
========

Manages donations: the donation fund (a wadah of donated money bound to a single
analytic account, together with whether the donor restricted how that money may be
used per PSAK 45 / ISAK 35), the donation type (accounting configuration a receipt
is posted under), and the donation document itself, which records the receipt of a
donation from a donor and, once Done, posts its own balanced journal entry crediting
the fund's analytic account.


Work Instruction
================

Donation Fund
-------------

* `Create Donation Fund <docs/donation_fund/01-create.html>`_

Donation Type
-------------

* `Create Donation Type <docs/donation_type/01-create.html>`_

Donation Document
------------------

* `Create Donation <docs/donation/01-create.html>`_
* `Confirm Donation <docs/donation/04-confirm.html>`_
* `Approve Donation <docs/donation/05-approve.html>`_
* `Reject Donation <docs/donation/06-reject.html>`_
* `Cancel Donation <docs/donation/10-cancel.html>`_
* `Restart Donation <docs/donation/12-restart.html>`_
* `Reset Document Number Donation <docs/donation/13-reset-number.html>`_
* `Restart Approval Process Donation <docs/donation/14-restart-approval.html>`_

Donation Restriction Release
-----------------------------

* `Create Donation Restriction Release <docs/donation_restriction_release/01-create.html>`_
* `Confirm Donation Restriction Release <docs/donation_restriction_release/04-confirm.html>`_
* `Approve Donation Restriction Release <docs/donation_restriction_release/05-approve.html>`_
* `Cancel Donation Restriction Release <docs/donation_restriction_release/10-cancel.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-donation
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Donation*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-donation/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
