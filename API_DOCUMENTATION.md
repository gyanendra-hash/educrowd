# 📚 EduCrowd API Documentation

## 🌐 Base URL

```
Development: http://localhost:8000/api/v1/
Production: https://api.educrowd.com/v1/
```

## 🔐 Authentication

EduCrowd uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## 📋 API Endpoints

### 🔑 Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "phone_number": "+1234567890",
  "date_of_birth": "1990-01-01"
}
```

**Response:**
```json
{
  "message": "User created successfully. Please check your email for verification.",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Login User
```http
POST /api/v1/auth/login/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_verified": true
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### Logout User
```http
POST /api/v1/auth/logout/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

#### Change Password
```http
POST /api/v1/auth/password/change/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

#### Request Password Reset
```http
POST /api/v1/auth/password/reset/
```

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

#### Verify Email
```http
POST /api/v1/auth/verify-email/
```

**Request Body:**
```json
{
  "uid": "base64_encoded_user_id",
  "token": "verification_token"
}
```

### 🏢 Tenant Management Endpoints

#### List Tenants
```http
GET /api/v1/tenants/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "University of Technology",
      "description": "Leading technology university",
      "email": "contact@university.edu",
      "website": "https://university.edu",
      "timezone": "America/New_York",
      "language": "en",
      "currency": "USD",
      "is_active": true,
      "subscription_plan": "premium",
      "subscription_status": "active",
      "user_count": 1250,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 1,
  "next": null,
  "previous": null
}
```

#### Create Tenant
```http
POST /api/v1/tenants/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "New University",
  "description": "A new educational institution",
  "email": "contact@newuniversity.edu",
  "website": "https://newuniversity.edu",
  "timezone": "UTC",
  "language": "en",
  "currency": "USD",
  "domain": "newuniversity.educrowd.com"
}
```

#### Get Tenant Details
```http
GET /api/v1/tenants/{tenant_id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

#### Update Tenant
```http
PUT /api/v1/tenants/{tenant_id}/
PATCH /api/v1/tenants/{tenant_id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

#### Delete Tenant
```http
DELETE /api/v1/tenants/{tenant_id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

### 👥 User Management Endpoints

#### Get User Profile
```http
GET /api/v1/auth/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "initials": "JD",
    "phone_number": "+1234567890",
    "avatar": "https://api.educrowd.com/media/avatars/john.jpg",
    "date_of_birth": "1990-01-01",
    "bio": "Software developer and educator",
    "is_verified": true,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "organization": "University of Technology",
  "job_title": "Professor",
  "website": "https://johndoe.com",
  "location": "New York, NY",
  "timezone": "America/New_York",
  "language": "en",
  "notification_preferences": {
    "email_notifications": true,
    "push_notifications": true,
    "sms_notifications": false
  },
  "privacy_settings": {
    "profile_visibility": "public",
    "email_visibility": "private"
  }
}
```

#### Update User Profile
```http
PUT /api/v1/auth/profile/
PATCH /api/v1/auth/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

#### List User Roles
```http
GET /api/v1/auth/roles/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `tenant_id` (optional): Filter roles by tenant

#### List User Sessions
```http
GET /api/v1/auth/sessions/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

### 🏫 LMS Endpoints (Week 2 - Coming Soon)

#### List Courses
```http
GET /api/v1/lms/courses/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search in course title and description
- `level`: Filter by course level (beginner, intermediate, advanced)
- `status`: Filter by course status (draft, published, archived)
- `page`: Page number for pagination
- `per_page`: Number of items per page

#### Create Course
```http
POST /api/v1/lms/courses/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Python Programming Fundamentals",
  "description": "Learn Python from scratch with hands-on projects",
  "level": "beginner",
  "price": 99.99,
  "duration_hours": 40,
  "metadata": {
    "prerequisites": ["Basic computer skills"],
    "learning_objectives": [
      "Understand Python syntax",
      "Write basic programs",
      "Work with data structures"
    ]
  }
}
```

#### Get Course Details
```http
GET /api/v1/lms/courses/{course_id}/
```

#### Update Course
```http
PUT /api/v1/lms/courses/{course_id}/
PATCH /api/v1/lms/courses/{course_id}/
```

#### Delete Course
```http
DELETE /api/v1/lms/courses/{course_id}/
```

#### Enroll in Course
```http
POST /api/v1/lms/enrollments/
```

**Request Body:**
```json
{
  "course_id": 1
}
```

#### Get Course Progress
```http
GET /api/v1/lms/courses/{course_id}/progress/
```

### 💰 Crowdfunding Endpoints (Week 3 - Coming Soon)

#### List Projects
```http
GET /api/v1/crowdfunding/projects/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search in project title and description
- `status`: Filter by project status (draft, active, completed, cancelled)
- `category`: Filter by project category
- `min_goal`: Minimum goal amount
- `max_goal`: Maximum goal amount

#### Create Project
```http
POST /api/v1/crowdfunding/projects/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Build a New Computer Lab",
  "description": "Help us build a state-of-the-art computer lab for our students",
  "goal_amount": 50000.00,
  "start_date": "2024-02-01",
  "end_date": "2024-04-01",
  "category": "education",
  "metadata": {
    "images": ["https://example.com/lab1.jpg"],
    "videos": ["https://example.com/demo.mp4"],
    "faq": [
      {
        "question": "When will the lab be completed?",
        "answer": "We expect to complete the lab by June 2024"
      }
    ]
  }
}
```

#### Get Project Details
```http
GET /api/v1/crowdfunding/projects/{project_id}/
```

#### Update Project
```http
PUT /api/v1/crowdfunding/projects/{project_id}/
PATCH /api/v1/crowdfunding/projects/{project_id}/
```

#### Make Pledge
```http
POST /api/v1/crowdfunding/pledges/
```

**Request Body:**
```json
{
  "project_id": 1,
  "amount": 100.00,
  "payment_method": "stripe",
  "reward_id": 2,
  "anonymous": false,
  "message": "Great project! Happy to support."
}
```

### 🔧 Core Endpoints

#### Health Check
```http
GET /api/v1/core/health/
```

**Response:**
```json
{
  "status": "healthy",
  "message": "EduCrowd API is running",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "celery": "healthy"
  }
}
```

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  },
  "errors": []
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "meta": {},
  "errors": [
    {
      "field": "email",
      "message": "This field is required.",
      "code": "required"
    }
  ]
}
```

