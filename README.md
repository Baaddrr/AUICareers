# AUICareers

AUICareers is a Flask web application for managing student job applications. Students can search job listings, submit cover letters, and view application decisions and scheduled interviews. Administrators can post jobs, review applications, and schedule interviews.

The application uses PostgreSQL for storage and renders pages with Jinja templates. It has no separate frontend build or JSON API.

## Features

| Area | Implemented behavior |
| --- | --- |
| Accounts | Sign up, log in, log out, and redirect to a dashboard based on the selected role |
| Student profiles | Edit major, graduation year, and biography |
| Job search | Search job titles and descriptions using a case-insensitive substring query |
| Applications | Submit a cover letter once per student and job; view application status |
| Companies | Browse company names, industries, locations, and contact emails |
| Job administration | Create, edit, and delete jobs; list jobs posted by the current administrator |
| Application review | View applications and set their status to `approved` or `rejected` |
| Interviews | Schedule interviews and display them to students and administrators |
| Admin profiles | Edit department and phone number |

Company records must be inserted through the database or a Flask shell. There is no company-management form, employer account, rÃ©sumÃ© upload, or email notification service in this version.

## Project status

This version is a local development prototype. Before using real accounts or exposing it publicly, address the access-control and configuration issues in [Known issues](docs/known-issues.md). In particular, signup permits users to select the admin role, and several application and interview routes have no authentication check.

Before creating accounts, enlarge the password column to accommodate generated hashes. The [setup guide](docs/setup.md) explains this change.

## Technology

- Python and Flask
- Flask-SQLAlchemy and PostgreSQL through `psycopg2-binary`
- Flask-Login, initialized alongside the application's custom session handling
- Werkzeug password hashing
- Jinja HTML templates, inline CSS, and Tailwind CSS loaded from a CDN

Dependencies in `requirements.txt` are unpinned. The project does not declare a supported Python or PostgreSQL version range.

## Run locally

Create a virtual environment from the directory containing `run.py`:

```sh
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Install the declared packages:

```sh
python -m pip install -r requirements.txt
```

Then follow [Local setup](docs/setup.md) to configure PostgreSQL, correct the password column, initialize the tables, and add a company. Once those steps are complete:

```sh
python run.py
```

Open <http://127.0.0.1:5000>. This command enables Flask's development debugger; use it only for local development.

## Repository structure

```text
app/
  __init__.py       Application factory and extension initialization
  login_manager.py Flask-Login instance and user loader
  models.py        Seven database models
  routes.py        Main blueprint and 23 application routes
  templates/       20 Jinja/HTML templates
config.py          Flask and database configuration
requirements.txt   Dependency manifest
run.py             Development entry point
```

`dashboard.html` is present, but `/dashboard` redirects to a role-specific page rather than rendering it. Styles are defined inside templates; there is no first-party static asset directory in the project.

## Documentation

- [Local setup and troubleshooting](docs/setup.md)
- [Architecture and workflows](docs/architecture.md)
- [Database reference](docs/database.md)
- [HTTP route reference](docs/routes.md)
- [Known issues](docs/known-issues.md)
- [Contributing](CONTRIBUTING.md)

## Credits

Ayman ELAKKAOUI and Badr FATOUH.
