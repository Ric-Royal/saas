#!/bin/bash

echo "Starting Security Audit..."

# Run dependency vulnerability scan
echo "Scanning dependencies..."
for service in services/*/; do
  if [ -f "${service}package.json" ]; then
    echo "Scanning Node.js dependencies in ${service}..."
    cd "${service}" && npm audit
  elif [ -f "${service}requirements.txt" ]; then
    echo "Scanning Python dependencies in ${service}..."
    safety check -r requirements.txt
  fi
done

# Run container security scan
echo "Scanning containers..."
docker-compose ps -q | xargs -I {} docker inspect {} | \
  trivy image --severity HIGH,CRITICAL

# Run OWASP ZAP scan for web applications
echo "Running OWASP ZAP scan..."
docker run --rm -v $(pwd)/infrastructure/security/reports:/zap/wrk/:rw \
  -t owasp/zap2docker-stable zap-baseline.py \
  -t http://tech-blog-frontend \
  -t http://agri-insights-frontend \
  -r security-report.html

# Check for exposed secrets
echo "Checking for exposed secrets..."
docker run --rm -v $(pwd):/src trufflesecurity/trufflehog \
  filesystem /src --json > infrastructure/security/reports/secrets-report.json

# Run static code analysis
echo "Running static code analysis..."
for service in services/*/; do
  if [ -f "${service}package.json" ]; then
    echo "Analyzing JavaScript/TypeScript code in ${service}..."
    cd "${service}" && npm run lint
  elif [ -f "${service}requirements.txt" ]; then
    echo "Analyzing Python code in ${service}..."
    bandit -r "${service}"
  fi
done

# Check SSL/TLS configuration
echo "Checking SSL/TLS configuration..."
docker run --rm -t drwetter/testssl.sh \
  tech-blog-frontend:443 > infrastructure/security/reports/ssl-report.txt

# Generate final report
echo "Generating final security report..."
cat << EOF > infrastructure/security/reports/audit-summary.md
# Security Audit Summary
Date: $(date)

## Vulnerability Scans
- Dependencies scan results: See npm-audit.json and safety-check.txt
- Container scan results: See trivy-results.json
- Web application scan: See security-report.html
- Secrets scan: See secrets-report.json
- Static code analysis: See static-analysis/
- SSL/TLS configuration: See ssl-report.txt

## Recommendations
Please review the detailed reports in the reports directory and address any findings
based on their severity level.

## Next Steps
1. Review and fix all HIGH and CRITICAL vulnerabilities
2. Update dependencies with known security issues
3. Address any exposed secrets
4. Implement recommended security headers
5. Fix any SSL/TLS configuration issues
EOF

echo "Security audit complete. Reports available in infrastructure/security/reports/" 