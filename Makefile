.PHONY: install-deps dev test lint clean

# Development
dev:
	docker-compose up -d

dev-build:
	docker-compose up -d --build

dev-down:
	docker-compose down

# Dependencies
install-deps:
	@echo "Installing dependencies for all services..."
	@for service in churn-prediction civilbot billbot agri-insights; do \
		cd services/$$service && pip install -r requirements.txt || true; \
		cd ../..; \
	done

# Testing
test:
	@echo "Running tests for all services..."
	@for service in churn-prediction civilbot billbot agri-insights; do \
		cd services/$$service && python -m pytest || true; \
		cd ../..; \
	done

# Linting
lint:
	@echo "Running linters..."
	@for service in churn-prediction civilbot billbot agri-insights; do \
		cd services/$$service && flake8 . || true; \
		cd ../..; \
	done

# Cleanup
clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Infrastructure
infra-init:
	cd infrastructure/terraform && terraform init

infra-plan:
	cd infrastructure/terraform && terraform plan

infra-apply:
	cd infrastructure/terraform && terraform apply

# Documentation
docs-serve:
	cd docs && mkdocs serve

# Database
db-migrate:
	@echo "Running database migrations..."
	@for service in churn-prediction billbot; do \
		cd services/$$service && alembic upgrade head || true; \
		cd ../..; \
	done

# Monitoring
monitoring-up:
	docker-compose up -d prometheus grafana

monitoring-down:
	docker-compose stop prometheus grafana 