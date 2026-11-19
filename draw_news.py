import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

def create_entry_image(output_path="entry.png"):
    # 1024x1024 canvas, warm off-white newspaper background
    img = Image.new("RGB", (1024, 1024), color="#FBF9F1")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_path_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font_masthead = ImageFont.truetype(font_path_bold, 42)
    font_subhead = ImageFont.truetype(font_path_regular, 16)
    font_panel_title = ImageFont.truetype(font_path_bold, 18)
    font_panel_body = ImageFont.truetype(font_path_regular, 13)
    font_ticker = ImageFont.truetype(font_path_bold, 12)

    # Colors
    c_black = "#1A1A1A"
    c_red = "#8B0000"
    c_blue = "#1C3B57"
    c_gray = "#E6E2D6"
    c_dark_gray = "#4A4A4A"

    def assert_fits(text, font, box_x1, box_x2, label_desc):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        box_w = box_x2 - box_x1
        # Require text to fit inside box with at least 8px padding on both sides
        assert text_w + 16 <= box_w, f"FAIL: {label_desc} text '{text}' width {text_w} exceeds box width {box_w} (with 8px padding)"

    # --- MASTHEAD ---
    draw.rectangle([16, 16, 1008, 1008], outline=c_black, width=3)
    draw.rectangle([20, 20, 1004, 1004], outline=c_black, width=1)
    draw.rectangle([24, 24, 1000, 110], fill="#F3EFE6")
    
    title_text = "THE WORLD IN ONE PICTURE"
    bbox = font_masthead.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((1024 - tw) / 2, 32), title_text, fill=c_black, font=font_masthead)

    date_text = "THURSDAY, 19 NOVEMBER 2026 · GLOBAL EDITION · SPECIAL NEWS SUMMARY"
    bbox_d = font_subhead.getbbox(date_text)
    dw = bbox_d[2] - bbox_d[0]
    draw.text(((1024 - dw) / 2, 82), date_text, fill=c_red, font=font_subhead)

    draw.line([36, 116, 988, 116], fill=c_black, width=2)
    draw.line([36, 120, 988, 120], fill=c_black, width=1)

    def draw_panel(x1, y1, x2, y2, title, subtitle, illustration_func):
        # Assert panel title fits
        assert_fits(title, font_panel_title, x1, x2, f"Panel title '{title}'")
        
        draw.rectangle([x1, y1, x2, y2], fill="#FFFFFF", outline=c_gray, width=2)
        draw.rectangle([x1, y1, x2, y1 + 32], fill=c_blue)
        draw.text((x1 + 12, y1 + 6), title, fill="#FFFFFF", font=font_panel_title)

        text_y = y1 + 40
        for line in subtitle:
            draw.text((x1 + 12, text_y), line, fill=c_black, font=font_panel_body)
            text_y += 18

        ill_y1 = text_y + 8
        ill_y2 = y2 - 12
        ill_x1 = x1 + 12
        ill_x2 = x2 - 12
        
        draw.rectangle([ill_x1, ill_y1, ill_x2, ill_y2], fill="#FAF8F5", outline=c_gray, width=1)
        illustration_func(ill_x1, ill_y1, ill_x2, ill_y2)

    # --- ILLUSTRATION 1: US POLITICS ---
    def ill_politics(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        
        # Enlarge Capitol building slightly
        draw.rectangle([cx - 80, cy + 5, cx + 80, cy + 60], fill="#EAE6DF", outline=c_black, width=2)
        for px in range(cx - 60, cx + 70, 20):
            draw.line([px, cy + 15, px, cy + 55], fill=c_black, width=2)
        draw.chord([cx - 45, cy - 25, cx + 45, cy + 30], 180, 360, fill="#D9D2C5", outline=c_black, width=2)
        draw.ellipse([cx - 10, cy - 40, cx + 10, cy - 15], fill="#D9D2C5", outline=c_black, width=2)
        draw.line([cx, cy - 40, cx, cy - 55], fill=c_black, width=2)
        
        # Label badge for Hakeem Jeffries & Senate 56-44
        label_text = "JEFFRIES · SENATE 56-44"
        # Check fits in illustration box
        assert_fits(label_text, font_panel_body, x1, x2, "Panel 1 label")
        
        badge_w = 210
        draw.rectangle([cx - badge_w//2, y1 + 8, cx + badge_w//2, y1 + 32], fill=c_red)
        draw.text((cx - badge_w//2 + 10, y1 + 10), label_text, fill="#FFFFFF", font=font_panel_body)

    # --- ILLUSTRATION 2: GTA VI GLOBAL ROLLOUT ---
    def ill_gta(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#1C1C2E")
        draw.ellipse([cx - 60, cy - 50, cx + 60, cy + 70], fill="#FF7043")
        draw.rectangle([x1 + 15, cy + 10, x1 + 55, y2 - 10], fill="#0F0F1A")
        draw.rectangle([x1 + 60, cy - 20, x1 + 100, y2 - 10], fill="#0F0F1A")
        draw.rectangle([x2 - 70, cy - 10, x2 - 20, y2 - 10], fill="#0F0F1A")

        px_tree = x1 + 115
        draw.line([px_tree, y2 - 10, px_tree, cy + 15], fill="#0F0F1A", width=4)
        for angle_offset in [-30, -15, 0, 15, 30]:
            draw.line([px_tree, cy + 15, px_tree + angle_offset * 1.2, cy - 5 + abs(angle_offset) * 0.3], fill="#0F0F1A", width=3)

        label_text = "GTA VI LIVE"
        assert_fits(label_text, font_panel_title, x1, x2, "Panel 2 label")
        
        draw.rectangle([cx - 75, y1 + 12, cx + 75, y1 + 42], fill="#FFD700", outline=c_black, width=2)
        draw.text((cx - 58, y1 + 15), label_text, fill="#000000", font=font_panel_title)
    # --- ILLUSTRATION 3: CYCLONE AKVAN ---
    def ill_cyclone(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#E8EEF5")
        draw.polygon([(cx + 20, y1 + 4), (x2 - 4, y1 + 4), (x2 - 4, y2 - 4), (cx - 20, y2 - 4)], fill="#D8E2D0")
        draw.text((cx + 25, y2 - 30), "INDIA (AP / ODISHA)", fill=c_dark_gray, font=font_subhead)

        for r in [50, 35, 20]:
            draw.arc([cx - r - 30, cy - r, cx + r - 30, cy + r], start=0, end=270, fill=c_red, width=4)
        draw.ellipse([cx - 45, cy - 8, cx - 35, cy + 2], fill=c_black)

        label_text = "HIGH ALERT: AKVAN"
        assert_fits(label_text, font_panel_body, x1, x2, "Panel 3 label")
        
        draw.rectangle([x1 + 8, y1 + 8, x1 + 175, y1 + 32], fill=c_red)
        draw.text((x1 + 14, y1 + 10), label_text, fill="#FFFFFF", font=font_panel_body)

    # --- ILLUSTRATION 4: IRAN WAR & US BASES ---
    def ill_iran(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#F0F4F8")
        
        bx = x1 + 50
        by = cy + 20
        draw.rectangle([bx - 15, by, bx + 15, by + 25], fill="#7F8C8D", outline=c_black, width=2)
        draw.arc([bx - 25, by - 25, bx + 25, by + 5], start=0, end=180, fill=c_black, width=3)
        draw.text((bx - 45, by + 30), "KUWAIT/BAHRAIN", fill=c_black, font=ImageFont.truetype(font_path_regular, 10))

        draw.arc([bx, cy - 30, x2 - 40, cy + 30], start=190, end=350, fill=c_red, width=3)
        draw.polygon([(cx, cy - 12), (cx + 10, cy - 8), (cx + 4, cy - 18)], fill=c_red)

        qx = x2 - 50
        qy = cy - 10
        draw.ellipse([qx - 20, qy - 15, qx + 20, qy + 15], fill="#D35400", outline=c_black, width=2)
        draw.text((qx - 40, qy + 20), "QESHM ISLAND", fill=c_black, font=ImageFont.truetype(font_path_regular, 10))

        label_text = "US & IRAN EXCHANGE"
        assert_fits(label_text, font_panel_body, x1, x2, "Panel 4 label")
        
        draw.rectangle([x1 + 8, y1 + 8, x1 + 185, y1 + 32], fill=c_red)
        draw.text((x1 + 14, y1 + 10), label_text, fill="#FFFFFF", font=font_panel_body)

    # Draw the 4 panels with shortened / verified titles
    draw_panel(36, 132, 494, 552, 
               "1. US POLITICS: JEFFRIES & SENATE",
               [
                   "Democrats nominate Hakeem Jeffries for House Speaker,",
                   "set to be the first African-American Speaker.",
                   "Mary Peltola wins in Alaska, giving Dems a 56–44 Senate majority."
               ], 
               ill_politics)

    draw_panel(530, 132, 988, 552,
               "2. GAMING: GTA VI GLOBAL ROLLOUT",
               [
                   "Grand Theft Auto VI begins its global rollout after",
                   "a historic 13-year wait.",
                   "Millions of eager gamers officially enter Vice City today."
               ],
               ill_gta)

    draw_panel(36, 568, 494, 920,
               "3. WEATHER: CYCLONE AKVAN",
               [
                   "Cyclone Akvan crosses the coast between Machilipatnam",
                   "and Puri (Andhra Pradesh and Odisha, India) on Nov 19.",
                   "Both states remain on extremely high alert."
               ],
               ill_cyclone)

    draw_panel(530, 568, 988, 920,
               "4. CONFLICT: US-IRAN CLASH",
               [
                   "Iran widens attacks, hitting a US base in Kuwait",
                   "and striking Bahrain again after previous US strikes",
                   "on missile launch sites at Qeshm Island."
               ],
               ill_iran)

    # --- BOTTOM TICKER STRIP ---
    draw.rectangle([36, 932, 988, 992], fill=c_blue)
    draw.rectangle([40, 936, 984, 988], outline="#FFFFFF", width=1)

    # Shortened ticker items so entire line fits with padding
    ticker_text = "ALSO: Nvidia/Kress · EU €45B loan · Trump, Xi & Putin · Voyager 1 · Islam #1 by 2035"
    assert_fits(ticker_text, font_ticker, 40, 984, "Bottom ticker")

    draw.text((50, 952), ticker_text, fill="#FFFFFF", font=font_ticker)

    img.save(output_path, "PNG")
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_entry_image()
