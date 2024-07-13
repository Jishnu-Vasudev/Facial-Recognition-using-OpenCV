start cmd /c "uvicorn main:app"
TIMEOUT /T 8 /NOBREAK  >nul
start http://127.0.0.1:8000
