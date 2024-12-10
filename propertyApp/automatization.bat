@echo off
call .venv\Scripts\activate
start cmd /k "uvicorn Server:app --reload --host 127.0.0.1 --port 8000"
start cmd /k "streamlit run app.py"
