#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import secrets
import string
import re
from typing import Dict, List, Tuple
import json
from dataclasses import dataclass
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

@dataclass
class EnvVariable:
    name: str
    value: str
    comment: str = ""
    section: str = ""
    required: bool = False

class EnvGenerator:
    def __init__(self):
        self.template_path = Path('.env.template')
        self.env_path = Path('.env')
        self.sections: Dict[str, List[EnvVariable]] = {}
        self.current_section = ""

    def generate_secure_key(self, length: int = 32) -> str:
        """Generate a secure random key."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def generate_jwt_secret(self) -> str:
        """Generate a secure JWT secret."""
        return secrets.token_urlsafe(32)

    def parse_template(self) -> None:
        """Parse the .env.template file."""
        if not self.template_path.exists():
            print(f"{Fore.RED}Error: .env.template file not found{Style.RESET_ALL}")
            sys.exit(1)

        with open(self.template_path, 'r', encoding='utf-8') as f:
            current_comment = ""
            
            for line in f:
                line = line.strip()
                
                # Handle section comments
                if line.startswith('# ') and not '=' in line:
                    self.current_section = line[2:]
                    if self.current_section not in self.sections:
                        self.sections[self.current_section] = []
                    continue
                
                # Handle variable comments
                if line.startswith('#') and not '=' in line:
                    current_comment = line[1:].strip()
                    continue
                
                # Handle variable definitions
                if '=' in line and not line.startswith('#'):
                    name, value = line.split('=', 1)
                    name = name.strip()
                    value = value.strip()
                    
                    # Extract inline comment if present
                    inline_comment = ""
                    if '#' in value:
                        value, inline_comment = value.split('#', 1)
                        value = value.strip()
                        inline_comment = inline_comment.strip()
                    
                    comment = inline_comment if inline_comment else current_comment
                    current_comment = ""
                    
                    # Determine if variable is required
                    required = not value or value in ['', '""', "''"]
                    
                    var = EnvVariable(
                        name=name,
                        value=value,
                        comment=comment,
                        section=self.current_section,
                        required=required
                    )
                    
                    if self.current_section not in self.sections:
                        self.sections[self.current_section] = []
                    self.sections[self.current_section].append(var)

    def generate_value(self, var: EnvVariable) -> str:
        """Generate an appropriate value for an environment variable."""
        # If value is already set and not empty, use it
        if var.value and var.value not in ['', '""', "''"]:
            return var.value
            
        # Generate values based on variable name patterns
        name = var.name.upper()
        
        if 'SECRET' in name or 'KEY' in name:
            return self.generate_secure_key()
        elif 'PASSWORD' in name:
            return self.generate_secure_key(16)
        elif 'PORT' in name:
            return str(self.get_available_port())
        elif 'HOST' in name:
            return '0.0.0.0'
        elif 'URL' in name:
            if 'DATABASE' in name or 'DB' in name:
                return 'postgresql://user:password@localhost:5432/dbname'
            elif 'REDIS' in name:
                return 'redis://localhost:6379/0'
            elif 'API' in name:
                return 'http://localhost:3000/api'
            else:
                return 'http://localhost:3000'
        elif 'PATH' in name:
            if 'LOG' in name:
                return 'logs/app.log'
            elif 'SSL' in name or 'CERT' in name:
                return f'/etc/nginx/ssl/{name.lower()}.pem'
        
        # Default values for common settings
        if name == 'NODE_ENV':
            return 'development'
        elif name == 'LOG_LEVEL':
            return 'info'
        elif name == 'ENVIRONMENT':
            return 'development'
        
        # For any other variables, ask the user
        return self.prompt_user(var)

    def get_available_port(self, start: int = 3000) -> int:
        """Find an available port starting from the given number."""
        import socket
        port = start
        while port < 65535:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                port += 1
        return start

    def prompt_user(self, var: EnvVariable) -> str:
        """Prompt the user for a value."""
        default = var.value if var.value and var.value not in ['', '""', "''"] else None
        prompt = f"\n{Fore.CYAN}{var.name}{Style.RESET_ALL}"
        
        if var.comment:
            prompt += f"\n{Fore.YELLOW}{var.comment}{Style.RESET_ALL}"
            
        if default:
            prompt += f"\nDefault: {default}"
            
        prompt += f"\nEnter value{' (required)' if var.required else ''}: "
        
        while True:
            value = input(prompt).strip()
            if not value and default:
                return default
            if not value and var.required:
                print(f"{Fore.RED}This value is required.{Style.RESET_ALL}")
                continue
            return value or default or ''

    def generate_env_file(self) -> None:
        """Generate the .env file."""
        if self.env_path.exists():
            backup_path = self.env_path.with_suffix('.env.backup')
            self.env_path.rename(backup_path)
            print(f"{Fore.YELLOW}Existing .env file backed up to {backup_path}{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}Generating .env file...{Style.RESET_ALL}\n")
        
        with open(self.env_path, 'w', encoding='utf-8') as f:
            for section, variables in self.sections.items():
                # Write section header
                f.write(f"# {section}\n")
                
                for var in variables:
                    # Write comment if present
                    if var.comment:
                        f.write(f"# {var.comment}\n")
                    
                    # Generate and write value
                    value = self.generate_value(var)
                    f.write(f"{var.name}={value}\n")
                
                # Add newline between sections
                f.write("\n")
        
        print(f"\n{Fore.GREEN}Successfully generated .env file at {self.env_path}{Style.RESET_ALL}")

def main():
    generator = EnvGenerator()
    print(f"{Fore.CYAN}Environment File Generator{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        generator.parse_template()
        generator.generate_env_file()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Generation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main() 