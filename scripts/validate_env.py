#!/usr/bin/env python3
import os
import sys
from typing import Dict, List, Optional
import re
from urllib.parse import urlparse

class EnvValidator:
    def __init__(self):
        self.required_vars = {
            'database': [
                'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB',
                'MONGO_USER', 'MONGO_PASSWORD',
                'NEO4J_USER', 'NEO4J_PASSWORD',
                'REDIS_PASSWORD'
            ],
            'services': [
                'PORT_PUBLIC_PARTICIPATION', 'PORT_CIVILBOT',
                'PORT_BILLBOT', 'PORT_AGRI_INSIGHTS',
                'PORT_TECH_BLOG', 'GATEWAY_PORT', 'GRAFANA_PORT'
            ],
            'security': [
                'JWT_SECRET', 'CORS_ORIGIN'
            ]
        }
        self.url_vars = [
            'POSTGRES_URI', 'DATABASE_URL',
            'MONGODB_URI_CIVILBOT', 'MONGODB_URI_TECH_BLOG',
            'REDIS_URL', 'NEO4J_URI'
        ]
        self.port_vars = [
            'PORT_PUBLIC_PARTICIPATION', 'PORT_CIVILBOT',
            'PORT_BILLBOT', 'PORT_AGRI_INSIGHTS',
            'PORT_TECH_BLOG', 'GATEWAY_PORT', 'GRAFANA_PORT'
        ]
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_required_vars(self, env: Dict[str, str]) -> bool:
        missing_vars = []
        for category, vars in self.required_vars.items():
            for var in vars:
                if var not in env or not env[var]:
                    missing_vars.append(var)
        
        if missing_vars:
            self.errors.append(f"Missing required variables: {', '.join(missing_vars)}")
            return False
        return True

    def validate_urls(self, env: Dict[str, str]) -> bool:
        valid = True
        for var in self.url_vars:
            if var in env:
                url = env[var]
                try:
                    result = urlparse(url)
                    if not all([result.scheme, result.netloc]):
                        self.errors.append(f"Invalid URL format for {var}: {url}")
                        valid = False
                except Exception as e:
                    self.errors.append(f"Error parsing URL for {var}: {str(e)}")
                    valid = False
        return valid

    def validate_ports(self, env: Dict[str, str]) -> bool:
        valid = True
        used_ports = {}
        for var in self.port_vars:
            if var in env:
                try:
                    port = int(env[var])
                    if port < 1024 or port > 65535:
                        self.errors.append(f"Port number for {var} must be between 1024 and 65535")
                        valid = False
                    elif port in used_ports:
                        self.errors.append(f"Port conflict: {var} and {used_ports[port]} both use port {port}")
                        valid = False
                    else:
                        used_ports[port] = var
                except ValueError:
                    self.errors.append(f"Invalid port number for {var}: {env[var]}")
                    valid = False
        return valid

    def validate_security(self, env: Dict[str, str]) -> None:
        if 'JWT_SECRET' in env:
            if len(env['JWT_SECRET']) < 32:
                self.warnings.append("JWT_SECRET should be at least 32 characters long")
            if env['JWT_SECRET'] == 'REPLACE_WITH_SECURE_SECRET':
                self.errors.append("JWT_SECRET is using default value")

        for key in env:
            if key.endswith('_KEY') or key.endswith('_SECRET'):
                if env[key].startswith('your-'):
                    self.errors.append(f"{key} is using placeholder value")

    def validate_env_file(self, env_file: str) -> bool:
        if not os.path.exists(env_file):
            self.errors.append(f"Environment file {env_file} not found")
            return False

        env = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        key, value = line.split('=', 1)
                        env[key.strip()] = value.strip()
                    except ValueError:
                        self.warnings.append(f"Invalid line in {env_file}: {line}")

        valid = True
        valid &= self.validate_required_vars(env)
        valid &= self.validate_urls(env)
        valid &= self.validate_ports(env)
        self.validate_security(env)

        return valid

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_env.py <env_file>")
        sys.exit(1)

    env_file = sys.argv[1]
    validator = EnvValidator()
    
    print(f"\nValidating environment file: {env_file}")
    print("=" * 50)
    
    is_valid = validator.validate_env_file(env_file)

    if validator.warnings:
        print("\nWarnings:")
        for warning in validator.warnings:
            print(f"⚠️  {warning}")

    if validator.errors:
        print("\nErrors:")
        for error in validator.errors:
            print(f"❌ {error}")
    
    if is_valid and not validator.errors:
        print("\n✅ Environment file is valid!")
        sys.exit(0)
    else:
        print("\n❌ Environment file validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 