

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

# Read API key from environment or Streamlit Cloud Secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "GEMINI_API_KEY is missing. "
        "Please check Streamlit Cloud Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

text = st.text_area(
    "Paste your text here",
    height=250,
    placeholder="Paste a paragraph or article to summarize..."
)

summary_length = st.selectbox(
    "Choose summary length",
    ["Short", "Medium", "Detailed"]
)

if st.button("Generate Summary", type="primary"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        prompt = f"""
Summarize the following text.
Summary length: {summary_length}.
Use clear, simple language and preserve the key points.

Text:
{text}
"""

        try:
            with st.spinner("Generating your summary..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            summary = response.text

            if summary:
                st.subheader("Your Summary")
                st.write(summary)

                st.download_button(
                    "Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
            else:
                st.error("No summary was returned. Please try again.")

        except Exception as error:
            st.error("Summary generate nahi hui.")
            st.code(str(error))
