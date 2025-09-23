Employee Management API-

    Simple Django REST API for Departments, Employees, Attendance, and Performance with token auth, filters/search/ordering, Swagger docs, and a small charts dashboard. Open the docs at /swagger/ and /redoc/, and the dashboard at /charts/.

Quick start-

    Create venv and install:

        python -m venv venv
        Windows: venv\Scripts\activate
        Mac/Linux: source venv/bin/activate
        python -m pip install -r requirements.txt (or see “Install manually” below)

    Configure environment:

        Create a .env next to manage.py:
        DEBUG=True
        SECRET_KEY=dev-secret-change-this
        DB_NAME=employee_db
        DB_USER=postgres
        DB_PASSWORD=your_postgres_password
        DB_HOST=localhost
        DB_PORT=5432

    Run database:

        python manage.py migrate
        Optional seed: python manage.py seed_data --employees 40 --days 30

    Create admin and token:

        python manage.py createsuperuser
        python manage.py runserver
        Visit /admin → Tokens → Add Token → select your user → copy the token

    Open the app:

        Swagger: http://127.0.0.1:8000/swagger/

        Redoc: http://127.0.0.1:8000/redoc/

        Dashboard: http://127.0.0.1:8000/charts/

Features

    CRUD for Employees and Departments; daily Attendance with one row per employee per date.

    Filters (?status=present), search (?search=an), ordering (?ordering=-date).

    Token auth: reads are open, writes require Authorization: Token <3aa8720884cdb2a6bfa694d1d7d54337e660c89e>.

    OpenAPI docs with drf-spectacular; dashboard with Chart.js (bar + pie).

API examples

    Employees:

        List: GET /api/employees/

        Search: GET /api/employees/?search=an

        Filter: GET /api/employees/?department=1

        Order: GET /api/employees/?ordering=-date_of_joining

        Create: POST /api/employees/ (requires token)

    Attendance:

        List: GET /api/attendance/

        Filter: GET /api/attendance/?status=present&ordering=-date

        Create: POST /api/attendance/ with:
        {
        "employee_id": 1,
        "date": "2025-09-21",
        "status": "present"
        } (requires token)

    Dashboard

        Charts page: /charts/

        Data endpoints:

        /charts/employees-per-department/

        /charts/attendance-last-7-days/

Install manually (if no requirements.txt)

    python -m pip install Django djangorestframework psycopg[binary] django-environ django-filter Faker drf-spectacular drf-spectacular-sidecar django-cors-headers

Settings highlights

    INSTALLED_APPS includes: rest_framework, rest_framework.authtoken, django_filters, drf_spectacular, drf_spectacular_sidecar, employees, attendance, charts, corsheaders.

    REST_FRAMEWORK:

        DEFAULT_SCHEMA_CLASS = drf_spectacular.openapi.AutoSchema

        DEFAULT_PAGINATION_CLASS = rest_framework.pagination.PageNumberPagination

        PAGE_SIZE = 10

        DEFAULT_AUTHENTICATION_CLASSES = SessionAuthentication, TokenAuthentication

        DEFAULT_PERMISSION_CLASSES = IsAuthenticatedOrReadOnly

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

Common issues-

    Duplicate attendance: update the existing record or use a new date; model enforces one per day per employee.

    Swagger/Redoc template errors: ensure drf-spectacular and sidecar are installed and in INSTALLED_APPS. Restart server.

    CORS for local frontend: install django-cors-headers, add CorsMiddleware, and set CORS_ALLOWED_ORIGINS=['http://localhost:3000'].

Deployment notes (summary)

    Set DEBUG=False and add the domain to ALLOWED_HOSTS.

    python manage.py collectstatic to gather static assets.

    Configure DB via environment variables; run migrations on server.