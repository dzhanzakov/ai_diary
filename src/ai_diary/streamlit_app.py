import streamlit as st
import tempfile
from pathlib import Path
from ai_diary.main import TranscriberFlow
import os

st.markdown(
    """
    <style>
    .main-title {
        font-size:2.5rem;
        font-weight:700;
        color:#4F8BF9;
        margin-bottom:0.5em;
    }
    .subtitle {
        font-size:1.2rem;
        color:#555;
        margin-bottom:1.5em;
    }
    .footer {
        margin-top:2em;
        color:#888;
        font-size:0.9em;
        text-align:center;
    }
    .stButton>button {
        background-color: #4F8BF9;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 2em;
        margin-top: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🎤 Create AI Diary</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Record your diary topic and let AI transcribe and summarize it for you.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with col1:
    audio_value = st.audio_input("Record a voice message")
    if audio_value:
        st.audio(audio_value)

with col2:
    st.info("Click the microphone to start recording. When done, click 'Transcribe and Generate new Diary'.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("Audio is processed securely and deleted after transcription.")

if audio_value:
    if st.button("Transcribe and Generate new AI Diary", use_container_width=True):
        script_dir = Path(__file__).parent
        output_path = script_dir / "output.wav"
        with open(output_path, "wb") as out_file:
            out_file.write(audio_value.read())

        with st.spinner("Transcribing and generating summary..."):
            flow = TranscriberFlow()
            flow.kickoff()
            transcript = flow.state.transcript
            meeting_minutes = flow.state.meeting_minutes

        st.success("Transcription complete!")

        with st.expander("📝 Transcript", expanded=False):
            st.write(transcript)
        with st.expander("📋 Diary Summary", expanded=True):
            st.write(meeting_minutes)

        if output_path.exists():
            os.remove(output_path)

st.markdown('<div class="footer">Made with ❤️ using Streamlit', unsafe_allow_html=True)
