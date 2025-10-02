# 🚀 EduCrowd - Multi-Tenant SaaS + LMS + Crowdfunding Platform

A comprehensive Django-based platform that combines Multi-Tenant SaaS architecture, Learning Management System (LMS), and Crowdfunding capabilities into a single, powerful solution.

## 🎯 Project Overview

EduCrowd is designed to solve real-world problems for educational institutions, businesses, and organizations that need:

- **Multi-Tenant SaaS**: Secure, isolated workspaces for multiple organizations
- **Learning Management**: Course delivery, progress tracking, and assessment tools
- **Crowdfunding**: Project funding, payment processing, and donor management

## 🏗️ System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Frontend]
        MOBILE[Mobile App]
        API_CLIENT[API Clients]
    end
    
    subgraph "Load Balancer"
        LB[Nginx Load Balancer]
    end
    
    subgraph "Application Layer"
        DJANGO[Django Application]
        CELERY[Celery Workers]
        BEAT[Celery Beat Scheduler]
    end
    
    subgraph "Data Layer"
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis Cache)]
        FILES[File Storage]
    end
    
    subgraph "External Services"
        EMAIL[Email Service]
        PAYMENT[Payment Gateways]
        AI[AI Services]
    end
    
    WEB --> LB
    MOBILE --> LB
    API_CLIENT --> LB
    LB --> DJANGO
    DJANGO --> POSTGRES
    DJANGO --> REDIS
    DJANGO --> FILES
    DJANGO --> CELERY
    CELERY --> REDIS
    CELERY --> EMAIL
    CELERY --> PAYMENT
    CELERY --> AI
    BEAT --> CELERY
```

### Multi-Tenant Data Architecture

```mermaid
graph TB
    subgraph "Tenant Isolation Strategy"
        TENANT_ID[Tenant ID in Every Table]
        SHARED_SCHEMA[Shared Database Schema]
        ROW_LEVEL[Row-Level Security]
    end
    
    subgraph "Database Tables"
        USERS[Users Table<br/>+ tenant_id]
        COURSES[Courses Table<br/>+ tenant_id]
        PROJECTS[Projects Table<br/>+ tenant_id]
        ORDERS[Orders Table<br/>+ tenant_id]
    end
    
    subgraph "Middleware Layer"
        TENANT_MW[Tenant Middleware]
        AUTH_MW[Authentication Middleware]
        PERM_MW[Permission Middleware]
    end
    
    TENANT_MW --> TENANT_ID
    AUTH_MW --> USERS
    PERM_MW --> ROW_LEVEL
    SHARED_SCHEMA --> USERS
    SHARED_SCHEMA --> COURSES
    SHARED_SCHEMA --> PROJECTS
    SHARED_SCHEMA --> ORDERS
