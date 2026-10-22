# course-catalog-api

Standalone FastAPI backend for the course catalog (moved from `lib/courses.ts`) — Advanced Web Technologies, Aimabek Aidar, IT3-2301.

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```

Open http://127.0.0.1:8000/docs for the interactive documentation.

## What was verified

| Request | Result |
| --- | --- |
| `GET /` | 200, `{"message": "Course Catalog API is running"}` |
| `GET /courses` | 6 courses, `ai-integration` first (32 likes), `api-design` last (11) |
| `GET /courses?is_elective=true` | 2: ai-integration, api-design |
| `GET /courses?is_elective=false` | 4: modern-frontend, web-security, backend-fastapi, databases-postgresql |
| `GET /courses?sort=title` | 6 alphabetically: ai-integration, api-design, backend-fastapi, modern-frontend, databases-postgresql, web-security |
| `GET /courses?page=1&page_size=2` | ai-integration, modern-frontend |
| `GET /courses?page=2&page_size=2` | web-security, backend-fastapi |
| `GET /courses?page=3&page_size=2` | databases-postgresql, api-design |
| `GET /courses?page=4&page_size=2` | `[]` |
| `GET /courses/web-security` | 200, one course |
| `GET /courses/nope` | 404, `{"detail": "Course not found"}` |
| `/docs` | exactly three routes: `GET /`, `GET /courses`, `GET /courses/{course_id}` |

## What changed (integration with the Next.js frontend)

- **CORS.** `CORSMiddleware` allows exactly one origin, `http://localhost:3000` (scheme + host + port, no trailing slash), with all methods and headers. Without it the browser hides responses to requests sent from the frontend's Client Components (the "Electives only" filter, the like button, the enrollment form). Requests from the Next.js server (Server Components) don't need CORS. CORS is not a protection for data: the server still executes requests from any origin.
- **camelCase in JSON.** `CamelModel` (`alias_generator=to_camel`, `validate_by_name=True`, `validate_by_alias=True`) makes `is_elective` appear as `isElective`, `course_id` as `courseId`, etc. Python code stays snake_case; query parameters (`is_elective`, `sort`, `page`, `page_size`) are not renamed.
- **New routes** (data lives in memory and resets on every restart):

| Route | Example response |
| --- | --- |
| `POST /courses/web-security/like` | `200` `{"id": "web-security", ..., "isElective": false, "likes": 22}`; unknown id → `404` `{"detail": "Course not found"}` |
| `POST /enrollments` with `{"courseId": "web-security", "studentName": "Aigerim"}` | `201` `{"courseId": "web-security", "studentName": "Aigerim", "id": 1}`; name shorter than 2 chars → `422`; unknown course → `404` |
| `GET /enrollments` | `[{"courseId": "web-security", "studentName": "Aigerim", "id": 1}]` |
