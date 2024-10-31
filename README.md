# Social Media API

A robust Django-based social media API with PostgreSQL backend, featuring secure user authentication, JWT tokens, and comprehensive user management.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)

##  Features

- **Authentication & Authorization**
  -  token-based authentication
  - Secure password hashing
  - Session management

  
- **User Management**
  - User registration with email
  - Profile management


## 🛠 Tech Stack

- Django 5.0+
- Django REST Framework
- PostgreSQL
- Python 3.12+

##  Prerequisites

- Python 3.12 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)
- Virtual environment (recommended)

##  Project Structure

```
vibes/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── vibez_api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── vibes/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

##  Installation

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd vibes
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env file with your configurations
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

##  API Endpoints

### Authentication Endpoints

| Method | Endpoint                | Description                              | Authentication Required |
|--------|--------------------------|------------------------------------------|--------------------------|
| POST   | `/api/auth/signup/`      | Register a new user                      | No                       |
| POST   | `/api/auth/login/`       | Login user                               | No                       |
| POST   | `/api/auth/logout/`      | Logout user                              | Yes                      |
| POST   | `/api/posts/`            | Create a new post with media             | Yes                      |
| GET    | `/api/posts/`            | Retrieve all posts with media            | Yes                      |
| GET    | `/api/posts/{post_id}/`  | Retrieve a specific post with media      | Yes                      |
| DELETE | `/api/posts/{post_id}/`  | Delete a specific post                   | Yes                      |


##  Usage Examples

### User Registration
**Endpoint:** `POST /api/auth/signup/`

**Request:**
```json
{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
     "token":  "eyJ0eXAiOiJKV1QiLCJhbGc...",
}
```

### User Login
**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "johndoe"
    },
    "token":  "eyJ0eXAiOiJKV1QiLCJhbGc...",
       
    
}
```

### Protected Endpoint Access
```bash
curl -H "Authorization: Token your_access_token" \
     -X GET http://localhost:8000/api/auth/logout
```

--

### Create a New Post
**Endpoint:** `POST /api/posts/`

**Request:**
```json
{
    "content": "Exciting day at the park!",
    "media_files": [
        "path/to/image1.jpg",
        "path/to/video1.mp4"
    ]
}
```

**Response:**
```json
{
    "post": {
        "id": 1,
        "content": "Exciting day at the park!",
        "created_at": "2024-10-31T14:32:00Z",
        "user": 1,
        "media": [
            {
                "id": 101,
                "media_url": "https://res.cloudinary.com/.../image1.jpg",
                "media_type": "image",
                "created_at": "2024-10-31T14:32:01Z"
            },
            {
                "id": 102,
                "media_url": "https://res.cloudinary.com/.../video1.mp4",
                "media_type": "video",
                "created_at": "2024-10-31T14:32:01Z"
            }
        ]
    }
}
```

---

### Retrieve All Posts
**Endpoint:** `GET /api/posts/`

**Response:**
```json
[
    {
        "id": 1,
        "content": "Exciting day at the park!",
        "created_at": "2024-10-31T14:32:00Z",
        "user": 1,
        "media": [
            {
                "id": 101,
                "media_url": "https://res.cloudinary.com/.../image1.jpg",
                "media_type": "image"
            },
            {
                "id": 102,
                "media_url": "https://res.cloudinary.com/.../video1.mp4",
                "media_type": "video"
            }
        ]
    },
    {
        "id": 2,
        "content": "Another beautiful sunset.",
        "created_at": "2024-10-30T18:20:00Z",
        "user": 2,
        "media": [
            {
                "id": 103,
                "media_url": "https://res.cloudinary.com/.../sunset.jpg",
                "media_type": "image"
            }
        ]
    }
]
```

---

### Retrieve a Specific Post
**Endpoint:** `GET /api/posts/{post_id}/`

**Response:**
```json
{
    "id": 1,
    "content": "Exciting day at the park!",
    "created_at": "2024-10-31T14:32:00Z",
    "user": 1,
    "media": [
        {
            "id": 101,
            "media_url": "https://res.cloudinary.com/.../image1.jpg",
            "media_type": "image"
        },
        {
            "id": 102,
            "media_url": "https://res.cloudinary.com/.../video1.mp4",
            "media_type": "video"
        }
    ]
}
```

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📧 Contact

Email: [Racheal Kuranchie](kuranchieracheal@gmail.com)
