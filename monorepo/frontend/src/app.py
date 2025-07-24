import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.title("Marker Engine")

uploaded = st.file_uploader("Upload chat export")
if uploaded and st.button("Analyze"):
    files = {"file": (uploaded.name, uploaded.getvalue())}
    resp = requests.post(f"{API_URL}/api/v1/analyze", files=files)
    st.write(resp.json())
