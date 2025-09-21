import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="YouTube Chat Assistant", layout="wide")
st.title("🎥 YouTube Chat Assistant")

# -------------------- Two columns --------------------
col1, col2 = st.columns([3, 2])

# -------------------- Left Column: Video --------------------
with col1:
    input_col, button_col = st.columns([3, 1])
    video_url = st.text_input("Paste YouTube URL here:")

    load_transcript_clicked = st.button("Load Transcript")

    video_id = None
    if video_url:
        parsed_url = urlparse(video_url)
        if "youtube" in parsed_url.netloc:
            qs = parse_qs(parsed_url.query)
            video_id = qs.get("v", [None])[0]
        elif "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path.lstrip("/")

    if load_transcript_clicked and video_id:
        with st.spinner("Loading transcript..."):
            try:
                res = requests.post(f"{API_BASE}/load_video/", json={"url": video_url})
                if res.status_code == 200:
                    data = res.json()
                    # st.success(f"Transcript loaded ({data['chunks']} chunks)")
                    # st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.error("Failed to load transcript")
            except:
                st.error("Backend not reachable")

    if video_id:
        st.video(f"https://www.youtube.com/watch?v={video_id}")

# -------------------- Right Column: Chat --------------------
with col2:
    st.subheader("💬 Chat with Video")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Form to handle chat input (auto reruns on submit)
    with st.form(key="chat_form", clear_on_submit=True):
        question = st.text_input("Type your question:")
        submitted = st.form_submit_button("Send Question")

        if submitted and question.strip():
            # Add user message
            st.session_state.chat_history.append({"role": "user", "text": question})
            try:
                res = requests.post(f"{API_BASE}/ask/", json={"question": question})
                if res.status_code == 200:
                    answer = res.json().get("answer", "No answer returned")
                    st.session_state.chat_history.append({"role": "bot", "text": answer})
                else:
                    st.session_state.chat_history.append({"role": "bot", "text": "Failed to get answer"})
            except:
                st.session_state.chat_history.append({"role": "bot", "text": "Backend not reachable"})

    # Display chat in reverse (newest on top)
    chat_lines = []
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            chat_lines.append(f"**You:** {msg['text']}")
        else:
            chat_lines.append(f"**Bot:** {msg['text']}")

    # Scrollable chat box
    st.text_area(
        "Chat",
        value="\n\n".join(chat_lines),
        height=500,
        key="chat_box",
        disabled=True
    )
