# Contributing

Start with the [setup guide](docs/setup.md) and [known issues](docs/known-issues.md). Use a local database with sample data and keep credentials out of commits.

## Making a change

Keep changes focused on a specific behavior. Describe the problem, the resulting behavior, and the checks performed. Include screenshots when changing a page. Update the route, database, or setup documentation when its corresponding behavior changes.

If a change alters a model, account for existing databases as well as fresh installations. `db.create_all()` will not update an existing table definition.

## Verification

The project has no automated test suite. Pull requests should describe the manual checks performed and any workflows that remain untested. Use disposable data for database checks.

A useful manual workflow, after the setup blockers are corrected, is:

1. Create distinct student and administrator accounts and verify login and logout.
2. Edit both profiles and confirm that the data persists after logging in again.
3. Insert a sample company, create a job, search for it as a student, and edit it as its administrator.
4. Submit an application and attempt a duplicate submission for the same job.
5. Approve the application, schedule an interview, and confirm what the student sees.
6. Verify rejected applications separately and inspect job deletion both with and without an interview.

For authorization fixes, also check requests while logged out, as a student, and as another administrator. Several routes currently permit access that should be restricted; use the [route reference](docs/routes.md) to identify the affected handlers.

Never commit the virtual environment, compiled Python files, database exports, or real account data.
