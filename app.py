import streamlit as st
import requests

HOSPITAL_INFO = "You are an AI assistant for Udayananda Hospitals, Nandyal. Phone: 08514222999. Open 24 hours. Departments: Cardiology, Neurology, Orthopedics, Pediatrics, Gynecology, Surgery, ICU, Emergency, Radiology. Answer in English or Telugu. For emergencies provide: 08514222999"

st.set_page_config(page_title="Udayananda Hospitals", page_icon="🏥")
st.title("🏥 Udayananda Hospitals")
st.caption("AI Patient Assistant — Available 24/7")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "నమస్కారం! Welcome to Udayananda Hospitals! How can I help you today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("..."):
            msgs = [{"role": "system", "content": HOSPITAL_INFO}] + st.session_state.messages
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}", "Content-Type": "application/json"}, json={"model": "llama3-8b-8192", "messages": msgs})
                reply = r.json()["choices"][0]["message"]["content"]
            except:
                reply = "Please call 08514222999 for assistance."
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
st.caption("🚑 Emergency: 08514222999 | 📍 Collector Office Road, Nandyal")
