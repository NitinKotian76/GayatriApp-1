Developer guide
=================

This page is for **new contributors**: where things live, how to work day to day, and what to watch out for. It complements :doc:`/getting_started` (commands) and :doc:`/overview` (big picture).

Two Python projects in one repo
-------------------------------

Keep the split clear — each has its own ``pyproject.toml`` and **uv** lockfile:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Directory
     - Purpose
   * - ``gayatri_invoice/``
     - The **Django application**. All ``uv add`` / ``uv sync`` / ``uv run python manage.py …`` commands for the app are run from here (see project rules).
   * - ``documentation/``
     - **Sphinx** docs only. Use ``uv sync`` and ``uv run sphinx-build …`` from this directory.

Python versions differ slightly between the two projects; follow the ``requires-python`` line in each ``pyproject.toml``.

Default settings module
-----------------------

``manage.py`` sets:

.. code-block:: python

   DJANGO_SETTINGS_MODULE = "main.settings.dev"

So local work uses **dev** settings unless you override the environment variable. Production and staging use other modules under ``main/settings/`` (see :doc:`/apps/main`).

Typical first-day checklist
---------------------------

#. Install **uv**, **PostgreSQL**, and **Memcached** (dev expects cache at ``127.0.0.1:11211`` — see ``main/settings/dev.py``).
#. From ``gayatri_invoice/``: ``uv sync`` (pulls **dev**, **test**, and **documentation** dependency groups by default).
#. Create a PostgreSQL database matching ``DATABASES`` in dev settings (name/user/password/host), or adjust dev settings for your machine.
#. From ``gayatri_invoice/gayatriapp/``: ``uv run python manage.py migrate``.
#. Create an admin user: ``uv run python manage.py createsuperuser``.
#. ``uv run python manage.py runserver`` — app URLs are under ``/invoice/``; admin at ``/admin/``.
#. With dev settings, ensure ``INTERNAL_IPS`` includes your client IP if you use **Django Debug Toolbar** on a non-localhost host.

Dependency groups (``gayatri_invoice``)
----------------------------------------

``gayatri_invoice/pyproject.toml`` defines optional groups such as **dev**, **test**, and **documentation**. The ``[tool.uv] default-groups`` setting includes them in a normal ``uv sync``, so you get Selenium, coverage, and similar tools without extra flags. For a minimal install you would need to sync with only the main dependencies (see uv docs for ``--no-default-groups``).

Useful packages to be aware of:

* **django-htmx** — request/response patterns for partial page updates.
* **django-axes** — login security / lockout (dev enables it; configure cache accordingly).
* **django-debug-toolbar** — dev only; disabled in production-style settings.
* **WeasyPrint**, **openpyxl**, **Pillow** — reports and exports (see Millsoft utility URLs in :doc:`/apps/invoice`).

Tests
-----

The app uses Django’s built-in test runner:

.. code-block:: bash

   cd gayatri_invoice/gayatriapp
   uv run python manage.py test

Tests live under ``invoice/tests/``, including **Selenium** scripts in ``invoice/tests/seleniumtests/`` (they assume a running browser/driver setup — treat them as integration checks, not always CI-default).

If you add **pytest**-style configuration later, the repository convention is still to invoke tools via ``uv run`` from ``gayatri_invoice/``.

Migrations and models
---------------------

* Model changes: ``uv run python manage.py makemigrations`` then ``migrate`` from ``gayatri_invoice/gayatriapp/``.
* The project uses PostgreSQL-specific features in places (e.g. indexes in ``invoice/models.py``); switching to SQLite for local dev may require extra care or settings overrides.

Templates and static assets
---------------------------

* App templates: ``gayatri_invoice/gayatriapp/invoice/templates/`` (including ``partials/`` for HTMX fragments).
* Base layout: ``invoice/templates/base.html``.
* Static files are collected per Django defaults; check ``STATIC_URL`` / ``STATIC_ROOT`` and ``MEDIA_*`` in the active settings module.

Production-oriented settings
-----------------------------

``main/settings/prod.py`` uses **python-decouple** (``config(...)``) for secrets and flags — e.g. ``DJANGO_SECRET_KEY``, ``DEBUG``, ``ALLOWED_HOSTS``. Do **not** copy dev ``SECRET_KEY`` values into production; use environment variables or your host’s secret store.

``main/settings/base.py`` enables **cache middleware**; **dev** disables the surrounding cache middleware so the debug toolbar can inject into responses. When debugging caching behaviour, switch settings module or adjust middleware to match the environment you are reproducing.

Code layout hints (``invoice`` app)
-----------------------------------

When you need to change behaviour, start from the URL name in the browser (under ``/invoice/``) and jump to ``invoice/urls.py``, then the referenced module under ``invoice/all_views/`` or ``invoice/all_views/millsoft/``.

Other hotspots:

* **Dynamic forms / tables:** ``invoice/form_files/``, ``invoice/formmod/``, ``invoice/all_views/form_views.py``.
* **Reports:** ``invoice/reportmod/``, ``invoice/all_views/report_views.py``.
* **DB helpers:** ``invoice/dbmod/``.

The URL config comments note that **sentence-case names** refer to **class-based views** — useful when scanning ``urls.py``.

Documentation maintenance
-------------------------

* Sources: ``documentation/source/``. Build with ``make html`` or ``sphinx-build`` (see :doc:`/getting_started`).
* After adding a new ``.rst`` file, include it in ``documentation/source/index.rst`` under a ``toctree``.
* Use **absolute** cross-references from nested pages, e.g. ``:doc:`/overview` `` (see existing pages under ``apps/``).

Where to look next
------------------

* :doc:`/apps/invoice` — URL groups and package map.
* :doc:`/developement_phases` — planned Phase 2 configurability.
* Root ``README.md`` — one-line product summary.
