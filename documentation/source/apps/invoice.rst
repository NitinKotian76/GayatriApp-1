``invoice`` — business application
==================================

The ``invoice`` app (``gayatri_invoice/gayatriapp/invoice/``) contains models, views, templates, and supporting modules for **inventory**, **invoicing**, **Millsoft-style masters and transactions**, **dynamic forms**, and **reports**.

Models
------

``invoice.models`` defines:

* An abstract ``Audit`` mixin (created/updated timestamps and user foreign keys).
* **Phase 2** flexible table support: ``Company``, ``TableName``, ``TableMetaData``, ``TableData``.
* **Authentication:** ``CustomUser`` and related managers (project uses ``AUTH_USER_MODEL = "invoice.CustomUser"``).
* **Millsoft domain** entities — e.g. agents, customers, items, locations, shades, production, export details, invoices, stock adjustments — as used by CRUD views and reports.

For exact fields and relationships, refer to the source file ``invoice/models.py`` or use Django’s admin / model introspection.

URL structure (``invoice/urls.py``)
-----------------------------------

All routes below are prefixed with ``/invoice/`` from the site root.

Authentication (``auth_urlpatterns``)
   Login at ``""``, logout, change password.

Forms and dynamic tables (``form_urlpatterns``, ``table_urlpatterns``)
   Form builder/list, row operations, table data and search — backed by modules under ``form_files/``, ``formmod/``, and related views in ``all_views/form_views.py``.

Reports (``report_urlpatterns``)
   Report list, creation, and viewing via ``all_views/report_views.py`` and ``reportmod/``.

Admin-style table management (``admin_urlpatterns``)
   Table list/create and company admin in ``all_views/admin_views.py``.

Common (``main_urlpatterns``)
   Index, profile, notifications, formset helpers in ``all_views/common_views.py``.

Millsoft — masters (``millsoft_master_urlpatterns``)
   Class-based CRUD list/create/update/delete for masters such as agents, units, customers, companies, export field definitions, items, categories, locations, plus/minus heads, shades.

Millsoft — transactions (``millsoft_transact_urlpatterns``)
   Production, production reels, export details, invoices (including production reel selection), stock plus/minus, production approval flows.

Millsoft — reports (``millsoft_report_urlpatterns``)
   Creation views for challan, invoice, dispatch details, gate pass, stock reports.

Millsoft — utilities (``millsoft_utility_urlpatterns``)
   Download endpoints for Excel, CSV, and PDF under ``reports/``.

Millsoft — helpers (``millsoft_helper_urlpatterns``)
   e.g. reel preview.

Millsoft — misc (``millsoft_misc_urlpatterns``)
   e.g. stock transfer.

Supporting packages (by directory)
----------------------------------

``all_views/``
   Feature views split into ``auth_views``, ``admin_views``, ``common_views``, ``form_views``, ``report_views``, ``mixin``, and ``millsoft/`` submodules.

``dbmod/``
   Database helpers: CRUD, filters/search (``buisness_crud.py``, ``filter_search.py``, ``dbfunctions.py``).

``form_files/``, ``formmod/``
   Dynamic form construction, CRUD tables/forms, Millsoft-specific form wiring, static field helpers.

``reportmod/``
   Report generation (e.g. ``create_report.py``).

``tests/``
   Unit tests and Selenium navigation tests.

Cross-references
----------------

* Project settings and root URLs: :doc:`/apps/main`.
* Setup and running the server: :doc:`/getting_started`.
