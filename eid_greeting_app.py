import streamlit as st
from jinja2 import Template
from html2image import Html2Image
import tempfile
import os
import io

TEMPLATE_PATH = "template.html"
hti = Html2Image()

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("🎉 Eid Greeting Generator")

name = st.text_input("👤 أدخل اسمك:", max_chars=30)

if name:
    # Load and fill HTML template
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())
    html_filled = template.render(name=name)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save filled HTML
        html_path = os.path.join(tmpdir, "greeting.html")
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_filled)

        # Render to PNG
        hti.screenshot(html_file=html_path, save_as="greeting.png", size=(800, 1000), output_path=tmpdir)
        img_path = os.path.join(tmpdir, "greeting.png")

        # Load image into memory
        with open(img_path, "rb") as img_file:
            png_bytes = img_file.read()

        # Preview and download
        st.image(png_bytes, caption="🎨 معايدتك", use_container_width=True)

        st.download_button(
            label="🖼️ تحميل PNG",
            data=png_bytes,
            file_name=f"eid_greeting_{name}.png",
            mime="image/png"
        )
