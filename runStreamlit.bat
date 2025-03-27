@echo off
echo Checking for virtual environment...

if not exist venv\ (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Virtual environment found.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running application...
python app.py

echo Application execution completed.
pause
