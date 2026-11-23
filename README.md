# Resume Analyzer AI

A Django application for candidate registration, PDF / DOCX resume upload and parsing, skill-based interview question generation, video interview submission and staff-led candidate status review.

## Current project scope

- Candidate registration and login with hashed passwords.
- PDF and DOCX resume parsing.
- Rule-based interview question generation from extracted skills, education and experience.
- Browser webcam / microphone recording and authenticated video upload.
- Staff-only dashboard for candidate status and interview review.
- SQLite for local development, with optional MySQL configuration.

## Requirements

- Python 3.10 or newer (Python 3.12 recommended)
- pip
- A webcam and microphone for recording interviews

## Setup on Windows

\`\`\`powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\`\`\`

Open http://127.0.0.1:8000/.

Create a Django staff account with createsuperuser for the admin area. The application no longer ships with a default admin/admin login.

## Database configuration

SQLite is used by default for local development. To use MySQL, install mysqlclient and set these environment variables before starting Django:

\`\`\`text
DB_ENGINE=django.db.backends.mysql
DB_NAME=resume_ai_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
\`\`\`

Create the database and run python manage.py migrate. Do not import the old SQL dump; it was removed because it contained uploaded candidate data and plaintext credentials.

## Environment and security

Set DJANGO_SECRET_KEY to a unique random secret before deployment, set DJANGO_DEBUG=false, and provide DJANGO_ALLOWED_HOSTS. Keep .env, the local SQLite database and uploaded media outside Git. Uploaded candidate resumes and interview recordings are private data: store them in access-controlled storage, define a retention policy and never commit them to a public repository.

The Django admin dashboard requires an authenticated staff account. Candidate passwords are hashed. Existing local accounts that were stored with plaintext passwords can sign in once using their current password; the password is immediately re-hashed at successful login.

This is a learning project, not a production-ready recruitment platform. Before production use, add HTTPS, private object storage, virus scanning, rate limiting, stronger audit controls, privacy / consent notices, retention and deletion workflows, and a security review. Do not use automated scores as the sole basis for hiring decisions.

## Tests

\`\`\`powershell
python manage.py test
\`\`\`

The tests cover password hashing, the resume parser, question generation and scoring validation. Test webcam recording manually in a browser using localhost or HTTPS, because browser camera permissions are not available from the unit-test runner.

## Sensitive-file history warning

Candidate uploads and a database export were removed from the current branch. Earlier Git commits may still contain those files and an old development secret. Before keeping this repository public, make it private temporarily and rewrite Git history to remove those paths and rotate the old secret. Deleting a file in a new commit does not erase it from earlier commits.
