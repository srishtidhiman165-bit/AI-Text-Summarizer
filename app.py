

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝"
)

st.title("📝 AI Text Summarizer")
st.write("Turn long text into short, clear summaries using AI.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your Gemini API key to the .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

text = st.text_area(
    "Paste your text here",
    height=250,
    placeholder="Paste an article, lecture notes, or any long text..."
)

style = st.selectbox(
    "Choose summary style",
    ["Short", "Detailed", "Bullet Points", "Simple English"]
)

if st.button("Generate Summary"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Summarizing your text..."):
            try:
                prompt = f"""
                Summarize the following text.
                Summary style: {style}.
                Keep the summary accurate and clear.
                Do not add facts that are not in the original text.

                Text:
                {text}
                """

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.subheader("Your Summary")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
