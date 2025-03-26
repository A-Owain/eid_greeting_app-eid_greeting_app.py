import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import os

# Constants
IMAGE_PATH = "eid-fitr.png"
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"  # Ensure this font file is in the repo root

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("Eid Greeting Generator")

name = st.text_input("Enter Your Name | ادخل اسمك", max_chars=30)
position = st.text_input("Position (Optional) | المسمى الوظيفي (اختياري)", max_chars=30)

if name:
    # Prepare Arabic text
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    # Load base image
    base_image = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(base_image)

    # Load fonts
    font_size_name = 70
    font_size_position = 40
    # font_size_name = 150
    # font_size_position = 100
    font = ImageFont.truetype(FONT_PATH, font_size_name)
    position_font = ImageFont.truetype(FONT_PATH, font_size_position)

    # Calculate name position
    image_width, _ = base_image.size
    name_bbox = font.getbbox(bidi_name)
    name_width = name_bbox[2] - name_bbox[0]
    x_name = (image_width - name_width) / 2
    y_name = 2200
    # y_name = 4300

    # Draw name without shadow
    draw.text((x_name, y_name), bidi_name, font=font, fill="#ea2f2f") # red

    # Draw position if provided
    if position.strip():
        reshaped_pos = arabic_reshaper.reshape(position)
        bidi_pos = get_display(reshaped_pos)
        pos_bbox = position_font.getbbox(bidi_pos)
        pos_width = pos_bbox[2] - pos_bbox[0]
        x_pos = (image_width - pos_width) / 2
        y_pos = y_name + 120
        draw.text((x_pos, y_pos), bidi_pos, font=position_font, fill="#EA2F2F")  # red

    # Convert to bytes
    img_bytes = io.BytesIO()
    base_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Show image and allow download
    st.image(img_bytes, caption="بطاقة معايدتك | Your Greeting Card", use_container_width=True)

    st.download_button(
        label="تنزيل | Download",
        data=img_bytes,
        file_name=f"eid_greeting_{name}.png",
        mime="image/png"
    )