## 🔒 Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## 🔄 Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "results": [...],
  "count": 100,
  "next": "http://api.educrowd.com/v1/endpoint/?page=2",
  "previous": null
}
```

## 🔍 Filtering and Searching

### Search
Most list endpoints support search via the `search` parameter:

```http
GET /api/v1/lms/courses/?search=python
```

### Filtering
Use query parameters to filter results:

```http
GET /api/v1/crowdfunding/projects/?status=active&min_goal=1000&max_goal=10000
```

### Ordering
Use the `ordering` parameter to sort results:

```http
GET /api/v1/lms/courses/?ordering=-created_at
```

## 📝 Rate Limiting

API requests are rate limited:

- **Authenticated users**: 1000 requests per hour
- **Unauthenticated users**: 100 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 🔐 Webhooks

EduCrowd supports webhooks for real-time notifications:

### Webhook Events

- `user.registered`
- `user.verified`
- `course.created`
- `course.enrolled`
- `project.created`
- `project.pledged`
- `payment.completed`
- `payment.failed`

### Webhook Payload

```json
{
  "event": "course.enrolled",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "user_id": 123,
    "course_id": 456,
    "tenant_id": 789
  }
}
```

## 🧪 Testing

### Test Environment

Use the test environment for development and testing:

```
Base URL: https://test-api.educrowd.com/v1/
```

### Test Credentials

```
Email: test@educrowd.com
Password: test123
```

### Postman Collection

Import our Postman collection for easy API testing:

[Download Postman Collection](https://api.educrowd.com/docs/postman-collection.json)

## 📚 SDKs

Official SDKs are available for:

- **Python**: `pip install educrowd-python-sdk`
- **JavaScript**: `npm install educrowd-js-sdk`
- **PHP**: `composer require educrowd/php-sdk`

## 🆘 Support

For API support:

- **Documentation**: https://docs.educrowd.com
- **Support Email**: api-support@educrowd.com
- **Status Page**: https://status.educrowd.com
- **GitHub Issues**: https://github.com/educrowd/api/issues

---

**API Version**: v1.0.0  
**Last Updated**: January 2024  
**Next Update**: February 2024 (LMS Module)
