# Local setup

Run all commands from the project root, where `run.py`, `config.py`, and `requirements.txt` are located. In the supplied ZIP, that directory is nested under `auicareers/auicareers/`.

## 1. Prepare Python

Create and activate a fresh virtual environment using the commands in the [README](../README.md). The archive's environment was created with Python 3.13; it is machine-specific and should not be reused or committed.

```sh
python -m pip install -r requirements.txt
```

`Flask-Login` is included in the prepared dependency manifest. No dependency lockfile is provided.

## 2. Configure the application

The prepared `config.py` reads the session secret and database URL from environment variables:

```python
import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

An `.env` file alone has no effect because no dotenv loader is configured. `.env.example` documents the variable names; export them in your terminal.

Set values in the same terminal used to start Flask. Generate a secret with:

```sh
python -c "import secrets; print(secrets.token_hex(32))"
```

PowerShell:

```powershell
$env:SECRET_KEY = 'paste-the-generated-secret'
$env:DATABASE_URL = 'postgresql://auicareers_user:local_password@localhost:5432/AUICareersDB'
```

macOS / Linux:

```sh
export SECRET_KEY='paste-the-generated-secret'
export DATABASE_URL='postgresql://auicareers_user:local_password@localhost:5432/AUICareersDB'
```

Use your own database credentials. URL-encode reserved characters in a password used inside the connection URL.

## 3. Create a PostgreSQL database

Install and start PostgreSQL, then connect with an account allowed to create roles and databases. For a new local installation, the following SQL creates a dedicated owner:

```sql
CREATE USER auicareers_user WITH PASSWORD 'local_password';
CREATE DATABASE "AUICareersDB" OWNER auicareers_user;
```

These are example development credentials. Match the database name and account to your connection URL. No database dump, schema migration, or seed data is included in the project.

## 4. Correct the password column

In `app/models.py`, change `User.password` from `db.String(100)` to at least `db.String(255)` before creating tables. The bundled Werkzeug 3.1.3 generates a 162-character default password hash, which does not fit the existing PostgreSQL column.

For a database that already has the original table, changing the model is insufficient. Back up the database and apply an appropriate schema change, for example:

```sql
ALTER TABLE users ALTER COLUMN password TYPE VARCHAR(255);
```

`db.create_all()` creates missing tables; it does not migrate existing columns.

## 5. Initialize tables and add a company

Start a Flask shell:

```sh
python -m flask --app run shell
```

Run the following Python statements in that shell:

```python
from app import db
from app.models import Company

db.create_all()

company = Company(
    company_name="Example Company",
    industry="Software",
    location="Ifrane",
    contact_email="careers@example.com",
)
db.session.add(company)
db.session.commit()
print(company.company_id)
```

Record the generated ID. Job creation requires an existing company ID entered manually in the form. The sample above adds a company each time it is run; it is not an idempotent seed script.

## 6. Start the development server

```sh
python run.py
```

Open <http://127.0.0.1:5000>. Create separate student and admin accounts to exercise both workflows. Self-selecting an admin account is part of the current prototype and must be replaced before public deployment.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `No module named 'flask_login'` | Install `Flask-Login` in the active environment and add it to the manifest. |
| PostgreSQL connection refused | Check that the server is running and the host and port match the URL. |
| Authentication failed or database missing | Check the role, password, exact database name, and connection URL. |
| Relation does not exist | Import the models and run `db.create_all()` against the intended database. |
| Signup fails with a value-too-long error | Confirm that the actual `users.password` column was enlarged. |
| Job creation fails on a foreign key | Use the ID of an existing company. |
| A successful job action shows no confirmation | Some standalone templates do not render Flask flash messages. |
| Tailwind styling, fonts, or the homepage image fail to load | These assets come from external hosts and require network access. |

## Hosting

The repository has no deployment configuration. `run.py` starts the development server with `debug=True`. Public hosting requires the fixes in [Known issues](known-issues.md), a production WSGI server, protected secrets, database backups and migrations, and an explicit timezone policy. This documentation does not establish that the current version is ready for production.
