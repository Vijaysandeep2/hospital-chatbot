import streamlit as st
import requests

HOSPITAL_INFO = """You are an AI assistant for Udayananda Hospitals, Nandyal.
- Name: Udayananda Hospitals
- Location: Collector Office Road, Nandyal
- Phone: 08514222999, 09144467444
- Timings: Open 24 hours, 7 days a week
- Type: 250 bed multispecialty tertiary care hospital
- Ambulance: 24/7 available
- Departments: Cardiology, Neurology, Orthopedics, Pediatrics, Gynecology, Surgery, ICU, Emergency, Radiology
- Answer in English or Telugu based on patient language
- For emergencies always provide: 08514222999
"""

st.set_page_config(page_title="Udayananda Hospitals", page_icon="🏥")
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🏥")
with col2:
    st.title("Udayananda Hospitals")
    st.caption("AI Patient Assistant — Available 24/7")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "నమస్కారం! Welcome to Udayananda Hospitals! 🏥\n\nI can help with appointments, departments, timings, and emergencies.\n\nHow can I assist you?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your question... (English or Telugu)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("..."):
            messages = [{"role": "system", "content": HOSPITAL_INFO}]
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}", "Content-Type": "application/json"},
                    json={"model": "llama3-8b-8192", "messages": messages}
                )
                reply = response.json()["choices"][0]["message"]["content"]
            except:
                reply = "Sorry, please call 08514222999 for assistance."
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
st.caption("🚑 Emergency: 08514222999 | 📍 Collector Office Road, Nandyal")
