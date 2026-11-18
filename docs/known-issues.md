# Known issues

The following limitations affect local setup, data integrity, and access control.

## Before public deployment

| Finding | Source | Required change |
| --- | --- | --- |
| Public signup accepts the submitted role, including `admin` | `signup()` and `signup.html` | Restrict ordinary signup to student accounts and provision administrators through a trusted process. |
| Application lists, status updates, interview scheduling, and interview lists lack authentication guards | `view_applications()`, `update_application_status()`, `schedule_interview()`, `admin_view_interviews()` | Require an authenticated administrator and enforce the intended data scope. |
| Any admin session can edit or delete any job ID | `update_job()` and `delete_job()` | Enforce job ownership or document and implement an explicit shared-management policy. |
| Forms have no CSRF protection | POST handlers and templates | Add server-side CSRF validation to state-changing requests. |
| Development debugger is enabled | `run.py` | Use a production server and disable debug mode outside local development. |

## Setup and data integrity

- **Unpinned dependencies.** `requirements.txt` does not pin package versions, so separate installations may resolve different versions.
- **Password hash storage.** `users.password` is limited to 100 characters. Werkzeug 3.1.3 generates a 162-character default password hash. PostgreSQL account creation can fail until the column is enlarged.
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
