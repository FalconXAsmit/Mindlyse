import streamlit as st
import requests

st.set_page_config(
    page_title="Mindlyse",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mindlyse")
st.caption("AI-powered conversation analysis for detecting psychological manipulation")

with st.sidebar:
    st.markdown("### Setup")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your Gemini API key here",
        help="Get your free API key from aistudio.google.com"
    )
    st.markdown("---")
    st.markdown("**Privacy:** Your conversation is never stored. Analysis happens in real time and is discarded immediately.")
    st.markdown("**API Key:** Your key is never stored. It's only used for this request.")

uploaded_file = st.file_uploader(
    "Upload a conversation",
    type=["txt"],
    help="Supports WhatsApp exports and standard chat formats"
)

if uploaded_file and st.button("Analyze", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar first.")
        st.stop()

    with st.spinner("Analyzing conversation..."):
        response = requests.post(
            "http://localhost:8000/analyze",
            files={"file": (uploaded_file.name, uploaded_file, "text/plain")},
            headers={"X-Api-Key": api_key}
        )

    if response.status_code == 200:
        result = response.json()

        severity = result["severity"]
        color = {
            "none": "green",
            "low": "blue",
            "medium": "orange",
            "high": "red"
        }.get(severity, "gray")

        st.markdown(f"### Severity: :{color}[{severity.upper()}]")

        if result["dominant_tactic"]:
            st.markdown(f"**Dominant tactic:** {result['dominant_tactic']}")

        st.markdown("### Pattern Summary")
        st.info(result["pattern_summary"])

        if result["flagged_messages"]:
            st.markdown("### Flagged Messages")
            for flag in result["flagged_messages"]:
                with st.expander(
                    f"Message {flag['message_index']} — {flag['speaker']} — {flag['tactic']}"
                ):
                    st.markdown(f"**Tactic:** {flag['tactic']}")
                    st.markdown(f"**Why it's a red flag:** {flag['explanation']}")
        else:
            st.success("No manipulation tactics detected. This conversation appears healthy.")

    elif response.status_code == 401:
        st.error("Invalid or missing API key. Please check your key in the sidebar.")
    elif response.status_code == 422:
        st.error("No messages found in the file. Check the format and try again.")
    else:
        st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")