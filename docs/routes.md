# HTTP route reference

All 23 application routes belong to the `main` blueprint in `app/routes.py`. They return HTML or redirects, rather than a JSON API. Flask's generated static route is excluded below.

The access column records handler checks in `app/routes.py`. An admin-looking URL or navigation link does not itself restrict access. `Student` and `Admin` mean a comparison with the role stored in the session. `None` means no authentication or role guard in the handler.

| Method | Path | Endpoint | Access check | Behavior |
| --- | --- | --- | --- | --- |
| GET | `/` | `main.index` | None | Render homepage |
| GET, POST | `/signup` | `main.signup` | None | Register user and set session |
| GET, POST | `/login` | `main.login` | None | Verify credentials and set session |
| GET | `/logout` | `main.logout` | None | Clear session |
| GET | `/dashboard` | `main.dashboard` | Session contains `user_id` | Redirect by session role |
| GET | `/admin/view` | `main.admin_view` | Admin | Render admin dashboard |
| GET | `/student_view` | `main.student_view` | Student | List jobs, own applications, and own interviews; optional `search` query |
| GET | `/student_profile` | `main.student_profile` | Student | Display own student profile |
| GET | `/admin_profile` | `main.admin_profile` | Admin | Display own admin profile |
| GET, POST | `/admin/create_job` | `main.create_job` | Admin | Display shared job form or create a job |
| GET | `/admin/jobs` | `main.admin_jobs` | Admin | List jobs posted by current user |
| GET, POST | `/add_job` | `main.add_job` | Admin | Display shared job form or create a job |
| POST | `/admin/jobs/delete/<int:job_id>` | `main.delete_job` | Admin; no ownership check | Delete selected job |
| GET, POST | `/admin/jobs/edit/<int:job_id>` | `main.update_job` | Admin; no ownership check | Read or update selected job |
| GET, POST | `/student/apply/<int:job_id>` | `main.student_apply` | Student | Display job and submit application |
| GET | `/view_applications` | `main.view_applications` | None | List all applications with user and job data |
| POST | `/update_application_status/<int:student_id>/<int:job_id>/<action>` | `main.update_application_status` | None | `accept` writes `approved`; `decline` writes `rejected` |
| GET, POST | `/update_student_profile` | `main.update_student_profile` | Student | Create missing own profile and update it |
| GET, POST | `/update_admin_profile` | `main.update_admin_profile` | Admin | Create missing own profile and update it |
| GET | `/aboutus` | `main.about_us` | None | Render project description and credits |
| GET, POST | `/admin/schedule_interview` | `main.schedule_interview` | None | List approved applications or insert interview |
| GET | `/admin/interviews` | `main.admin_view_interviews` | None | List all interviews |
| GET | `/view_companies` | `main.view_companies` | Student | List companies |

## Submitted fields

| Form | Fields consumed by handler |
| --- | --- |
| Signup | `name`, `email`, `password`, `role` |
| Login | `email`, `password` |
| Create or edit job | `company_id`, `title`, `description`, `location`, `salary` |
| Apply | `cover_letter`; student comes from session and job from URL |
| Student profile | `major`, `graduation_year`, `bio` |
| Admin profile | `department`, `phone_number` |
| Interview | `student_id`, `job_id`, `scheduled_time` |

Interview time is parsed as `%Y-%m-%dT%H:%M`. The scheduling POST does not verify that its submitted student and job have an approved application, even though the GET page lists only approved applications. No CSRF token handling is implemented for these forms.

The profile update GET handlers may create and commit a missing profile row before displaying the form. Logout also changes session state through GET.
