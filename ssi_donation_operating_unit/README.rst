.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Donation + Operating Unit
=========================

This is a glue module that adds Operating Unit support to the ``donation`` and
``donation_restriction_release`` models. Users can pick an operating unit on both
documents' tree, search, and form views, editable while the document is in Draft. The
operating unit set on the document is propagated to the ``account.move`` generated when
the document reaches Done and to both of its journal items (debit and credit), keeping
the resulting journal entries scoped to the same operating unit. Visibility of both
documents is restricted per operating unit through a record rule.

Work Instruction
================

* `Create Donation <docs/donation/01-create.html>`_
* `Create Donation Restriction Release <docs/donation_restriction_release/01-create.html>`_


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
