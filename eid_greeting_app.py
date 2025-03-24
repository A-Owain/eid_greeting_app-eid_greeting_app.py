import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# Constants
IMAGE_PATH = "eid-fitr.jpg"
FONT_PATH = "NotoSansArabic-SemiBold.ttf"

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("TRAY Eid Greeting Generator")

# Input fields
name = st.text_input("Enter Your Name | ادخل اسمك", max_chars=30)
position = st.text_input("Position (Optional) | المسمى الوظيفي (اختياري)", max_chars=30)

if name:
    # Reshape and format text for Arabic
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    # Load image
    base_image = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(base_image)

    # Load fonts
    font_name = ImageFont.truetype(FONT_PATH, 150)
    font_position = ImageFont.truetype(FONT_PATH, 80)

    # Calculate name position
    image_width, _ = base_image.size
    name_width = font_name.getbbox(bidi_name)[2]
    x_name = (image_width - name_width) / 2
    y_name = 4450

    # Draw name
    shadow_offset = 2
    draw.text((x_name + shadow_offset, y_name + shadow_offset), bidi_name, font=font_name, fill="black")
    draw.text((x_name, y_name), bidi_name, font=font_name, fill="white")

    # Draw position if given
    if position.strip():
        reshaped_position = arabic_reshaper.reshape(position)
        bidi_position = get_display(reshaped_position)
        pos_width = font_position.getbbox(bidi_position)[2]
        x_pos = (image_width - pos_width) / 2
        y_pos = y_name + 250
        draw.text((x_pos + shadow_offset, y_pos + shadow_offset), bidi_position, font=font_position, fill="black")
        draw.text((x_pos, y_pos), bidi_position, font=font_position, fill="white")

    # Convert image to bytes
    img_bytes = io.BytesIO()
    base_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Show and download
    st.image(img_bytes, caption="بطاقة معايدتك | Your Greeting Card", use_container_width=True)

    st.download_button(
        label="تنزيل | Download",
        data=img_bytes,
        file_name=f"eid_greeting_{name}.png",
        mime="image/png"
    )
