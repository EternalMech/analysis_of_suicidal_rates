# define variables

STREAMLIT_APP = app/main.py
FASTAPI_APP = api.main

.PHONY: frontend backend run_app

frontend:
	streamlit run $(STREAMLIT_APP)

backend:
	uvicorn $(FASTAPI_APP):app --port 8070 --reload &

run_app: backend frontend