```

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```mermaid
erDiagram
    TENANT ||--o{ DOMAIN : has
    TENANT ||--o{ USER_ROLE : contains
    TENANT ||--o{ COURSE : owns
    TENANT ||--o{ PROJECT : owns
    TENANT ||--o{ AUDIT_LOG : generates
    TENANT ||--|| TENANT_SETTINGS : has
    
    USER ||--o{ USER_ROLE : has
    USER ||--o{ USER_PROFILE : has
    USER ||--o{ USER_SESSION : creates
    USER ||--o{ COURSE_ENROLLMENT : enrolls
    USER ||--o{ PROJECT_PLEDGE : pledges
    USER ||--o{ AUDIT_LOG : performs
    
    COURSE ||--o{ LESSON : contains
    COURSE ||--o{ QUIZ : has
    COURSE ||--o{ COURSE_ENROLLMENT : enrolled_by
    COURSE ||--o{ PROGRESS : tracks
    
    LESSON ||--o{ LESSON_CONTENT : contains
    LESSON ||--o{ PROGRESS : tracks
    
    QUIZ ||--o{ QUIZ_QUESTION : contains
    QUIZ ||--o{ QUIZ_ATTEMPT : attempted_by
    
    PROJECT ||--o{ PROJECT_PLEDGE : receives
    PROJECT ||--o{ PROJECT_REWARD : offers
    PROJECT ||--o{ PROJECT_UPDATE : publishes
    
    TENANT {
        int id PK
        string name
        string description
        string email
        string website
        string timezone
        string language
        string currency
        boolean is_active
        json settings
        json features
        string subscription_plan
        string subscription_status
        datetime subscription_expires_at
        datetime created_at
        datetime updated_at
    }
    
    USER {
        int id PK
        string username
        string email
        string first_name
        string last_name
        string phone_number
        string avatar
        date date_of_birth
        text bio
        boolean is_verified
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    USER_ROLE {
        int id PK
        int user_id FK
        int tenant_id FK
        string role
        boolean is_active
        int assigned_by FK
        datetime assigned_at
        datetime expires_at
    }
    
    COURSE {
        int id PK
        int tenant_id FK
        string title
        text description
        string status
        decimal price
        int duration_hours
        string level
        json metadata
        datetime created_at
        datetime updated_at
    }
    
    PROJECT {
        int id PK
        int tenant_id FK
        string title
        text description
        decimal goal_amount
        decimal current_amount
        string status
        date start_date
        date end_date
        json metadata
        datetime created_at
        datetime updated_at
    }
```

## 🔄 System Flow Diagrams

### User Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database
    participant R as Redis
    participant E as Email Service
    
    U->>F: Enter credentials
    F->>A: POST /api/v1/auth/login/
    A->>D: Validate credentials
    D-->>A: User data
    A->>R: Store session
    A->>D: Create audit log
    A-->>F: JWT tokens + user data
    F-->>U: Login successful
    
    Note over U,E: Email Verification Flow
    U->>F: Register new account
    F->>A: POST /api/v1/auth/register/
    A->>D: Create user
    A->>E: Send verification email
    E-->>U: Verification email
    U->>F: Click verification link
    F->>A: POST /api/v1/auth/verify-email/
    A->>D: Mark user as verified
    A-->>F: Verification successful
```

### Multi-Tenant Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant LB as Load Balancer
    participant MW as Middleware
    participant V as View
    participant D as Database
    participant T as Tenant Context
    
    C->>LB: HTTP Request
    LB->>MW: Route to Django
    MW->>MW: Extract tenant from domain/subdomain
    MW->>T: Set tenant context
    MW->>V: Process request with tenant context
    V->>D: Query with tenant_id filter
    D-->>V: Tenant-specific data
    V-->>MW: Response data
    MW-->>LB: HTTP Response
    LB-->>C: Response
```

### Course Enrollment Flow

```mermaid
sequenceDiagram
    participant S as Student
    participant F as Frontend
    participant A as API
    participant D as Database
    participant C as Celery
    participant E as Email Service
    participant N as Notification Service
    
    S->>F: Browse courses
    F->>A: GET /api/v1/lms/courses/
    A->>D: Query courses for tenant
    D-->>A: Course list
    A-->>F: Course data
    F-->>S: Display courses
    
    S->>F: Enroll in course
    F->>A: POST /api/v1/lms/enrollments/
    A->>D: Create enrollment
    A->>C: Queue welcome email task
    A->>C: Queue notification task
    C->>E: Send welcome email
    C->>N: Send enrollment notification
    A-->>F: Enrollment successful
    F-->>S: Confirmation
```

### Crowdfunding Pledge Flow

```mermaid
sequenceDiagram
    participant B as Backer
    participant F as Frontend
    participant A as API
    participant D as Database
    participant P as Payment Gateway
    participant C as Celery
    participant E as Email Service
    
    B->>F: View project
    F->>A: GET /api/v1/crowdfunding/projects/{id}/
    A->>D: Query project details
    D-->>A: Project data
    A-->>F: Project information
    F-->>B: Display project
    
    B->>F: Make pledge
    F->>A: POST /api/v1/crowdfunding/pledges/
    A->>P: Process payment
    P-->>A: Payment result
    A->>D: Create pledge record
    A->>D: Update project amount
    A->>C: Queue confirmation email
    A->>C: Queue project update task
    C->>E: Send confirmation email
    A-->>F: Pledge successful
    F-->>B: Confirmation
```

## 🏢 Multi-Tenant Architecture Details

### Tenant Isolation Strategy

```mermaid
graph TB
    subgraph "Request Processing"
        REQ[HTTP Request]
        DOMAIN[Domain/Subdomain Detection]
        TENANT_LOOKUP[Tenant Lookup]
        CONTEXT[Set Tenant Context]
    end
    
    subgraph "Database Layer"
        SHARED_DB[(Shared PostgreSQL Database)]
        TENANT_FILTER[tenant_id Filter]
        ROW_SECURITY[Row-Level Security]
    end
    
    subgraph "Application Layer"
        MIDDLEWARE[Tenant Middleware]
        VIEWS[Django Views]
        SERIALIZERS[DRF Serializers]
    end
    
    REQ --> DOMAIN
    DOMAIN --> TENANT_LOOKUP
    TENANT_LOOKUP --> CONTEXT
    CONTEXT --> MIDDLEWARE
    MIDDLEWARE --> VIEWS
    VIEWS --> TENANT_FILTER
    TENANT_FILTER --> SHARED_DB
    SHARED_DB --> ROW_SECURITY
```

### Data Security Model

```mermaid
graph TB
    subgraph "Authentication Layer"
        JWT[JWT Tokens]
        SESSION[Session Management]
        RBAC[Role-Based Access Control]
    end
    
    subgraph "Tenant Isolation"
        TENANT_ID[Tenant ID Validation]
        DOMAIN_CHECK[Domain Verification]
        PERMISSION_CHECK[Permission Verification]
    end
    
    subgraph "Data Access"
        QUERY_FILTER[Query Filtering]
        AUDIT_LOG[Audit Logging]
        ENCRYPTION[Data Encryption]
    end
    
    JWT --> TENANT_ID
    SESSION --> DOMAIN_CHECK
    RBAC --> PERMISSION_CHECK
    TENANT_ID --> QUERY_FILTER
    DOMAIN_CHECK --> AUDIT_LOG
    PERMISSION_CHECK --> ENCRYPTION
```

## 🔧 Technology Stack & Integration

### Backend Architecture

```mermaid
graph TB
    subgraph "Django Framework"
        MODELS[Django Models]
        VIEWS[Django Views]
        SERIALIZERS[DRF Serializers]
        MIDDLEWARE[Custom Middleware]
    end
    
    subgraph "Authentication"
        JWT[JWT Authentication]
        ALLAUTH[Django Allauth]
        PERMISSIONS[Django Permissions]
    end
    
    subgraph "Multi-Tenancy"
        TENANT_MW[Tenant Middleware]
        TENANT_MODELS[Tenant Models]
        DOMAIN_MODELS[Domain Models]
    end
    
    subgraph "Background Tasks"
        CELERY[Celery Workers]
        REDIS_QUEUE[Redis Queue]
        PERIODIC[Periodic Tasks]
    end
    
    subgraph "External Integrations"
        STRIPE[Stripe Payments]
        RAZORPAY[Razorpay Payments]
        OPENAI[OpenAI Integration]
        EMAIL_SERVICE[Email Service]
    end
    
    MODELS --> TENANT_MODELS
    VIEWS --> JWT
    SERIALIZERS --> PERMISSIONS
    MIDDLEWARE --> TENANT_MW
    CELERY --> REDIS_QUEUE
    CELERY --> STRIPE
    CELERY --> EMAIL_SERVICE
```

## 📈 Scalability & Performance

### Horizontal Scaling Strategy

```mermaid
graph TB
    subgraph "Load Balancer Layer"
        NGINX[Nginx Load Balancer]
        SSL[SSL Termination]
        STATIC[Static File Serving]
    end
    
    subgraph "Application Servers"
        APP1[Django App Server 1]
        APP2[Django App Server 2]
        APP3[Django App Server 3]
    end
    
    subgraph "Database Layer"
        MASTER_DB[(PostgreSQL Master)]
        REPLICA_DB[(PostgreSQL Replica)]
        REDIS_CLUSTER[(Redis Cluster)]
    end
    
    subgraph "Background Processing"
        CELERY1[Celery Worker 1]
        CELERY2[Celery Worker 2]
        CELERY3[Celery Worker 3]
    end
    
    NGINX --> APP1
    NGINX --> APP2
    NGINX --> APP3
    APP1 --> MASTER_DB
    APP2 --> REPLICA_DB
    APP3 --> MASTER_DB
    CELERY1 --> REDIS_CLUSTER
    CELERY2 --> REDIS_CLUSTER
    CELERY3 --> REDIS_CLUSTER
```

## 🚀 8-Week Development Plan

### Week 1 ✅ - Project Scaffolding
- [x] Django project setup with multi-tenancy
- [x] Docker containerization
- [x] User management system
- [x] Tenant management system
- [x] Basic API structure

### Week 2 - Authentication & Tenant Management
- [ ] JWT authentication implementation
- [ ] Tenant creation workflows
- [ ] Shared-schema tenancy implementation
- [ ] Admin interface enhancements

### Week 3 - LMS Module
- [ ] Course management system
- [ ] Lesson and content management
- [ ] Quiz and assessment system
- [ ] Teacher and student dashboards

### Week 4 - Crowdfunding Module
- [ ] Project creation and management
- [ ] Pledge system
- [ ] Payment integration (sandbox)
- [ ] Backer management

### Week 5 - Billing & Subscriptions
- [ ] Stripe integration
- [ ] Webhook handling
- [ ] Tenant billing model
- [ ] Subscription management

### Week 6 - Real-time Features
- [ ] Redis + Channels implementation
- [ ] Real-time notifications
- [ ] Celery task optimization
- [ ] Email and receipt automation

### Week 7 - Testing & Documentation
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline setup
- [ ] API documentation (Swagger)
- [ ] Performance testing

### Week 8 - Deployment & Production
- [ ] Staging environment setup
- [ ] Security hardening
- [ ] Production deployment
- [ ] Monitoring and logging

## 🏗️ Architecture

### Week 1 - Project Scaffolding ✅
- Django project setup with multi-tenancy support
- Docker containerization
- User management with custom authentication
- Tenant management system
- Basic API structure

### Week 2 - LMS Module (Coming Soon)
- Course and lesson management
- Quiz and assessment system
- Progress tracking and analytics
- Student and teacher dashboards

### Week 3 - Crowdfunding Module (Coming Soon)
- Project creation and management
- Payment gateway integration
- Rewards and perks system
- Real-time analytics

## 🛠️ Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL with multi-tenancy support
- **Cache**: Redis
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT + Django Allauth
- **Payment**: Stripe, Razorpay integration
- **AI/ML**: OpenAI, HuggingFace (optional)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EduCrowd
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - Web Interface: http://localhost:8000
   - Django Admin: http://localhost:8000/admin
   - API Documentation: http://localhost:8000/api/v1/

## 📁 Project Structure

```
EduCrowd/
├── apps/
│   ├── users/           # User management and authentication
│   ├── tenants/         # Multi-tenant architecture
│   ├── lms/            # Learning Management System
│   ├── crowdfunding/   # Crowdfunding platform
│   └── core/           # Shared utilities
├── educrowd/           # Django project settings
├── templates/          # HTML templates
├── static/            # Static files
├── media/             # Media files
├── logs/              # Application logs
├── docker-compose.yml # Docker configuration
├── Dockerfile         # Docker image definition
└── requirements.txt   # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Key environment variables you need to configure:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=educrowd
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

## 🎯 Key Features

### Multi-Tenant SaaS Module
- ✅ Tenant registration and management
- ✅ Role-based access control (RBAC)
- ✅ Customizable settings per tenant
- ✅ Audit logs for compliance
- ✅ Secure data isolation

### Learning Management System (LMS)
- 🔄 Course and lesson management
- 🔄 Quiz and assessment system
- 🔄 Progress tracking and analytics
- 🔄 Student and teacher dashboards
- 🔄 AI-powered quiz generation

### Crowdfunding Platform
- 🔄 Project creation and management
- 🔄 Secure payment processing
- 🔄 Rewards and perks system
- 🔄 Real-time analytics
- 🔄 Backer management

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/password/change/` - Change password
- `POST /api/v1/auth/password/reset/` - Request password reset

### Tenants
- `GET /api/v1/tenants/` - List tenants
- `POST /api/v1/tenants/` - Create tenant
- `GET /api/v1/tenants/{id}/` - Get tenant details
- `PUT /api/v1/tenants/{id}/` - Update tenant
- `DELETE /api/v1/tenants/{id}/` - Delete tenant

### Health Check
- `GET /api/v1/core/health/` - System health status

## 🐳 Docker Services

The application runs with the following services:

- **web**: Django application server
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery**: Background task worker
- **celery-beat**: Periodic task scheduler

## 🧪 Development

### Running Tests
```bash
docker-compose exec web python manage.py test
```

### Code Quality
```bash
# Run linting
docker-compose exec web flake8 .

# Run type checking
docker-compose exec web mypy .
```

### Database Management
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 📊 Monitoring and Logging

- Application logs are stored in the `logs/` directory
- Celery task monitoring available via Django admin
- Health check endpoint for monitoring: `/api/v1/core/health/`

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Multi-tenant data isolation
- Audit logging for compliance
- CSRF protection
- XSS protection
- Secure password validation

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
2. **Configure reverse proxy (Nginx)**
3. **Set up SSL certificates**
4. **Configure database backups**
5. **Set up monitoring and logging**

### Environment-specific Settings

- Development: `DEBUG=True`, local database
- Staging: `DEBUG=False`, staging database
- Production: `DEBUG=False`, production database with SSL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

## 🗓️ Roadmap

### Week 1 ✅
- [x] Project scaffolding
- [x] Docker setup
- [x] User management
- [x] Tenant management
- [x] Basic API structure

### Week 2 (Planned)
- [ ] LMS module implementation
- [ ] Course management
- [ ] Quiz system
- [ ] Progress tracking

### Week 3 (Planned)
- [ ] Crowdfunding module
- [ ] Payment integration
- [ ] Project management
- [ ] Analytics dashboard

---

**Built with ❤️ using Django, Docker, and modern web technologies**
