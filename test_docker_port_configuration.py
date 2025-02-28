#!/usr/bin/env python3
"""
Test script to verify the Docker port configuration has been updated correctly.
"""
import os
import sys
import yaml
import re

def test_docker_compose_port_configuration():
    """Test that the Docker Compose file uses port 3000 for the frontend."""
    print("Testing Docker Compose port configuration...")
    
    # Check if the docker-compose.windows.yml file exists
    if not os.path.exists('docker-compose.windows.yml'):
        print("❌ Error: docker-compose.windows.yml file not found")
        return False
    
    # Read the docker-compose.windows.yml file
    with open('docker-compose.windows.yml', 'r') as f:
        try:
            compose_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing docker-compose.windows.yml: {e}")
            return False
    
    # Check if the frontend service exists
    if 'services' not in compose_data or 'frontend' not in compose_data['services']:
        print("❌ Error: Frontend service not found in docker-compose.windows.yml")
        return False
    
    # Check if the ports are configured correctly
    if 'ports' not in compose_data['services']['frontend']:
        print("❌ Error: Ports not configured for frontend service")
        return False
    
    # Check if port 3000 is mapped to port 80
    frontend_ports = compose_data['services']['frontend']['ports']
    port_mapping = None
    for port in frontend_ports:
        if isinstance(port, str) and '3000:80' in port:
            port_mapping = port
            break
    
    if not port_mapping:
        print("❌ Error: Port 3000 not mapped to port 80 for frontend service")
        return False
    
    print("✅ Frontend service correctly configured to use port 3000")
    return True

def test_build_script_port_references():
    """Test that the build script references port 3000 for the frontend."""
    print("Testing build script port references...")
    
    # Check if the build_windows_docker.bat file exists
    if not os.path.exists('build_windows_docker.bat'):
        print("❌ Error: build_windows_docker.bat file not found")
        return False
    
    # Read the build_windows_docker.bat file
    with open('build_windows_docker.bat', 'r') as f:
        build_script = f.read()
    
    # Check if the script references port 3000
    if 'http://localhost:3000' not in build_script:
        print("❌ Error: build_windows_docker.bat does not reference port 3000")
        return False
    
    print("✅ Build script correctly references port 3000")
    return True

def test_readme_port_references():
    """Test that the README references port 3000 for the frontend."""
    print("Testing README port references...")
    
    # Check if the README.md file exists in the windows_build_docker directory
    if not os.path.exists('windows_build_docker/README.md'):
        print("❌ Error: windows_build_docker/README.md file not found")
        return False
    
    # Read the README.md file
    with open('windows_build_docker/README.md', 'r') as f:
        readme = f.read()
    
    # Check if the README references port 3000
    if 'http://localhost:3000' not in readme:
        print("❌ Error: README does not reference port 3000")
        return False
    
    print("✅ README correctly references port 3000")
    return True

def test_docker_package_contents():
    """Test that the Docker package contains the updated files."""
    print("Testing Docker package contents...")
    
    # Check if the QT.AI_Windows_Docker.zip file exists
    if not os.path.exists('QT.AI_Windows_Docker.zip'):
        print("❌ Error: QT.AI_Windows_Docker.zip file not found")
        return False
    
    # We can't easily check the contents of the zip file in this script,
    # but we can check if it was recently updated
    if not os.path.getmtime('QT.AI_Windows_Docker.zip') > os.path.getmtime('docker-compose.windows.yml'):
        print("❌ Warning: QT.AI_Windows_Docker.zip may not contain the latest changes")
        return False
    
    print("✅ Docker package appears to be up to date")
    return True

def main():
    """Run all tests and report results."""
    print("=== Docker Port Configuration Test ===")
    
    tests = [
        test_docker_compose_port_configuration,
        test_build_script_port_references,
        test_readme_port_references,
        test_docker_package_contents
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n=== Test Summary ===")
    if all(results):
        print("✅ All tests passed! Docker configuration has been successfully updated to use port 3000.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
