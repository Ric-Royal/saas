# SaaS Microservices Platform

A comprehensive, scalable, and secure microservices-based SaaS platform offering multiple interconnected services for civic engagement, agricultural insights, and technical content management.

## Services

1. **Public Participation Service** (Port: 8000)
   - Parliamentary bill engagement platform
   - Public commenting and discussion system
   - Knowledge graph-based bill relationship visualization
   - Real-time bill tracking and notifications
   - Built with FastAPI, PostgreSQL, Neo4j, and Redis

2. **CivilBot** (Port: 8001)
   - WhatsApp-integrated legislative assistant
   - Multi-language support (English, Swahili, French)
   - NLP-powered intent recognition and response
   - Conversational bill information access
   - Integration with Public Participation Service
   - Built with FastAPI, MongoDB, and Redis
   - Features:
     - Automated bill status updates
     - Natural language query processing
     - Custom alert preferences
     - Multi-channel support (WhatsApp, Telegram)

3. **BillBot** (Port: 8002)
   - Automated bill management and tracking system
   - Features:
     - Real-time bill status monitoring
     - Automated PDF parsing and data extraction
     - Custom notification system
     - Analytics dashboard with trend analysis
     - Subscription management with Stripe integration
     - Bill comparison and historical tracking
     - Export functionality (PDF, CSV, Excel)
     - Custom tagging and categorization
   - Built with FastAPI, PostgreSQL, Redis
   - Integration points:
     - Stripe for payment processing
     - AWS S3 for document storage
     - Elasticsearch for full-text search
     - Redis for caching and real-time updates

4. **Agricultural Market Insights** (Port: 8003)
   - Real-time market data analytics platform
   - Features:
     - ML-powered price predictions
     - Weather impact analysis
     - Supply chain monitoring
     - Custom alert system
     - Market trend visualization
     - Crop planning tools
   - Built with FastAPI, PostgreSQL, Redis
   - Integration with external APIs:
     - Weather services
     - Market data providers
     - Satellite imagery

5. **Tech Blog** (Port: 3004)
   - Modern technical content platform
   - Features:
     - Rich text editing with markdown
     - Code syntax highlighting
     - Real-time collaboration
     - SEO optimization
     - Analytics dashboard
   - Built with Node.js, Express, MongoDB
   - Integration with:
     - AWS S3 for media storage
     - Algolia for search
     - Auth0 for authentication

## Architecture

### Backend Technologies
- **Primary Languages**: Python 3.11+, Node.js 18+
- **Frameworks**: FastAPI, Express
- **Databases**:
  - PostgreSQL 13+ (Public Participation, BillBot, Agri-Insights)
  - MongoDB 5+ (CivilBot, Tech Blog)
  - Neo4j 4.4+ (Public Participation - Graph Database)
  - Redis (Caching, Message Queue)
  - Elasticsearch (Full-text search)

### Frontend Technologies
- **Framework**: Next.js 13+
- **Language**: TypeScript 5+
- **UI Libraries**: 
  - TailwindCSS
  - Material-UI
  - Chakra UI
- **State Management**: 
  - Redux Toolkit
  - React Query
  - Zustand

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring Stack**:
  - Prometheus (Metrics)
  - Grafana (Visualization)
  - ELK Stack (Logging)
  - Jaeger (Tracing)
- **Security**:
  - WAF (ModSecurity)
  - Rate Limiting
  - JWT Authentication
  - SSL/TLS encryption

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd saas
```

2. Run the unified setup script:
```powershell
# For Windows (PowerShell)
./scripts/setup-env.ps1 -Environment development

# For Unix-like systems
./scripts/setup-env.sh development
```

3. Start the platform:
```bash
docker-compose up -d
```

## Environment Management

The platform uses a unified environment configuration system:

- Single `.env` file generated from templates
- Environment-specific overrides
- Secure secret management
- Service-specific configurations

### Configuration Structure

```
/
├── .env                    # Main configuration file (generated)
├── infrastructure/
│   ├── security/          # Security configurations
│   ├── monitoring/        # Monitoring setup
│   └── gateway/           # API Gateway configuration
├── services/              # Microservices
│   ├── public-participation/
│   ├── civilbot/
│   ├── billbot/
│   ├── agri-insights/
│   └── tech-blog/
└── scripts/              # Utility scripts
    ├── setup-env.ps1    # Windows setup script
    └── setup-env.sh     # Unix setup script
