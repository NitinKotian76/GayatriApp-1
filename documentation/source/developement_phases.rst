Development phases
==================

The product is evolving in planned phases. This page summarizes the roadmap described alongside the codebase.

Phase 1 — Initial MVP
---------------------

* Planning and Django project setup.
* Basic inventory management and invoice / challan generation.

Phase 2 — Dynamic, user-configurable system
-------------------------------------------

* User-editable database tables (metadata-driven storage; see models such as ``TableName``, ``TableMetaData``, ``TableData`` in the ``invoice`` app).
* User-editable UI.
* User-editable invoice template designer or helper.

See :doc:`/apps/invoice` for where dynamic forms and reports are implemented in code.
