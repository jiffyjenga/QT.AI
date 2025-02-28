#!/usr/bin/env python3
"""
Test script to verify Windows Docker compatibility for QT.AI Trading Bot.
This script checks the Docker configuration files for Windows compatibility.
"""

import os
import sys
import re
import subprocess
import json
from datetime import datetime

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")

def check_file_exists(filepath):
    """Check if a file exists."""
    exists = os.path.isfile(filepath)
    print(f"Checking {filepath}: {'✅ Found' if exists else '❌ Not found'}")
    return exists

def check_windows_compatibility(dockerfile_path):
    """Check if a Dockerfile is Windows-compatible."""
    if not os.path.isfile(dockerfile_path):
        print(f"❌ {dockerfile_path} not found")
        return False
    
    with open(dockerfile_path, 'r') as f:
        content = f.read()
    
    # Check for Windows base image
    windows_base = re.search(r'FROM\s+mcr\.microsoft\.com/windows', content, re.IGNORECASE)
    if not windows_base:
        print(f"❌ {dockerfile_path} does not use a Windows base image")
        return False
    
    print(f"✅ {dockerfile_path} uses a Windows-compatible base image")
    return True

def check_docker_compose(compose_path):
    """Check if docker-compose.yml is Windows-compatible."""
    if not os.path.isfile(compose_path):
        print(f"❌ {compose_path} not found")
        return False
    
    with open(compose_path, 'r') as f:
        content = f.read()
    
    # Check for Windows network driver
    windows_network = re.search(r'driver:\s*nat', content, re.IGNORECASE)
    if not windows_network:
        print(f"❌ {compose_path} does not use Windows NAT network driver")
        return False
    
    print(f"✅ {compose_path} is configured for Windows containers")
    return True

def check_build_script(script_path):
    """Check if the build script is Windows-compatible."""
    if not os.path.isfile(script_path):
        print(f"❌ {script_path} not found")
        return False
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Check for Windows batch file syntax
    windows_syntax = re.search(r'@echo off', content, re.IGNORECASE)
    if not windows_syntax:
        print(f"❌ {script_path} does not use Windows batch file syntax")
        return False
    
    print(f"✅ {script_path} is a valid Windows batch file")
    return True

def check_zip_package(zip_path):
    """Check if the zip package exists and contains required files."""
    if not os.path.isfile(zip_path):
        print(f"❌ {zip_path} not found")
        return False
    
    # Check zip contents using unzip -l
    try:
        result = subprocess.run(['unzip', '-l', zip_path], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        
        required_files = [
            'Dockerfile.backend.windows',
            'Dockerfile.frontend.windows',
            'docker-compose.windows.yml',
            'build_windows_docker.bat',
            'README.md'
        ]
        
        missing_files = []
        for file in required_files:
            if file not in result.stdout:
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ {zip_path} is missing required files: {', '.join(missing_files)}")
            return False
        
        print(f"✅ {zip_path} contains all required files")
        return True
    
    except subprocess.CalledProcessError:
        print(f"❌ Failed to check contents of {zip_path}")
        return False

def generate_report():
    """Generate a Windows Docker compatibility report."""
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tests": {
            "dockerfile_backend": check_windows_compatibility("Dockerfile.backend.windows"),
            "dockerfile_frontend": check_windows_compatibility("Dockerfile.frontend.windows"),
            "docker_compose": check_docker_compose("docker-compose.windows.yml"),
            "build_script": check_build_script("build_windows_docker.bat"),
            "zip_package": check_zip_package("QT.AI_Windows_Docker.zip")
        }
    }
    
    # Calculate overall result
    report["overall_result"] = all(report["tests"].values())
    
    # Write report to file
    with open("DOCKER_WINDOWS_COMPATIBILITY_REPORT.md", "w") as f:
        f.write("# QT.AI Trading Bot - Windows Docker Compatibility Report\n\n")
        f.write(f"Generated: {report['timestamp']}\n\n")
        f.write(f"## Overall Result: {'✅ PASS' if report['overall_result'] else '❌ FAIL'}\n\n")
        
        f.write("## Test Results\n\n")
        for test, result in report["tests"].items():
            f.write(f"- {test}: {'✅ PASS' if result else '❌ FAIL'}\n")
        
        f.write("\n## Windows Compatibility Notes\n\n")
        f.write("### Docker on Windows Requirements\n\n")
        f.write("- Windows 11 or Windows 10 Pro/Enterprise/Education (Build 2004 or later)\n")
        f.write("- Docker Desktop for Windows with Windows containers enabled\n")
        f.write("- Hyper-V and Containers Windows features enabled\n")
        f.write("- At least 4GB of RAM dedicated to Docker Desktop\n\n")
        
        f.write("### Known Limitations\n\n")
        f.write("- Windows containers are larger than Linux containers\n")
        f.write("- Startup time is longer for Windows containers\n")
        f.write("- Some Python packages may require additional configuration on Windows\n")
        f.write("- Windows containers cannot run on Linux hosts and vice versa\n\n")
        
        f.write("### Installation Instructions\n\n")
        f.write("1. Install Docker Desktop for Windows\n")
        f.write("2. Switch to Windows containers (right-click Docker icon in system tray)\n")
        f.write("3. Extract QT.AI_Windows_Docker.zip\n")
        f.write("4. Run build_windows_docker.bat\n")
        f.write("5. Access the application at http://localhost\n")
    
    print_header("Windows Docker Compatibility Report Generated")
    print(f"Overall result: {'✅ PASS' if report['overall_result'] else '❌ FAIL'}")
    print(f"Report saved to: DOCKER_WINDOWS_COMPATIBILITY_REPORT.md")
    
    return report["overall_result"]

if __name__ == "__main__":
    print_header("QT.AI Trading Bot - Windows Docker Compatibility Test")
    success = generate_report()
    sys.exit(0 if success else 1)
