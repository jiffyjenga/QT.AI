# QT.AI Windows Installation Guide

## Prerequisites
- Windows 11 (latest version)
- Docker Desktop for Windows
- WSL2 enabled
- Git for Windows
- Administrator privileges

## Installation Options

### Option 1: Using Executable Files (Recommended)
1. Download the QT.AI Windows executable files from the release page
2. Extract the files to a directory of your choice
3. Run the `qtai_setup.exe` file to start the installation process
4. Follow the on-screen instructions to complete the installation
5. Once installed, you can run the application using the desktop shortcut or start menu entry

### Option 2: Using Docker
1. Install Docker Desktop for Windows
2. Enable WSL2 integration in Docker Desktop settings
3. Clone the QT.AI repository:
   ```
   git clone https://github.com/jiffyjenga/QT.AI.git
   ```
4. Navigate to the QT.AI directory:
   ```
   cd QT.AI
   ```
5. Build and start the Docker containers:
   ```
   docker-compose -f docker-compose.windows.yml up -d
   ```
6. Access the application at http://localhost:3000

### Option 3: Manual Installation
1. Install Python 3.12 for Windows
2. Install Node.js 18+ for Windows
3. Clone the QT.AI repository:
   ```
   git clone https://github.com/jiffyjenga/QT.AI.git
   ```
4. Navigate to the QT.AI directory:
   ```
   cd QT.AI
   ```
5. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```
7. Start the backend server:
   ```
   cd ..
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
8. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```
9. Access the application at http://localhost:3000

## Troubleshooting

### Port Conflicts
If you encounter port conflicts, you can change the ports in the `.env` file:
- Backend port: `BACKEND_PORT=8000`
- Frontend port: `FRONTEND_PORT=3000`

### Docker Issues
If you encounter Docker issues, try the following:
- Ensure Docker Desktop is running
- Ensure WSL2 is enabled
- Restart Docker Desktop
- Run Docker commands as administrator

### Windows Defender Firewall
If Windows Defender Firewall blocks the application, you may need to add exceptions for the following:
- `qtai_backend.exe`
- `qtai_frontend.exe`
- `qtai_ai.exe`
- `qtai_docker.exe`
- `qtai_setup.exe`

## Support
For support, please contact the jiffyjenga organization administrators.
