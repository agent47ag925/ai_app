#!/bin/bash
streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
uvicorn fastapp:app --reload --host=0.0.0.0 --port=${PORT}