```

## Development

### Project Structure
```
/
├── services/                # Microservices
│   ├── public-participation/
│   ├── civilbot/
│   ├── billbot/
│   ├── agri-insights/
│   └── tech-blog/
├── frontend/               # Main landing page
├── infrastructure/         # Infrastructure configuration
│   ├── k8s/               # Kubernetes manifests
│   ├── security/          # Security configurations
│   └── monitoring/        # Monitoring setup
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

### Local Development
1. Install service dependencies:
```bash
# For Python services
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# For Node.js services
npm install
```

2. Start services individually:
```bash
# Python services
uvicorn app.main:app --reload

# Node.js services
npm run dev
```

## Monitoring and Logging

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Kibana: http://localhost:5601
- Jaeger UI: http://localhost:16686

## Security

- All services use JWT for authentication
- HTTPS enforced in production
- Rate limiting implemented
- Regular security audits with automated tools
- Secrets management through environment variables

## Backup and Recovery

- Automated daily backups for all databases
- Point-in-time recovery capability
- Backup retention policy: 30 days
- Regular backup testing and verification

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: /docs
- Issue Tracker: GitHub Issues
- Email Support: support@example.com 

## Environment Management

The project uses a standardized environment management system across all services:

### Structure
- `.env.example` - Template file with all possible configuration options
- `.env.development` - Development environment overrides (created by setup script)
- `.env.production` - Production environment overrides
- `.env` - Active environment file (created by setup script)

### Setup Instructions

1. Initialize the environment:
```powershell
# For development environment (default)
.\scripts\setup-env.ps1

# For production environment
.\scripts\setup-env.ps1 -Environment production

# For staging environment
.\scripts\setup-env.ps1 -Environment staging
```

2. The setup script will:
   - Copy the base configuration from `.env.example`
   - Apply environment-specific overrides
   - Set up service-specific environment files
   - Install dependencies for each service

### Environment Variables

The environment configuration is organized into categories:
- Global Configuration
- Service Ports
- Database Configuration (PostgreSQL, MongoDB, Neo4j)
- Redis Configuration
- JWT Authentication
- API Keys
- Monitoring and Logging
- Security Settings
- Backup Configuration

See `.env.example` for all available options and their descriptions.

## 🚀 Deployment Guide

### Production Configuration

The platform uses a production-ready Docker Compose configuration that's available in `docker-compose.yml`. This configuration includes all necessary services, networking, and volume management for a production environment.

### Deployment Steps

1. **Pre-deployment**:
```bash
# 1. Generate production secrets
python scripts/generate_secrets.py --env production

# 2. Verify environment files
python scripts/validate_env.py
```

2. **Build and Deploy**:
```bash
# 1. Build all images
docker-compose build

# 2. Start services in order
docker-compose up -d postgres mongodb redis neo4j
sleep 30  # Wait for databases to be ready
docker-compose up -d public-participation civilbot billbot agri-insights tech-blog
sleep 15  # Wait for services to be ready
docker-compose up -d gateway frontend prometheus grafana
```

3. **Post-deployment Verification**:
```bash
# 1. Check service health
curl http://localhost:3000/health

# 2. Verify database migrations
docker-compose exec public-participation alembic upgrade head
docker-compose exec billbot alembic upgrade head

# 3. Monitor logs
docker-compose logs -f
```

4. **Monitoring Access**:
- Grafana dashboard: http://localhost:3005 (admin/admin)
- Prometheus metrics: http://localhost:9090

### Important Notes
- Always generate new secrets for production deployment
- Verify all environment variables before deployment
- Follow the service startup order to ensure proper initialization
- Monitor the logs during initial deployment for any issues
- Change default monitoring credentials immediately after deployment