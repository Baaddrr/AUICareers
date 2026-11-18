# Local setup

Run all commands from the project root, where `run.py`, `config.py`, and `requirements.txt` are located.

## 1. Prepare Python

Create and activate a virtual environment using the commands in the [README](../README.md).

```sh
python -m pip install -r requirements.txt
```

Dependencies, including `Flask-Login`, are listed in `requirements.txt`. There is no dependency lockfile.

## 2. Configure the application

`config.py` reads the session secret and database URL from environment variables:

```python
import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

An `.env` file alone has no effect because no dotenv loader is configured. `.env.example` documents the variable names; export them before starting Flask.

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

Replace the example credentials with the local database credentials. URL-encode reserved characters in a password used inside the connection URL.

## 3. Create a PostgreSQL database

Install and start PostgreSQL, then connect with an account allowed to create roles and databases. For a new local installation, the following SQL creates a dedicated owner:

```sql
CREATE USER auicareers_user WITH PASSWORD 'local_password';
CREATE DATABASE "AUICareersDB" OWNER auicareers_user;
```

These are example development credentials. The database name and account must match the connection URL. No database dump, schema migration, or seed data is included in the project.

## 4. Correct the password column

In `app/models.py`, change `User.password` from `db.String(100)` to at least `db.String(255)` before creating tables. Werkzeug 3.1.3 generates a 162-character default password hash, which does not fit the existing PostgreSQL column.

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
| `No module named 'flask_login'` | Install the dependencies from `requirements.txt` in the active environment. |
| PostgreSQL connection refused | Check that the server is running and the host and port match the URL. |
| Authentication failed or database missing | Check the role, password, exact database name, and connection URL. |
| Relation does not exist | Import the models and run `db.create_all()` against the intended database. |
| Signup fails with a value-too-long error | Confirm that the actual `users.password` column was enlarged. |
| Job creation fails on a foreign key | Use the ID of an existing company. |
| A successful job action shows no confirmation | Some standalone templates do not render Flask flash messages. |
| Tailwind styling, fonts, or the homepage image fail to load | These assets come from external hosts and require network access. |

## Hosting

The repository has no deployment configuration. `run.py` starts the development server with `debug=True`. Public hosting requires the fixes in [Known issues](known-issues.md), a production WSGI server, protected secrets, database backups and migrations, and an explicit timezone policy.
