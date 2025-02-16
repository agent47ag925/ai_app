#!/bin/bash
API_PORT=8000 python fastapp.py &
streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 
