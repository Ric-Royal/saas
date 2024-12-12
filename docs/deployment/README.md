# Deployment Guide

## Prerequisites
- Docker and Docker Compose
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Nginx
- SSL certificate

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Environment Variables
Create `.env` files for different environments:

```bash
# .env.production
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET=your-secret-key
```

### 3. Docker Deployment

#### Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d
```

#### Container Management
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Database Setup
```bash
# Run migrations
npm run migrate

# Seed initial data
npm run seed
```

### 5. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Monitoring Setup

### 1. ELK Stack
```bash
# Start ELK stack
docker-compose -f docker-compose.elk.yml up -d

# Access Kibana
http://localhost:5601
```

### 2. Prometheus & Grafana
```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
http://localhost:3000
```

## Backup Procedures

### Database Backup
```bash
# Automated backup script
0 0 * * * /usr/local/bin/backup-script.sh

# Manual backup
pg_dump -U username dbname > backup.sql
```

### File Storage Backup
```bash
# Backup uploaded files
rsync -avz /path/to/uploads/ /path/to/backup/
```

## SSL Configuration
```bash
# Install certbot
apt-get install certbot

# Generate certificate
certbot --nginx -d yourdomain.com

# Auto-renewal
certbot renew --dry-run
```

## Troubleshooting

### Common Issues

1. **Container Startup Failures**
   ```bash
   # Check logs
   docker-compose logs <service-name>
   ```

2. **Database Connection Issues**
   ```bash
   # Test connection
   pg_isready -h localhost -p 5432
   ```

3. **Redis Connection Issues**
   ```bash
   # Test Redis
   redis-cli ping
   ```

### Health Checks
```bash
# API health check
curl http://localhost:3000/health

# Database health check
npm run db:health

# Redis health check
npm run redis:health
```

## Rollback Procedures

### 1. Application Rollback
```bash
# Revert to previous version
git checkout <previous-tag>
docker-compose up -d --build
```

### 2. Database Rollback
```bash
# Revert last migration
npm run migrate:down

# Restore from backup
psql dbname < backup.sql
```

## Security Checklist
- [ ] SSL certificates installed
- [ ] Firewall configured
- [ ] Security headers enabled
- [ ] Rate limiting configured
- [ ] Database backups automated
- [ ] Monitoring alerts set up
- [ ] Access logs enabled
- [ ] Error logging configured 