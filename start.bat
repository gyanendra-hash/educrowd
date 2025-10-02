@echo off
REM EduCrowd Startup Script for Windows
echo 🚀 Starting EduCrowd - Multi-Tenant SaaS + LMS + Crowdfunding Platform
echo ==================================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your configuration before continuing.
    echo    You can use the default values for development.
)

REM Build and start containers
echo 🐳 Building and starting Docker containers...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
echo 📊 Running database migrations...
docker-compose exec web python manage.py migrate

REM Create test data
echo 🧪 Creating test data...
docker-compose exec web python manage.py create_test_data

echo.
echo ✅ EduCrowd is now running!
echo.
echo 🌐 Access the application:
echo    Web Interface: http://localhost:8000
echo    Django Admin: http://localhost:8000/admin
echo    API Health: http://localhost:8000/api/v1/core/health/
echo.
echo 👤 Test credentials:
echo    Admin: admin@educrowd.com / admin123
echo    User: test@educrowd.com / test123
echo.
echo 🛠️  Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop: docker-compose down
echo    Restart: docker-compose restart
echo.
echo Happy coding! 🎉
pause
