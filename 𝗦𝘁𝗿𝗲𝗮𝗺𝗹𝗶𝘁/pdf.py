
import streamlit as st
from fpdf import FPDF

name = st.text_input("Enter your name:")

mess = f"""Hello {name}! Every person in this world has a unique identity, a different personality, and a journey that makes their life
meaningful.
No matter where someone comes from, what their background is, what challenges they have faced, or what dreams they carry in their heart,
every individual has the potential to learn, grow, improve, and achieve something meaningful in life.
Some people are naturally confident, while others take time to discover their strengths.
Some are good at communicating, while others express themselves through their actions, creativity, or hard work.
Everyone makes mistakes, experiences difficult situations, faces moments of uncertainty,
and sometimes struggles to find the right direction, but these experiences are an important part of becoming a better person.
Life is not always easy, and success does not come to everyone at the same time. Some people achieve their goals early,
while others need more time, patience, and determination. What truly matters is the willingness to keep moving forward, learn from past experiences,
respect others, and never stop believing in the possibility of a better future. A person's value should never be measured only by their appearance,
financial situation, educational qualifications, professional achievements, or social status, because kindness, honesty, responsibility,
understanding, and the ability to help others are equally important qualities. Every day brings new opportunities to discover something interesting,
develop new skills, build meaningful relationships, and become more knowledgeable than yesterday. Sometimes a small decision can create a big
difference, a simple conversation can change someone's perspective, and a little encouragement can give another person the confidence to continue
working towards their dreams.
It is important to remember that nobody is perfect, and comparing our journey with someone else's journey often creates unnecessary
pressure and disappointment.
Instead, we should focus on our own progress, appreciate the people who support us,
remain grateful for the opportunities we have, and treat everyone with respect. Whether someone is a student, teacher, developer, entrepreneur,
artist, employee, or simply a person trying to understand life, everyone deserves the opportunity to grow and create a positive impact.
Ultimately, a meaningful life is not just about reaching the destination but also
about enjoying the journey, learning valuable lessons, overcoming obstacles, helping others, and becoming someone we can genuinely be proud of."""

bu = st.button("Generate")

if bu:
    st.write(mess)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, mess)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    st.download_button(
        label="Download as PDF",
        data=pdf_bytes,
        file_name="response.pdf",
        mime="application/pdf"
    )
