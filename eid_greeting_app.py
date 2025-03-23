import streamlit as st
from weasyprint import HTML
from jinja2 import Template
from pdf2image import convert_from_bytes
import io

TEMPLATE_PATH = "template.html"

st.set_page_config(page_title="Eid Greeting Generator", layout="centered")
st.title("🎉 Eid Greeting Generator")

name = st.text_input("👤 أدخل اسمك:", max_chars=30)

if name:
    # Fill HTML with user's name
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())
    html_filled = template.render(name=name)

    # Generate PDF in memory
    pdf_bytes = HTML(string=html_filled, base_url=".").write_pdf()

    # Convert PDF to PNG in memory
    images = convert_from_bytes(pdf_bytes, dpi=300)
    png_image = io.BytesIO()
    images[0].save(png_image, format="PNG")
    png_image.seek(0)

    # Preview image
    st.image(png_image, caption="🎨 معايدتك", use_container_width=True)

    st.success("🎁 جاهز للتحميل!")

    # Download buttons
    st.download_button(
        label="📄 تحميل PDF",
        data=pdf_bytes,
        file_name=f"eid_greeting_{name}.pdf",
        mime="application/pdf"
    )

    st.download_button(
        label="🖼️ تحميل PNG",
        data=png_image,
        file_name=f"eid_greeting_{name}.png",
        mime="image/png"
    )