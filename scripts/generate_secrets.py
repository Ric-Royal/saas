import secrets
import string
import base64
import os
from pathlib import Path
import sys

def generate_secure_string(length=32, include_special=True):
    """Generate a cryptographically secure random string."""
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_jwt_secret():
    """Generate a secure JWT secret."""
    return base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

def generate_api_key():
    """Generate an API key."""
    return secrets.token_urlsafe(32)

def generate_secrets():
    """Generate all required secrets."""
    return {
        'JWT_SECRET': generate_jwt_secret(),
        'POSTGRES_PASSWORD': generate_secure_string(24),
        'REDIS_PASSWORD': generate_secure_string(24),
        'NEO4J_PASSWORD': generate_secure_string(24),
        'AWS_ACCESS_KEY_ID': generate_api_key(),
        'AWS_SECRET_ACCESS_KEY': generate_api_key(),
    }

def validate_env_file(env_path):
    """Validate that all required variables are present in the env file."""
    required_vars = [
        'NODE_ENV',
        'PORT',
        'HOST',
        'BASE_URL',
        'POSTGRES_SERVER',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'REDIS_HOST',
        'REDIS_PASSWORD',
        'JWT_SECRET',
        'NEO4J_PASSWORD',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY'
    ]
    
    if not env_path.exists():
        print(f"Error: {env_path} does not exist")
        return False
        
    with open(env_path, 'r') as f:
        content = f.read()
        
    missing_vars = []
    for var in required_vars:
        if f"{var}=" not in content and f"${var}" not in content:
            missing_vars.append(var)
            
    if missing_vars:
        print(f"Error: Missing required variables in {env_path}:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
        
    return True

def update_env_file(template_path, output_path, secrets, is_docker=False):
    """Update environment file with generated secrets."""
    if not template_path.exists():
        print(f"Error: Template file {template_path} not found")
        return False

    with open(template_path, 'r') as f:
        content = f.read()

    # Replace placeholders with generated secrets
    for key, value in secrets.items():
        content = content.replace(f"${key}", value)

    # Adjust environment-specific variables
    if is_docker:
        content = content.replace("localhost", "host.docker.internal")
        content = content.replace("NODE_ENV=development", "NODE_ENV=production")

    with open(output_path, 'w') as f:
        f.write(content)

    return validate_env_file(output_path)

def main():
    # Generate secrets
    secrets = generate_secrets()
    
    # Define paths
    template_path = Path('.env.template')
    env_path = Path('.env')
    docker_env_path = Path('.env.docker')
    
    # Update development environment
    print("\nGenerating development environment...")
    if update_env_file(template_path, env_path, secrets):
        print("✅ Development environment (.env) created successfully")
    else:
        print("❌ Failed to create development environment")
        sys.exit(1)
    
    # Update Docker environment
    print("\nGenerating Docker environment...")
    if update_env_file(template_path, docker_env_path, secrets, is_docker=True):
        print("✅ Docker environment (.env.docker) created successfully")
    else:
        print("❌ Failed to create Docker environment")
        sys.exit(1)
    
    # Print the generated secrets
    print("\nGenerated Secrets (Save these securely):")
    for key, value in secrets.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 