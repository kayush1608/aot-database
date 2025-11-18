from sql import create
from gui import app, get_credentials
import streamlit as st
import sys
import subprocess

if __name__ == "__main__":
    if (st.runtime.scriptrunner.get_script_run_ctx() is None):
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])
        sys.exit()
    if 'db_credentials' not in st.session_state:
        get_credentials()
    else:
        app()

