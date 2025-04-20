@echo off
echo Creating database if it doesn't exist...
set PGPASSWORD=postgres
psql -h localhost -U postgres -c "CREATE DATABASE ticketdb;" || echo Database already exists

echo Initializing database...
python backend/init_db.py

echo Starting the application...
docker-compose up -d

echo Application started successfully!
echo Frontend is available at: http://localhost:3000
echo API Gateway is available at: http://localhost:4000
echo Backend is available at: http://localhost:8000
echo.
echo Login credentials:
echo Admin: admin@example.com / admin123
echo User: user@example.com / user123 