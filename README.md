# CascadeGuard AI

A single-agent educational prototype that analyzes a directed software dependency network, traces possible downstream impact, and recommends a preventive action.

## Run on Windows
1. Install Python from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract this ZIP.
3. Open the extracted folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run:
```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```
If `py` is not recognized, try replacing `py` with `python`. A browser should open at `http://localhost:8501`. Keep the terminal open while using the app.

## Deploy online
1. Create a GitHub repository named `cascadeguard-ai-agent`.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Create/deploy an app, select the repository, branch `main`, and main file `app.py`.
5. Click Deploy and wait for the build to complete.

## Limitations
This uses a simulated network and a simple score heuristic. It does not connect to or repair real infrastructure. Clearly describe it as a prototype in your presentation.
