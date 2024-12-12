# Create necessary directories
New-Item -ItemType Directory -Force -Path `
    infrastructure\monitoring\prometheus, `
    infrastructure\logging\logstash\pipeline, `
    frontend\logs, `
    services\public-participation\logs, `
    services\agri-insights\logs, `
    services\tech-blog\logs, `
    services\civilbot\logs

# Copy configuration files if they exist
if (Test-Path infrastructure\monitoring\prometheus\prometheus.yml.example) {
    Copy-Item infrastructure\monitoring\prometheus\prometheus.yml.example infrastructure\monitoring\prometheus\prometheus.yml
}
if (Test-Path infrastructure\logging\logstash\pipeline\logstash.conf.example) {
    Copy-Item infrastructure\logging\logstash\pipeline\logstash.conf.example infrastructure\logging\logstash\pipeline\logstash.conf
}

# Set up environment variables
if (Test-Path .env.example) {
    Copy-Item .env.example .env
}

# Build and start services
docker-compose build
docker-compose up -d

# Wait for databases to be ready
Write-Host "Waiting for databases to be ready..."
Start-Sleep -Seconds 30

# Run database migrations
docker-compose exec -T public-participation alembic upgrade head
docker-compose exec -T agri-insights alembic upgrade head
docker-compose exec -T tech-blog npx prisma migrate deploy

# Create initial superuser
$createSuperuser = @"
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
"@

docker-compose exec -T public-participation python -c "$createSuperuser"

Write-Host "Services initialized successfully!" 