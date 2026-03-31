``main`` — project package
==========================

The ``main`` package under ``gayatri_invoice/gayatriapp/main/`` is the Django **project** (not the business app). It hosts global configuration and the root URL dispatcher.

Settings
--------

Settings are split by environment:

* ``main/settings/base.py`` — shared defaults (``INSTALLED_APPS``, middleware, templates, etc.). Production-oriented cache middleware appears here; dev overrides may disable it for the debug toolbar.
* ``main/settings/dev.py`` — local development: ``debug_toolbar``, ``axes``, ``django_htmx``, PostgreSQL, Memcached, ``INTERNAL_IPS``.
* ``main/settings/staging.py`` and ``main/settings/prod.py`` — environment-specific overrides for deployment.

Important entries include ``ROOT_URLCONF`` (``main.urls``), ``AUTH_USER_MODEL = "invoice.CustomUser"``, and login URLs pointing under ``/invoice``.

URL configuration
-----------------

``main/urls.py`` mounts:

* Django admin at ``admin/``.
* The invoice application at ``invoice/`` via ``include("invoice.urls")``.
* Debug toolbar routes when using dev settings.

WSGI / ASGI
-----------

``main/wsgi.py`` and ``main/asgi.py`` expose the Django application for traditional and async servers respectively.

Cross-references
----------------

* Application routes and features: :doc:`/apps/invoice`.
* Project overview: :doc:`/overview`.
