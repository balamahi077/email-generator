import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Email Drafting Assistant", layout="centered")
st.title("📧 Email Drafting Assistant")
st.markdown("Generate well-written emails with the help of Gemini AI.")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = ""
if "translated_email" not in st.session_state:
    st.session_state.translated_email = ""

# API key input
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

# Language options
language = st.selectbox("🌍 Choose Language for Output", ["English", "Hindi", "Telugu", "Spanish", "French", "German", "Japanese"])

# Proceed only if API key is provided
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    recipient = st.text_input("Recipient (e.g. John, Hiring Manager)")
    purpose = st.text_area("What’s the purpose of the email?")
    tone = st.selectbox("Tone of the email", ["Formal", "Friendly", "Persuasive", "Apologetic", "Thankful", "Neutral"])
    extra = st.text_area("Any additional information to include?")

    if st.button("Generate Email"):
        if not purpose:
            st.warning("Please provide the purpose of the email.")
        else:
            with st.spinner("Drafting your email..."):
                prompt = (
                    f"Write an email to {recipient or 'a recipient'}.\n"
                    f"Purpose: {purpose}\n"
                    f"Tone: {tone}\n"
                    f"Additional Info: {extra}\n"
                    f"Format it like a professional email with greeting and closing."
                )

                try:
                    response = model.generate_content(prompt)
                    st.session_state.email = response.text
                    st.success("Here's your draft:")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # Show generated email
    if st.session_state.email:
        st.text_area("Generated Email", st.session_state.email, height=300)

    # Translation logic
    if st.session_state.email and language != "English":
        if st.button("🌐 Translate Email"):
            translate_prompt = f"Translate the following email to {language}:\n\n{st.session_state.email}"
            try:
                with st.spinner(f"Translating to {language}..."):
                    translation = model.generate_content(translate_prompt)
                    st.session_state.translated_email = translation.text
            except Exception as e:
                st.error(f"Translation error: {e}")

    # Show translated email
    if st.session_state.translated_email:
        st.text_area(f"📜 Translated Email in {language}", st.session_state.translated_email, height=300)

# Footer
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #000;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    z-index: 999;
}
</style>
<div class="footer">
    © 2025  | Developed by Balakrishna.
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
