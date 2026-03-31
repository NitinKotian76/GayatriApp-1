CI/CD and Deployment
=====================

This page documents the CI/CD and deployment workflow for **GayatriApp**, based on the repository scripts and environment setup:

* ``jenkins/cicd.md`` (pipeline stages and intent)
* ``docker-compose.yml`` (local/staging/prod container stack)
* ``gayatri_invoice/Dockerfile`` + ``gayatri_invoice/entrypoint.sh`` (build and runtime behavior)
* ``gayatri_invoice/test.sh`` and ``gayatri_invoice/deploy.sh`` (what runs in test vs deploy mode)
* ``nginx/default.conf`` (reverse proxy + static file serving)

Pipeline overview
------------------

The high-level flow is described in ``jenkins/cicd.md`` as **dev -> staging -> prod**:

* Develop changes -> open/trigger a PR
* Run tests for the PR
* Push/confirm deployment
* Deploy to staging/prod environments (with all services running)

The repository is designed so that the **same Django container image** can run either:

* **test mode** (runs Django tests and then exits)
* **deploy mode** (runs migrations, collects static files, and starts Gunicorn)

Container stack (Docker Compose)
---------------------------------

``docker-compose.yml`` defines these services:

* ``postgres``: PostgreSQL database (port ``5433:5432`` on the host)
* ``memcached``: Memcached cache (port ``11212:11211`` on the host)
* ``gayatriapp``: Django app container (built from ``gayatri_invoice/Dockerfile``)
* ``nginx``: reverse proxy to the Django container, and static file serving

The ``gayatriapp`` service is exposed on container port ``8000`` and depends on ``postgres`` and ``memcached``.

Nginx configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From ``nginx/default.conf``:

* ``/static/`` is served from ``/app/staticfiles``
* all other traffic is proxied to ``gayatriapp:8000`` (the upstream name is ``gayatriserver``)

Application image build (Dockerfile)
--------------------------------------

``gayatri_invoice/Dockerfile`` is a multi-stage build:

* **builder stage**
  * installs ``uv``
  * installs Python dependencies from ``requirements.txt`` (production dependencies)
  * copies application code and the helper scripts::

    * ``entrypoint.sh``
    * ``deploy.sh``
    * ``test.sh``
* **runtime stage**
  * installs OS packages needed by the app (Postgres client libs and WeasyPrint dependencies)
  * creates an unprivileged ``appuser``
  * copies installed dependencies + the app from the builder stage
  * sets::

    * ``ENTRYPOINT ["/gayatri/entrypoint.sh"]``
    * ``EXPOSE 8000``

Runtime behavior (TEST switch)
--------------------------------

The container behavior is controlled by the ``TEST`` environment variable in:

* ``gayatri_invoice/entrypoint.sh``

If ``TEST='test'``:

* runs ``gayatri_invoice/test.sh``
* ``test.sh`` performs:
  * ``python manage.py migrate --noinput``
  * ``python -Wa manage.py test --noinput``

If ``TEST`` is not ``test``:

* runs ``gayatri_invoice/deploy.sh``
* ``deploy.sh`` performs:
  * ``python manage.py migrate --noinput``
  * ``python manage.py migrate axes --noinput``
  * ``python manage.py collectstatic --noinput``
  * starts Gunicorn via ``gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120``

Environment files (.env)
--------------------------

The repo includes two environment files used for composing local/CI runs:

* ``.env``: production-style defaults
  * ``DJANGO_SETTINGS_MODULE='main.settings.prod'``
  * ``DEBUG='False'``
  * ``TEST=''`` (empty)
* ``.env.test``: CI test defaults
  * ``DJANGO_SETTINGS_MODULE='main.settings.dev'``
  * ``DEBUG='False'``
  * ``TEST='test'``

When running with Docker Compose, ensure the environment variables used for container startup are consistent with what you want to execute:

* unit tests: set ``TEST='test'`` (so ``entrypoint.sh`` runs ``test.sh``)
* deploy: keep ``TEST`` empty/anything else (so ``entrypoint.sh`` runs ``deploy.sh``)

Local “CI-like” test run (recommended)
----------------------------------------

To simulate the CI test stage locally using the docker-compose stack:

1. Use the test environment values (so that Django loads dev settings and ``TEST='test'``).
   * Option A: copy/replace ``.env`` with ``.env.test`` before the run.
   * Option B: run Compose with ``.env.test`` values injected into the environment.
2. Build and start the stack in test mode so the Django container exits after tests complete:

.. code-block:: bash

   docker compose up --build --abort-on-container-exit gayatriapp

Expected result: ``gayatriapp`` runs migrations, executes ``manage.py test``, and exits. If tests fail, the command fails.

Health checks
--------------

In ``docker-compose.yml``:

* ``gayatriapp`` healthcheck probes ``http://localhost:8000/``
* ``nginx`` healthcheck probes ``http://localhost/invoice``

Troubleshooting notes for CI contributors
-------------------------------------------

* If tests hang: ensure ``postgres`` and ``memcached`` containers are healthy (startup order matters; ``depends_on`` is set in Compose).
* If static files are missing in deploy mode: confirm ``collectstatic`` runs (it only runs when ``TEST`` is not ``test``).
* If environment doesn''t trigger the expected path: check ``TEST`` in the container environment (``entrypoint.sh`` reads it).

