# start_apps.py
import threading
import subprocess
import os


def run_fastapi():
    # Set the working directory to where the FastAPI app is located
    os.chdir("backend/app")
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    # Set the working directory to where the Streamlit app is located
    streamlit_path = os.path.abspath('../../app.py')
    subprocess.run(["streamlit", "run", streamlit_path])

if __name__ == "__main__":
    # Create threads for FastAPI and Streamlit
    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)
    
    # Start both threads
    fastapi_thread.start()
    streamlit_thread.start()
    
    # Wait for both threads to complete
    fastapi_thread.join()
    streamlit_thread.join()
