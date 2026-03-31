Getting started
===============

This section covers running the **Django application** and **building this documentation**. The app uses **uv** for Python dependencies; run uv commands from ``gayatri_invoice/`` as described in the repository rules.

For day-to-day conventions (tests, templates, two-project layout, production env vars), see :doc:`/developer_guide`.
For CI/CD container flow (test vs deploy mode), see :doc:`/ci_cd`.

Prerequisites
-------------

* Python 3.11+ (see ``gayatri_invoice/pyproject.toml`` for the pinned range).
* **PostgreSQL** — development settings expect a database (see ``main/settings/dev.py``).
* **Memcached** — dev settings configure Django cache and django-axes via Memcached on ``127.0.0.1:11211``.
* **uv** — install from https://docs.astral.sh/uv/

Run the Django application
---------------------------

From the repository root:

.. code-block:: bash

   cd gayatri_invoice
   uv sync
   cd gayatriapp
   uv run python manage.py migrate
   uv run python manage.py runserver

Adjust ``main/settings/dev.py`` (or use environment-specific settings) if your local database name, user, password, host, or cache endpoint differ.

Build the Sphinx documentation
--------------------------------

The docs are a **separate** uv project under ``documentation/``:

.. code-block:: bash

   cd documentation
   uv sync
   uv run sphinx-build -b html source build/html

Or use the Makefile from ``documentation/``:

.. code-block:: bash

   make html

Open ``documentation/build/html/index.html`` in a browser to view the site.

**Note:** ``documentation/source/conf.py`` calls ``django.setup()`` using ``main.settings.dev`` so that autodoc and imports resolve. Building docs therefore requires the documentation virtualenv dependencies (including Django and related packages) to install successfully; a running PostgreSQL server is not required for a successful HTML build unless something in app loading connects eagerly.
