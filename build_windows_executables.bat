@echo off
echo Installing required packages...
pip install pyinstaller
pip install -r requirements.txt

echo Creating executables directory...
mkdir executables

echo Building Backend executable...
pyinstaller --onefile --name QT.AI_Backend.exe create_backend_exe.py

echo Building AI Module executable...
pyinstaller --onefile --name QT.AI_AI_Module.exe create_ai_exe.py

echo Building Security executable...
pyinstaller --onefile --name QT.AI_Security.exe create_security_exe.py

echo Building Docker Setup executable...
pyinstaller --onefile --name QT.AI_Docker_Setup.exe create_docker_exe.py

echo Building Frontend executable...
pyinstaller --onefile --name QT.AI_Frontend.exe create_frontend_exe.py

echo Moving executables to the executables directory...
move dist\QT.AI_Backend.exe executables\
move dist\QT.AI_AI_Module.exe executables\
move dist\QT.AI_Security.exe executables\
move dist\QT.AI_Docker_Setup.exe executables\
move dist\QT.AI_Frontend.exe executables\

echo Build complete! Executables are available in the executables directory.
pause
