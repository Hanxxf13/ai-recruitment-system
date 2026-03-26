web: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# Note: Streamlit handles its own port internally or via command line
gui: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
