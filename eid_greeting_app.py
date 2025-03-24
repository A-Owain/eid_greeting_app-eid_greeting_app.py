import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("🎉 Eid Greeting Generator")

# Inputs
name = st.text_input("Enter Your Name | ادخل اسمك", max_chars=30)
position = st.text_input("Position (Optional) | المسمى الوظيفي (اختياري)", max_chars=30)

# Video Background
st.video("eid-greeting.mp4")

# Display Name and Position
if name:
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)
    st.markdown(f"""
        <h2 style='text-align: center; margin-top: 20px; color: white;'>
            {bidi_name}
        </h2>
    """, unsafe_allow_html=True)

    if position.strip():
        reshaped_pos = arabic_reshaper.reshape(position)
        bidi_pos = get_display(reshaped_pos)
        st.markdown(f"""
            <h4 style='text-align: center; color: #ccc;'>
                {bidi_pos}
            </h4>
        """, unsafe_allow_html=True)
