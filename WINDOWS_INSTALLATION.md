# QT.AI Trading Bot - Windows 11 Installation Guide

This guide provides step-by-step instructions for installing and running the QT.AI Trading Bot on Windows 11.

## Prerequisites

1. **Windows 11 Operating System**
   - Make sure your system is updated to the latest version

2. **Python 3.10 or higher**
   - Download and install from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

3. **Git for Windows**
   - Download and install from [git-scm.com](https://git-scm.com/download/win)

4. **Docker Desktop for Windows** (optional, for full system deployment)
   - Download and install from [docker.com](https://www.docker.com/products/docker-desktop)
   - Requires WSL2 to be enabled

## Option 1: Download Pre-built Executables

1. **Clone the Repository**
   ```
   git clone https://github.com/jiffyjenga/QT.AI.git
   cd QT.AI
   ```

2. **Run the Executables**
   - Navigate to the `executables` directory
   - Right-click on each .exe file and select "Run as administrator"
   - Allow the application through Windows Defender if prompted

## Option 2: Build Executables Yourself

1. **Clone the Repository**
   ```
   git clone https://github.com/jiffyjenga/QT.AI.git
   cd QT.AI
   ```

2. **Run the Build Script**
   - Double-click on `build_windows_executables.bat`
   - This will install the required packages and build the executables
   - The executables will be available in the `executables` directory

## Running the QT.AI Trading Bot

### Individual Components

1. **Backend (QT.AI_Backend.exe)**
   - Provides the FastAPI server for handling API requests
   - Run this first before other components

2. **Frontend (QT.AI_Frontend.exe)**
   - Launches a web server with the trading dashboard
   - Access through your browser at http://localhost:8080

3. **AI Module (QT.AI_AI_Module.exe)**
   - Demonstrates the AI and sentiment analysis capabilities
   - Shows sample predictions and sentiment analysis

4. **Security (QT.AI_Security.exe)**
   - Shows the security features including encryption and JWT handling
   - Demonstrates API key encryption and token generation

5. **Docker Setup (QT.AI_Docker_Setup.exe)**
   - Creates Docker configuration files for running the full system
   - Requires Docker Desktop to be installed

### Full System Deployment with Docker

1. Run `QT.AI_Docker_Setup.exe` to create Docker configuration files
2. Open Docker Desktop
3. Open Command Prompt in the QT.AI directory
4. Run `docker-compose up -d`
5. Access the application at http://localhost

## Troubleshooting

- **Windows Protected Your PC Message**
  - Click "More info"
  - Select "Run anyway"

- **Executables Fail to Run**
  - Make sure you have the latest .NET Framework installed
  - Check Windows Defender or antivirus settings
  - Try running in compatibility mode (right-click > Properties > Compatibility)

- **Docker Issues**
  - Make sure WSL2 is enabled
  - Restart Docker Desktop
  - Check Docker logs for errors

## Support

If you encounter any issues, please create an issue on the GitHub repository.
