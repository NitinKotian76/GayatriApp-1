Overview
========

Purpose
-------

GayatriApp provides internal **inventory management**, **invoicing**, **challans**, **dispatch** and related **reports** (including Excel/PDF export) for mill and export workflows. The product direction is described in more detail under :doc:`/developement_phases`.

Technology stack
----------------

* **Backend:** Django (PostgreSQL, custom user model, session auth).
* **Frontend:** Django templates with HTMX for partial updates and interactions.
* **Ops-related:** Gunicorn, Memcached (caching and django-axes), WeasyPrint and spreadsheet libraries for document output (see application ``pyproject.toml``).

Repository layout
-----------------

``gayatri_invoice/``
   Python project managed with **uv**. Dependencies and tooling are defined in ``gayatri_invoice/pyproject.toml``.

``gayatri_invoice/gayatriapp/``
   Django project root: ``manage.py``, ``main/`` (settings and URL config), ``invoice/`` (business app).

``documentation/``
   This Sphinx documentation (separate uv project in ``documentation/pyproject.toml``).

Core Django apps
----------------

``main``
   Project configuration: :mod:`settings <django.conf>` modules (``base``, ``dev``, ``staging``, ``prod``), root :file:`urls.py`, WSGI/ASGI.

``invoice``
   Domain models, views, dynamic forms, Millsoft-oriented CRUD and report generation. See :doc:`/apps/invoice`.

URL map (high level)
--------------------

* **Admin:** ``/admin/``
* **Application:** ``/invoice/`` — includes authentication, dynamic tables/forms, reports, and Millsoft masters/transactions (see :doc:`/apps/invoice`).

Further reading
---------------

* :doc:`/getting_started` — environment, database, and how to run the app and build these docs.
* :doc:`/developer_guide` — onboarding checklist, tests, templates, production settings, and where to edit code.
* :doc:`/ci_cd` — CI/CD pipeline behavior, Docker Compose stack, and deploy/test entrypoints.
* :doc:`/apps/main` — settings and project wiring.
* :doc:`/apps/invoice` — invoice app structure and URL groups.
