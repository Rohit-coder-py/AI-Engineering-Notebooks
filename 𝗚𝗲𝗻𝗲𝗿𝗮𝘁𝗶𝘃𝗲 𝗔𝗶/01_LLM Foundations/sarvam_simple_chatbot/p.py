
import os
import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape
from io import BytesIO

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Sarvam AI PDF Generator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Sarvam AI PDF Generator")
st.caption("Generate AI responses and download them as PDFs.")

# Initialize API client
api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    st.error("Please add SARVAM_API_KEY to your .env file.")
    st.stop()

client = SarvamAI(api_subscription_key=api_key)


# PDF generation function
def create_pdf(text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = [
        Paragraph("Sarvam AI Response", styles["Title"]),
        Spacer(1, 20),
        Paragraph(
            escape(text).replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]

    doc.build(content)
    buffer.seek(0)

    return buffer


# User input
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask Sarvam AI anything...",
    height=120
)

# Generate response
if st.button("✨ Generate Response", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a prompt.")

    else:
        try:
            with st.spinner("Sarvam AI is thinking..."):

                response = client.chat.completions(
                    model="sarvam-105b-conversations",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.session_state.answer = answer

        except Exception as error:
            st.error(f"API Error: {error}")


# Display response and download button
if "answer" in st.session_state:

    st.success("Response generated successfully!")

    st.subheader("AI Response")

    st.write(st.session_state.answer)

    pdf = create_pdf(st.session_state.answer)

    st.download_button(
        label="📄 Download PDF",
        data=pdf,
        file_name="sarvam_ai_response.pdf",
        mime="application/pdf",
        use_container_width=True
    )
