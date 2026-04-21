@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.
echo Usage:
echo   python run_tests.py            - Run all tests
echo   python run_tests.py assertion  - Run assertion tests
echo   python run_tests.py visual     - Run visual tests
echo   python run_tests.py api        - Run API tests
echo.