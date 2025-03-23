import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import os

# Constants
IMAGE_PATH = "eid-fitr.jpg"
FONT_PATH = "NotoSansArabic-SemiBold.ttf"  # Ensure this font file is in the repo root

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("🎉 Eid Greeting Generator")

name = st.text_input("👤 أدخل اسمك:", max_chars=30)

if name:
    # Prepare Arabic text
    reshaped_text = arabic_reshaper.reshape(name)
    bidi_text = get_display(reshaped_text)

    # Load base image
    base_image = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(base_image)

    # Load font with specified size
    font_size = 150
    font = ImageFont.truetype(FONT_PATH, font_size)

    # Calculate text position
    image_width, _ = base_image.size
    text_bbox = font.getbbox(bidi_text)
    text_width = text_bbox[2] - text_bbox[0]
    x = (image_width - text_width) / 2
    y = 4050  # Precise vertical position you specified

    # Draw shadow (optional)
    shadow_offset = 2
    draw.text((x + shadow_offset, y + shadow_offset), bidi_text, font=font, fill="black")

    # Draw main text
    draw.text((x, y), bidi_text, font=font, fill="white")

    # Convert to bytes
    img_bytes = io.BytesIO()
    base_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Show image and allow download
    st.image(img_bytes, caption="🎨 معايدتك", use_container_width=True)
    st.download_button(
        label="🖼️ تحميل الصورة",
        data=img_bytes,
        file_name=f"eid_greeting_{name}.png",
        mime="image/png"
    )