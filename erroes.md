# Setup checklist — django-newos_url

Date: 2025-10-24

This document is a concise "set up the project" style checklist that focuses on the practical steps and environment tasks you (or another developer) should perform to get the repo ready to run and to address the best-practice issues discovered during the audit. It intentionally avoids making code edits for you — use this as a checklist to follow now or hand off to someone else.

---

## Prerequisites

- Python 3.11+ (the repo lists packages that match modern Python versions). If you use a virtual environment tool you prefer (venv, virtualenv, conda), create an isolated environment.
- Git and a terminal (PowerShell on Windows).

---

## Quick local setup (recommended)

1) Create and activate a virtual environment

```powershell
# from repo root
python -m venv venv
# activate (PowerShell)
.\venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Ensure `src` is on the PYTHONPATH when running tools. Two options:

- Use the `src/manage.py` entrypoint (recommended for this repo) — run commands from the repo root as `python src/manage.py <command>`.
- Or adjust your IDE/run configuration to add `src/` to the Python path.

4) Create an environment file for local secrets (optional but recommended). Create a `.env` (do not commit it):

- Add at least the following keys:
  - `DJANGO_SECRET_KEY` — a long random string
  - `DJANGO_DEBUG=true` (for local dev only)
  - `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`

We will not change code for you now, but later you should update `src/project/settings.py` to read these variables.

---

## Checklist: configuration & safety (what to do next, no code edits required now)

- [ ] Remove hard-coded secrets from the repository
  - The repository currently contains a hard-coded `SECRET_KEY` in `src/project/settings.py`. Do not use that key in production.
  - Action: generate a secure random SECRET_KEY and store it in your local `.env` (see above). When you or another developer update settings, use an env reader (e.g. `django-environ` or `python-decouple`).

- [ ] Make `DEBUG` environment-controlled
  - For local development you can leave `DJANGO_DEBUG=true` in `.env`. For staging/production, set `DJANGO_DEBUG=false`.

- [ ] Configure `ALLOWED_HOSTS` for non-dev environments
  - Local: `localhost,127.0.0.1` is fine. For deploys, add your domain names.

- [ ] Secure production settings (when deploying)
  - Plan to enable `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and HSTS headers in production. These are deployment-time toggles; note them in your deployment checklist.

---

## Checklist: project structure & wiring (non-coding steps you can do now)

- [ ] Decide canonical manage.py entrypoint
  - Repo has both `manage.py` (root) and `src/manage.py`. For clarity, decide: either use `src/manage.py` (recommended here) or create a small wrapper at repo root that adjusts PYTHONPATH to include `src/`.

- [ ] Register apps
  - The `news` app directory exists under `src/news/` but is not registered in `INSTALLED_APPS`. Make a note to add `"news.apps.NewsConfig"` to `INSTALLED_APPS` before running app-specific code.

- [ ] Plan URL wiring
  - `src/project/urls.py` currently exposes only the admin. Plan to add a `news/urls.py` and include it (e.g., `path("news/", include("news.urls"))`). This is a small, later code change.

- [ ] Tidy scaffolding
  - There are empty scaffold files (services, tests). Decide which will be implemented and which to remove to reduce confusion.

---

## Checklist: database and runtime

- [ ] Apply migrations (first run after you set env and registering apps)

```powershell
# using src/manage.py
python src/manage.py makemigrations
python src/manage.py migrate
```

- [ ] Create a superuser (if you need admin access locally)

```powershell
python src/manage.py createsuperuser
```

- [ ] Run the development server

```powershell
python src/manage.py runserver
```

Visit <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/admin/> to verify basic functionality.

---

## Tests and verification (manual, no coding required now)

- [ ] Run the test suite to see current coverage

```powershell
python src/manage.py test
```

- Note: tests currently show "NO TESTS RAN" in this repo. Add at least one smoke test later (e.g., import test or a view response test) so CI can validate basic functionality.

---

## Developer tooling & CI (non-blocking, plan these items)

- [ ] Add dev dependencies separately (suggestion)
  - Create `requirements-dev.txt` with tools such as `black`, `isort`, `flake8`, `pytest-django`, and a pre-commit config.

- [ ] Add a simple GitHub Actions workflow to run:
  - `pip install -r requirements.txt` (and dev deps),
  - run `python src/manage.py test`,
  - run formatting/lint checks.

This is optional now, but strongly recommended before merging new work.

---

## Cleanup & repository hygiene

- [ ] Ensure `venv/` is not committed
  - The working directory currently contains `venv/`; add `venv/` to `.gitignore` and remove it from the repo if it was accidentally committed.

- [ ] Add a short `README.md` with these quick setup instructions
  - Include Python version, how to activate the venv, how to run tests, and where to add environment variables.

---

## Minimal verification checklist you can run right now

1. Activate the venv.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a local `.env` with `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=true`, `DJANGO_ALLOWED_HOSTS=localhost`.
4. Run:

```powershell
python src/manage.py migrate
python src/manage.py runserver
python src/manage.py test
```

If the server starts and tests run (even if no tests exist), the environment is wired correctly.

---

## If you want me to do the small code updates (optional follow-up)

I can implement these low-risk changes for you:

- Make `settings.py` read `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` from the environment.
- Add `"news.apps.NewsConfig"` to `INSTALLED_APPS` and create a minimal `news/urls.py` and `news/views.py` example.
- Add one smoke test and a GitHub Actions workflow that runs tests and linters.

Tell me which of these you'd like and I will implement them and run the test suite.

---

Generated as a "set up project" style checklist so you (or a teammate) can prepare the repo and environment without making code changes right now.
