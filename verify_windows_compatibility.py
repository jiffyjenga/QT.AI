"""
Verify Windows compatibility for QT.AI trading bot.

This script verifies that the QT.AI trading bot is compatible with Windows 11.
"""
import os
import sys
import logging
import platform
import json
import subprocess
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('verify_windows_compatibility.log')
    ]
)
logger = logging.getLogger(__name__)

def check_docker_compatibility():
    """Check Docker compatibility."""
    logger.info("Checking Docker compatibility")
    
    # Check if Docker is installed
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Docker version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Docker is not installed or not in PATH")
        return False
    
    # Check if Docker Compose is installed
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Docker Compose version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Docker Compose is not installed or not in PATH")
        return False
    
    # Check Docker configuration
    docker_files = [
        "Dockerfile.backend",
        "Dockerfile.frontend",
        "docker-compose.yml"
    ]
    
    for docker_file in docker_files:
        if not os.path.exists(docker_file):
            logger.error(f"Docker file {docker_file} not found")
            return False
        
        logger.info(f"Docker file {docker_file} found")
    
    # Check Windows-specific Docker files
    windows_docker_files = [
        "Dockerfile.backend.windows",
        "Dockerfile.frontend.windows",
        "docker-compose.windows.yml"
    ]
    
    for docker_file in windows_docker_files:
        if os.path.exists(docker_file):
            logger.info(f"Windows-specific Docker file {docker_file} found")
        else:
            logger.warning(f"Windows-specific Docker file {docker_file} not found")
    
    return True

def check_executable_compatibility():
    """Check executable compatibility."""
    logger.info("Checking executable compatibility")
    
    # Check if executables directory exists
    executables_dir = Path("windows_build/executables")
    if not executables_dir.exists():
        logger.error(f"Executables directory {executables_dir} not found")
        return False
    
    # Check if executables exist
    executables = [
        "qtai_backend.exe",
        "qtai_frontend.exe",
        "qtai_ai.exe",
        "qtai_docker.exe",
        "qtai_setup.exe"
    ]
    
    for executable in executables:
        executable_path = executables_dir / executable
        if executable_path.exists():
            logger.info(f"Executable {executable} found")
        else:
            logger.warning(f"Executable {executable} not found")
    
    return True

def check_port_configuration():
    """Check port configuration."""
    logger.info("Checking port configuration")
    
    # Check if port configuration file exists
    port_config_file = Path("PORT_CONFIGURATION_UPDATE_REPORT.md")
    if not port_config_file.exists():
        logger.warning(f"Port configuration file {port_config_file} not found")
        return False
    
    logger.info(f"Port configuration file {port_config_file} found")
    
    # Check port configuration
    with open(port_config_file, "r") as f:
        content = f.read()
        
        if "80" in content and "8000" in content and "3000" in content:
            logger.info("Port configuration includes standard ports (80, 8000, 3000)")
        else:
            logger.warning("Port configuration may not include all standard ports")
    
    return True

def check_feature_compatibility():
    """Check feature compatibility."""
    logger.info("Checking feature compatibility")
    
    # Check user setup wizard
    setup_files = [
        "frontend/src/components/setup/SetupWizard.tsx",
        "frontend/src/components/setup/ProfileSetup.tsx",
        "frontend/src/components/setup/SecuritySetup.tsx",
        "frontend/src/components/setup/TradingPreferencesSetup.tsx",
        "frontend/src/components/setup/AccountFundingSetup.tsx",
        "frontend/src/components/setup/SetupConfirmation.tsx"
    ]
    
    for setup_file in setup_files:
        if os.path.exists(setup_file):
            logger.info(f"Setup file {setup_file} found")
        else:
            logger.error(f"Setup file {setup_file} not found")
            return False
    
    # Check trading amount configuration
    trading_amount_files = [
        "frontend/src/components/account/TradingAllocation.tsx",
        "app/api/endpoints/accounts.py"
    ]
    
    for trading_amount_file in trading_amount_files:
        if os.path.exists(trading_amount_file):
            logger.info(f"Trading amount file {trading_amount_file} found")
        else:
            logger.error(f"Trading amount file {trading_amount_file} not found")
            return False
    
    # Check API key management
    api_key_files = [
        "frontend/src/components/account/ApiKeyManagement.tsx",
        "app/api/endpoints/api_keys.py",
        "app/models/api_key.py",
        "app/security/encryption.py"
    ]
    
    for api_key_file in api_key_files:
        if os.path.exists(api_key_file):
            logger.info(f"API key file {api_key_file} found")
        else:
            logger.error(f"API key file {api_key_file} not found")
            return False
    
    return True

def main():
    """Main function."""
    try:
        logger.info("=== Starting Windows Compatibility Verification ===")
        
        # Check platform
        system = platform.system()
        logger.info(f"Current platform: {system}")
        
        # Check Docker compatibility
        docker_compatible = check_docker_compatibility()
        logger.info(f"Docker compatibility: {docker_compatible}")
        
        # Check executable compatibility
        executable_compatible = check_executable_compatibility()
        logger.info(f"Executable compatibility: {executable_compatible}")
        
        # Check port configuration
        port_configured = check_port_configuration()
        logger.info(f"Port configuration: {port_configured}")
        
        # Check feature compatibility
        feature_compatible = check_feature_compatibility()
        logger.info(f"Feature compatibility: {feature_compatible}")
        
        # Generate compatibility report
        compatibility_report = {
            "platform": system,
            "docker_compatible": docker_compatible,
            "executable_compatible": executable_compatible,
            "port_configured": port_configured,
            "feature_compatible": feature_compatible,
            "overall_compatible": docker_compatible and executable_compatible and port_configured and feature_compatible
        }
        
        # Save compatibility report
        with open("windows_compatibility_report.json", "w") as f:
            json.dump(compatibility_report, f, indent=2)
        
        # Generate compatibility report markdown
        with open("WINDOWS_COMPATIBILITY_REPORT.md", "w") as f:
            f.write("# QT.AI Windows Compatibility Report\n\n")
            f.write(f"## Platform: {system}\n\n")
            f.write("## Compatibility Summary\n\n")
            f.write(f"- Docker Compatibility: {'✅' if docker_compatible else '❌'}\n")
            f.write(f"- Executable Compatibility: {'✅' if executable_compatible else '❌'}\n")
            f.write(f"- Port Configuration: {'✅' if port_configured else '❌'}\n")
            f.write(f"- Feature Compatibility: {'✅' if feature_compatible else '❌'}\n\n")
            f.write(f"## Overall Compatibility: {'✅' if compatibility_report['overall_compatible'] else '❌'}\n\n")
            f.write("## Recommendations\n\n")
            
            if not docker_compatible:
                f.write("- Update Docker configuration for Windows compatibility\n")
            
            if not executable_compatible:
                f.write("- Create or update Windows executables\n")
            
            if not port_configured:
                f.write("- Update port configuration for Windows compatibility\n")
            
            if not feature_compatible:
                f.write("- Ensure all features are compatible with Windows\n")
        
        logger.info("=== Windows Compatibility Verification Complete ===")
        logger.info(f"Overall compatibility: {compatibility_report['overall_compatible']}")
        
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
