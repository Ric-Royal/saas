#!/bin/bash

# Create necessary directories
mkdir -p infrastructure/monitoring/prometheus
mkdir -p infrastructure/logging/logstash/pipeline
mkdir -p frontend/logs
mkdir -p services/public-participation/logs
mkdir -p services/agri-insights/logs
mkdir -p services/tech-blog/logs
mkdir -p services/civilbot/logs

# Copy configuration files
cp infrastructure/monitoring/prometheus/prometheus.yml.example infrastructure/monitoring/prometheus/prometheus.yml
cp infrastructure/logging/logstash/pipeline/logstash.conf.example infrastructure/logging/logstash/pipeline/logstash.conf

# Set up environment variables
cp .env.example .env

# Build and start services
docker-compose build
docker-compose up -d

# Wait for databases to be ready
echo "Waiting for databases to be ready..."
sleep 30

# Run database migrations
docker-compose exec public-participation alembic upgrade head
docker-compose exec agri-insights alembic upgrade head
docker-compose exec tech-blog npx prisma migrate deploy

# Create initial superusers
docker-compose exec public-participation python -c "
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate
from app.db.session import SessionLocal
db = SessionLocal()
crud_user.create(db, obj_in=UserCreate(
    email='admin@example.com',
    password='admin123',
    full_name='Admin User',
    is_superuser=True
))
"

echo "Services initialized successfully!" 