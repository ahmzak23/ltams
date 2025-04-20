@echo off
echo Starting the application...
docker-compose up -d

echo Waiting for the database to be ready...
timeout /t 10

echo Initializing the database...
docker-compose run --rm db-init

echo Application started successfully!
echo Frontend is available at: http://localhost:3000
echo API Gateway is available at: http://localhost:4000
echo Backend is available at: http://localhost:8000
echo.
echo Login credentials:
echo Admin: admin@example.com / admin123
echo User: user@example.com / user123 