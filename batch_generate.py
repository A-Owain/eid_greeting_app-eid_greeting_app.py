
import csv
import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Constants
IMAGE_PATH = "eid-fitr.jpg"
FONT_PATH = "NotoSansArabic-SemiBold.ttf"
OUTPUT_DIR = "output"
CSV_FILE = "employees.csv"

# Font sizes
FONT_SIZE_NAME = 150
FONT_SIZE_POSITION = 100

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load fonts
font_name = ImageFont.truetype(FONT_PATH, FONT_SIZE_NAME)
font_position = ImageFont.truetype(FONT_PATH, FONT_SIZE_POSITION)

# Read CSV
with open(CSV_FILE, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get("name", "").strip()
        position = row.get("position", "").strip()

        if not name:
            continue

        # Reshape text
        reshaped_name = arabic_reshaper.reshape(name)
        bidi_name = get_display(reshaped_name)

        reshaped_position = arabic_reshaper.reshape(position) if position else ""
        bidi_position = get_display(reshaped_position) if position else ""

        # Load image
        base_image = Image.open(IMAGE_PATH).convert("RGB")
        draw = ImageDraw.Draw(base_image)

        # Calculate text positions
        image_width, _ = base_image.size

        name_bbox = font_name.getbbox(bidi_name)
        name_width = name_bbox[2] - name_bbox[0]
        x_name = (image_width - name_width) / 2
        y_name = 4300
        draw.text((x_name, y_name), bidi_name, font=font_name, fill="#EA2F2F")

        if bidi_position:
            pos_bbox = font_position.getbbox(bidi_position)
            pos_width = pos_bbox[2] - pos_bbox[0]
            x_pos = (image_width - pos_width) / 2
            y_pos = y_name + 300
            draw.text((x_pos, y_pos), bidi_position, font=font_position, fill="#EA2F2F")

        # Save image
        safe_name = name.replace(" ", "_").replace("/", "_")
        out_path = os.path.join(OUTPUT_DIR, f"eid_greeting_{safe_name}.png")
        base_image.save(out_path, format="PNG")
        print(f"Saved: {out_path}")
