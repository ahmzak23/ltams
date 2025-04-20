#!/bin/bash

# Create the database if it doesn't exist
echo "Creating database if it doesn't exist..."
PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE ticketdb;" || true

# Initialize the database
echo "Initializing database..."
python backend/init_db.py

# Start the application
echo "Starting the application..."
docker-compose up -d

echo "Application started successfully!"
echo "Frontend is available at: http://localhost:3000"
echo "API Gateway is available at: http://localhost:4000"
echo "Backend is available at: http://localhost:8000"
echo ""
echo "Login credentials:"
echo "Admin: admin@example.com / admin123"
echo "User: user@example.com / user123" 