# 🎓 Learning Management System (LMS) API

A robust and scalable **Learning Management System (LMS)** API built with **Django 5** and **Django REST Framework (DRF)**. This backend handles core functionalities like student and instructor management, course enrollment, lesson tracking, and session management.

---

## 🚀 Features

- Token-based authentication (JWT)
- Role-based student/instructor management
- Course creation & enrollment
- Lesson and video management
- Auto-generated schema docs via `drf-spectacular`
- CKEditor integration for rich text content

---

## 🏗️ Project Structure

```
LearningMgtSystem/
├── accounts/
├── enrolments/
├── instructors/
├── students/
├── LearningMgtSystem/
├── api_test.http
├── log/
├── logs.log
├── manage.py
├── note.txt
├── README.md
├── requirements.txt
└── working_tree.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sheyzie/Alx_Capstone_Project.git
cd Alx_Capstone_Project
```

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DB_NAME=learning_mgt_sys
DB_USER=super_admin_user
DB_PASSWORD=SuperAdminUser1
DB_HOST=localhost
DB_PORT=3306

DEBUG=True
DJANGO_SECRET_KEY=your_secret_key

PA_HOST=your_pythonanywhere_host   # Example: yourusername.pythonanywhere.com
PROD_HOST=your_production_host     # Example: api.yourdomain.com
FRONTEND_ORIGIN=http://localhost:3000   # Frontend client URL

# Optional: non‑interactive superuser creation
DJANGO_SUPERUSER_FIRSTNAME=admin
DJANGO_SUPERUSER_LASTNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=super_admin_pass
```

You can use `python-dotenv` to load this file automatically.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py create_super_admin
```

This uses the custom management command at:
`accounts/management/commands/create_super_admin.py`

### 7. Start the Development Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

This project uses **JWT via djangorestframework-simplejwt**.

### Obtain Token

```http
POST /api/token/

{
  "username": "your_username",
  "password": "your_password"
}
```

### Refresh Token

```http
POST /api/token/refresh/

{
  "refresh": "your_refresh_token"
}
```

---

## 🧾 API Endpoints

### 📘 Courses

| Method | Endpoint |
|--------|----------|
| GET    | /api/courses/ |
| GET    | /api/courses/{id}/ |
| POST   | /api/courses/create/ |
| PUT    | /api/courses/{id}/edit/ |
| PATCH  | /api/courses/{id}/edit/ |
| DELETE | /api/courses/{id}/delete/ |

### 🎓 Enrolments

| Method | Endpoint |
|--------|----------|
| GET    | /api/enrolments/ |
| GET    | /api/enrolments/{id}/ |
| POST   | /api/enrolments/create/ |
| PUT    | /api/enrolments/{id}/edit/ |
| PATCH  | /api/enrolments/{id}/edit/ |
| DELETE | /api/enrolments/{id}/delete/ |

### 👨‍🏫 Instructors

| Method | Endpoint |
|--------|----------|
| GET    | /api/instructors/ |
| GET    | /api/instructors/{id}/ |
| POST   | /api/instructors/register/ |
| PUT    | /api/instructors/{id}/activate/ |
| PUT    | /api/instructors/{id}/deactivate/ |
| DELETE | /api/instructors/{id}/delete/ |

### 🎥 Lesson Videos

| Method | Endpoint |
|--------|----------|
| GET    | /api/lesson-videos/ |
| GET    | /api/lesson-videos/{id}/ |
| POST   | /api/lesson-videos/create/ |
| PUT    | /api/lesson-videos/{id}/edit/ |
| PATCH  | /api/lesson-videos/{id}/edit/ |
| DELETE | /api/lesson-videos/{id}/delete/ |

### 📖 Lessons

| Method | Endpoint |
|--------|----------|
| GET    | /api/lessons/ |
| GET    | /api/lessons/{id}/ |
| POST   | /api/lessons/create/ |
| PUT    | /api/lessons/{id}/edit/ |
| PATCH  | /api/lessons/{id}/edit/ |
| DELETE | /api/lessons/{id}/delete/ |

### 🧑‍🎓 Students

| Method | Endpoint |
|--------|----------|
| GET    | /api/students/ |
| GET    | /api/students/{id}/ |
| POST   | /api/students/register/ |
| PUT    | /api/students/{id}/activate/ |
| PUT    | /api/students/{id}/deactivate/ |
| DELETE | /api/students/{id}/delete/ |

### 🕒 Sessions

| Method | Endpoint |
|--------|----------|
| GET    | /api/sessions/ |
| GET    | /api/sessions/{id}/ |
| POST   | /api/sessions/create/ |
| PUT    | /api/sessions/{id}/edit/ |
| PATCH  | /api/sessions/{id}/edit/ |
| DELETE | /api/sessions/{id}/delete/ |

---

## 📊 API Schema

`GET /api/schema/`

Auto-generated using **drf-spectacular**.  
Compatible with **Swagger & Redoc**.

---

## 📦 Tech Stack

- Python 3.12+
- Django 5.2.4
- Django REST Framework
- JWT Auth via SimpleJWT
- MySQL (via mysqlclient)
- drf-spectacular for API docs
- CKEditor for lesson content

---

## 📋 Models / Schemas

- Course
- Enrolment
- Instructor
- Lesson
- LessonVideo
- Session
- Student
- User
- UserProfile
- VideoSession

---

## 🧪 Testing

Basic HTTP test file included: **api_test.http**

Or run Django tests:

```bash
python manage.py test
```

---

## 🛡️ Security Tips

- Disable `DEBUG` in production
- Use strong, unique `SECRET_KEY`
- Secure environment with `.env`
- Set up CORS and rate limiting appropriately

---

## 📄 License

Licensed under the **MIT License**

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss ideas or submit a pull request.
