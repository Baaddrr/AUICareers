# Database reference

The seven SQLAlchemy models are defined in `app/models.py`. The configured backend is PostgreSQL. No migrations, SQL schema file, or seed script were supplied.

`PK` means primary key; `FK` means a database foreign key declared by the model. Unless specified otherwise, non-key fields below are nullable.

## Tables

| Model / table | Columns and constraints |
| --- | --- |
| `User` / `users` | `user_id` integer PK; required `name` varchar(100), unique required `email` varchar(100), required `password` varchar(100), required `role` varchar(20); `created_at` datetime with database `now()` default |
| `StudentProfile` / `student_profile` | `user_id` integer PK and FK to `users.user_id`; `major` varchar(100); `bio` text; `graduation_year` integer |
| `AdminProfile` / `admin_profile` | `user_id` integer PK and FK to `users.user_id`; `department` varchar(50); `phone_number` varchar(20) |
| `Company` / `company` | `company_id` integer PK; required `company_name` varchar(100); `industry` varchar(100); `location` varchar(100); `contact_email` varchar(100) |
| `Job` / `job` | `job_id` integer PK; required `company_id` FK to `company.company_id`; required `admin_id` FK to `users.user_id`; required `title` varchar(100); `description` text; `location` varchar(100); `salary` float; `created_at` datetime with Python `datetime.utcnow` default |
| `Application` / `applications` | Composite integer PK (`student_id`, `job_id`); `job_id` FK to `job.job_id` with `ON DELETE CASCADE`; `cover_letter` text; `status` varchar(20) with database default `pending`; `applied_at` datetime with database `now()` default |
| `JobInterview` / `job_interview` | `interview_id` integer PK; required `student_id` FK to `users.user_id`; required `job_id` FK to `job.job_id`; required `scheduled_time` datetime |

The table describes the supplied schema, including the undersized password column. Apply the correction in [Local setup](setup.md) before creating accounts.

## Relationships

- Each student or admin profile uses the user's ID as its own primary key, permitting at most one row of each profile type per user.
- A company can have many jobs. Each job references a company and the user who posted it.
- A student and job pair identifies an application. The model defines an ORM student relationship using an explicit join, but `applications.student_id` has **no database foreign key** to `users`.
- Interviews reference a user and a job separately. There is no foreign key tying an interview to an application, and no constraint requiring an approved application.

The models do not enforce role membership. A user referenced as an administrator or student is not checked against `users.role` by a database constraint.

## Application status

| Event | Stored value |
| --- | --- |
| New application | `pending` |
| Admin selects Accept | `approved` |
| Admin selects Decline | `rejected` |

The scheduling page queries `approved` applications. The student dashboard's special styling checks `accepted` and `declined`, so actual decisions fall through to plain-text display. The status column has no enum or check constraint; these values are conventions enforced only by some handlers.

## Deletion behavior

The application-to-job foreign key specifies cascading deletion, and `Job.applications` also configures delete-orphan behavior. Interviews have a separate job foreign key without an explicit database cascade. Deleting a job with interviews can therefore fail; validate the intended policy before relying on job deletion.

`Job.applications` and `Application.job` are defined separately without `back_populates`. Configuring the supplied models emits a SQLAlchemy overlapping-relationship warning. Mapper configuration succeeds, but the relationships should be reviewed together before changing deletion behavior.

## Schema maintenance

`db.create_all()` is suitable for creating missing tables in a fresh local database. It does not upgrade an existing schema. Introduce versioned migrations before maintaining shared databases. The archive provides no authoritative record of any schema changes previously applied outside the models.
