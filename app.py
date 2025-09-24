import streamlit as st
import speech_recognition as sr
import os

st.set_page_config(page_title="🎤 Speech Recognition App", layout="centered")
st.title("🎤 Speech Recognition App")

# Initialize session state
if "paused" not in st.session_state:
    st.session_state.paused = False
if "stopped" not in st.session_state:
    st.session_state.stopped = False
if "transcriptions" not in st.session_state:
    st.session_state.transcriptions = []

# --- User Inputs ---
api_choice = st.selectbox(
    "Select Speech Recognition API",
    ["google", "sphinx"],  # you can add more: "wit", "bing", "houndify" if you have API keys
)

language = st.text_input("Enter language code (e.g., en-US, fr-FR, es-ES):", "en-US")

filename = st.text_input("Save transcription file name:", "transcription.txt")
save_file = st.checkbox("💾 Save transcriptions to file", value=True)


def transcribe_speech(api_choice="google", language="en-US"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        if api_choice == "google":
            text = recognizer.recognize_google(audio, language=language)
        elif api_choice == "sphinx":
            text = recognizer.recognize_sphinx(audio, language=language)
        else:
            st.error("Unsupported API choice")
            return None

        # Save transcription
        st.session_state.transcriptions.append(text)
        st.success("✅ Recognized speech:")
        st.write(text)

        if save_file:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            st.info(f"Saved to {filename}")

        return text

    except sr.UnknownValueError:
        st.error("❌ Could not understand audio")
    except sr.RequestError as e:
        st.error(f"⚠️ API request error: {e}")
    except Exception as e:
        st.error(f"⚡ Unexpected error: {e}")


# --- Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Start / Resume"):
        st.session_state.paused = False
        st.session_state.stopped = False
        transcribe_speech(api_choice, language)

with col2:
    if st.button("⏸ Pause"):
        st.session_state.paused = True
        st.warning("⏸ Recognition paused.")

with col3:
    if st.button("⏹ Stop"):
        st.session_state.stopped = True
        st.session_state.paused = False
        st.warning("🛑 Recognition stopped.")


# --- Display history ---
if st.session_state.transcriptions:
    st.subheader("📝 Transcription History")
    for i, t in enumerate(st.session_state.transcriptions, 1):
        st.write(f"{i}. {t}")


