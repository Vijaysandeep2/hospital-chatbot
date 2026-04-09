import streamlit as st
import requests

HOSPITAL_INFO = """You are an AI assistant for Udayananda Hospitals, Nandyal.

HOSPITAL INFORMATION:
- Name: Udayananda Hospitals
- Location: Collector Office Road, Opp. Railway Station South Gate, Nandyal, Andhra Pradesh
- Phone: 08514222999, 09144467444
- Timings: Open 24 hours, 7 days a week
- Type: 250 bed multispecialty tertiary care hospital
- Ambulance: 24/7 available

DEPARTMENTS:
- Cardiology, Neurology, Orthopedics
- Pediatrics, Gynecology, General Surgery
- ICU, Emergency, Radiology
- Pathology, Physiotherapy, Dermatology

SERVICES:
- 24/7 Emergency care
- Outpatient (OPD) consultations
- Inpatient admissions
- Diagnostic services (X-ray, MRI, CT scan)
- Blood bank available

INSTRUCTIONS:
- Answer in English or Telugu based on patient's language
- Be helpful, warm and professional
- For emergencies always provide: 08514222999
- If unsure about specific doctor availability, ask them to call
"""

st.set_page_config(
    page_title="Udayananda Hospitals - AI Assistant",
    page_icon="🏥",
    layout="centered"
)

col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🏥")
with col2:
    st.title("Udayananda Hospitals")
    st.caption("AI Patient Assistant — Available 24/7")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "నమస్కారం! Welcome to Udayananda Hospitals Nandyal! 🏥\n\nI can help you with:\n- 📅 Appointment bookings\n- 🏥 Department information\n- ⏰ Doctor timings\n- 🚑 Emergency contacts\n- 📍 Location & directions\n\nHow can I assist you today?"
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your question here... (English or Telugu)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            messages = [{"role": "system", "content": HOSPITAL_INFO}]
            for msg in st.session_state.messages:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.2-3b-instruct:free",
                    "messages": messages
                }
            )
data = response.json()
if "choices" in data:
    reply = data["choices"][0]["message"]["content"]
else:
    reply = "Sorry, I'm having trouble connecting. Please call us at 08514222999 for assistance."
        
            st.write(reply)
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

st.divider()
st.caption("🚑 Emergency: 08514222999 | 📍 Collector Office Road, Nandyal")
