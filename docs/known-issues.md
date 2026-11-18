# Known issues

These findings originated from the supplied archive. Repository preparation replaced the embedded configuration values with environment variables, added the missing Flask-Login dependency, and excluded the archived Git history, virtual environment, and bytecode. The remaining application issues below are unresolved.

## Before public deployment

| Finding | Source | Required change |
| --- | --- | --- |
| Public signup accepts the submitted role, including `admin` | `signup()` and `signup.html` | Restrict ordinary signup to student accounts and provision administrators through a trusted process. |
| Application lists, status updates, interview scheduling, and interview lists lack authentication guards | `view_applications()`, `update_application_status()`, `schedule_interview()`, `admin_view_interviews()` | Require an authenticated administrator and enforce the intended data scope. |
| Any admin session can edit or delete any job ID | `update_job()` and `delete_job()` | Enforce job ownership or document and implement an explicit shared-management policy. |
| Forms have no CSRF protection | POST handlers and templates | Add server-side CSRF validation to state-changing requests. |
| Development debugger is enabled | `run.py` | Use a production server and disable debug mode outside local development. |

## Setup and data integrity

- **Unpinned dependencies.** A fresh install may differ from the bundled environment. The missing Flask-Login declaration has been added during repository preparation.
- **Password hash storage.** `users.password` is limited to 100 characters. A default hash generated with bundled Werkzeug 3.1.3 was 162 characters. PostgreSQL account creation can fail until the column is enlarged.
- **No schema lifecycle.** There are no migration files, initialization commands, seed scripts, or database dump. The documentation provides manual local setup instructions.
- **Missing student foreign key on applications.** The ORM join works, but PostgreSQL does not enforce that `applications.student_id` references a user.
- **Overlapping ORM relationships.** Mapper configuration emits a warning for `Job.applications` and `Application.job`; they are not paired with `back_populates`.
- **Interview validation.** Scheduling accepts submitted IDs and a timestamp without checking approval, duplicate appointments, conflicts, or whether the time is in the future. Times have no timezone policy.
- **Job deletion with interviews.** Interview foreign keys have no explicit deletion cascade. Associated interviews can prevent job deletion.
- **Uneven validation and error handling.** Numeric profile and job fields are passed from form strings to model fields. Several writes lack exception handling and rollback. Some account and job errors include raw exception text in flash messages.

## Behavior and maintenance

- The status handler writes `approved` and `rejected`, while the student template styles `accepted` and `declined`. Actual stored decisions display through a plain-text fallback.
- Two job creation handlers duplicate behavior. Their shared template posts to `/add_job`, including when opened through `/admin/create_job`.
- Flask-Login is initialized, but login and logout use custom session handling. `UserMixin.get_id()` also needs an override for the model's `user_id` key if Flask-Login is adopted fully.
- Standalone templates do not share `base.html` flash rendering, so some confirmations and errors may not be visible on the destination page.
- Companies require manual insertion. There is no employer account, company editor, password reset, account deletion, rÃ©sumÃ© upload, or notification service.
- Lists have no pagination. Salary has no currency or period convention. The UI depends on remotely hosted styles, fonts, and a homepage image.

## Verification scope

The documentation review covered all 27 first-party files: six Python files, 20 templates, and `requirements.txt`. The archive also contains Git metadata, a virtual environment, and Python bytecode; those are not application features.

Checks performed using Python 3.13 and the archive's installed dependency libraries:

- Parsed all six Python files and all 20 Jinja templates successfully.
- Created the Flask application successfully and confirmed 23 application routes.
- Configured ORM mappers successfully; observed the relationship warning described above.
- Measured a default Werkzeug password hash against the declared column length.

Relevant bundled versions were Flask 3.1.0, Flask-SQLAlchemy 3.1.1, Flask-Login 0.6.3, SQLAlchemy 2.0.40, Werkzeug 3.1.3, and psycopg2-binary 2.9.10. These are observed versions, not a declared support matrix or a lockfile.

No PostgreSQL instance was created or contacted for this review. Account creation, persistence, deletion behavior, and complete browser workflows were not integration-tested. No first-party test suite or CI configuration was supplied. Syntax checks and application startup do not establish that all workflows succeed.
