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
    font_panel_title = ImageFont.truetype(font_path_bold, 20)
    font_panel_body = ImageFont.truetype(font_path_regular, 14)
    font_ticker = ImageFont.truetype(font_path_bold, 13)

    # Colors
    c_black = "#1A1A1A"
    c_red = "#8B0000"
    c_blue = "#1C3B57"
    c_gray = "#E6E2D6"
    c_dark_gray = "#4A4A4A"

    # --- MASTHEAD ---
    # Outer border / frame
    draw.rectangle([16, 16, 1008, 1008], outline=c_black, width=3)
    draw.rectangle([20, 20, 1004, 1004], outline=c_black, width=1)

    # Top banner background for masthead
    draw.rectangle([24, 24, 1000, 110], fill="#F3EFE6")
    
    # Masthead text
    title_text = "THE WORLD IN ONE PICTURE"
    bbox = font_masthead.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((1024 - tw) / 2, 32), title_text, fill=c_black, font=font_masthead)

    # Dateline
    date_text = "THURSDAY, 19 NOVEMBER 2026 · GLOBAL EDITION · SPECIAL NEWS SUMMARY"
    bbox_d = font_subhead.getbbox(date_text)
    dw = bbox_d[2] - bbox_d[0]
    draw.text(((1024 - dw) / 2, 82), date_text, fill=c_red, font=font_subhead)

    # Thin rules under masthead
    draw.line([36, 116, 988, 116], fill=c_black, width=2)
    draw.line([36, 120, 988, 120], fill=c_black, width=1)

    # --- LAYOUT: 2x2 GRID FOR 4 STORIES ---
    # Grid coordinates:
    # Panel 1 (Top-Left): US Politics (Jeffries / Peltola)
    # Panel 2 (Top-Right): GTA VI Global Rollout
    # Panel 3 (Bottom-Left): Cyclone Akvan
    # Panel 4 (Bottom-Right): Iran War & US Bases

    # Panel boxes:
    # X range: Left 36 to 494, Right 530 to 988
    # Y range: Top 132 to 552, Bottom 568 to 920

    def draw_panel(x1, y1, x2, y2, title, subtitle, illustration_func):
        # Panel background
        draw.rectangle([x1, y1, x2, y2], fill="#FFFFFF", outline=c_gray, width=2)
        # Category header bar
        draw.rectangle([x1, y1, x2, y1 + 32], fill=c_blue)
        draw.text((x1 + 12, y1 + 6), title, fill="#FFFFFF", font=font_panel_title)

        # Subtitle / summary text (word-wrapped manually or neatly fitted)
        # We draw subtitle lines below header
        text_y = y1 + 40
        for line in subtitle:
            draw.text((x1 + 12, text_y), line, fill=c_black, font=font_panel_body)
            text_y += 18

        # Illustration area bounding box
        ill_y1 = text_y + 8
        ill_y2 = y2 - 12
        ill_x1 = x1 + 12
        ill_x2 = x2 - 12
        
        # Draw illustration frame
        draw.rectangle([ill_x1, ill_y1, ill_x2, ill_y2], fill="#FAF8F5", outline=c_gray, width=1)
        
        # Call illustration function
        illustration_func(ill_x1, ill_y1, ill_x2, ill_y2)

    # --- ILLUSTRATION 1: US POLITICS (Capitol Dome & Gavel / Senate 56-44) ---
    def ill_politics(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Capitol Dome representation using polygon and arcs
        # Base building
        draw.rectangle([cx - 70, cy + 10, cx + 70, cy + 60], fill="#EAE6DF", outline=c_black, width=2)
        # Pillars
        for px in range(cx - 50, cx + 60, 20):
            draw.line([px, cy + 20, px, cy + 55], fill=c_black, width=2)
        # Dome base
        draw.chord([cx - 40, cy - 20, cx + 40, cy + 30], 180, 360, fill="#D9D2C5", outline=c_black, width=2)
        # Dome top lantern & spire
        draw.ellipse([cx - 10, cy - 35, cx + 10, cy - 15], fill="#D9D2C5", outline=c_black, width=2)
        draw.line([cx, cy - 35, cx, cy - 50], fill=c_black, width=2)
        
        # Label badge for Hakeem Jeffries & Senate 56-44
        draw.rectangle([cx - 90, y1 + 8, cx + 90, y1 + 32], fill=c_red)
        draw.text((cx - 82, y1 + 10), "HAKEEM JEFFRIES · 56-44", fill="#FFFFFF", font=font_panel_body)

    # --- ILLUSTRATION 2: GTA VI GLOBAL ROLLOUT ---
    def ill_gta(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Neon city skyline / palm trees
        # Background gradient bars (sunset)
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#1C1C2E")
        
        # Neon sun semicircle
        draw.ellipse([cx - 60, cy - 50, cx + 60, cy + 70], fill="#FF7043")
        
        # Buildings silhouette
        draw.rectangle([x1 + 15, cy + 10, x1 + 55, y2 - 10], fill="#0F0F1A")
        draw.rectangle([x1 + 60, cy - 20, x1 + 100, y2 - 10], fill="#0F0F1A")
        draw.rectangle([x2 - 70, cy - 10, x2 - 20, y2 - 10], fill="#0F0F1A")

        # Palm tree trunk & leaves (simplified geometric)
        px_tree = x1 + 115
        draw.line([px_tree, y2 - 10, px_tree, cy + 15], fill="#0F0F1A", width=4)
        for angle_offset in [-30, -15, 0, 15, 30]:
            draw.line([px_tree, cy + 15, px_tree + angle_offset * 1.2, cy - 5 + abs(angle_offset) * 0.3], fill="#0F0F1A", width=3)

        # Big bold VI sign
        draw.rectangle([cx - 55, y1 + 12, cx + 55, y1 + 42], fill="#FFD700", outline=c_black, width=2)
        draw.text((cx - 45, y1 + 15), "GTA VI LIVE", fill="#000000", font=font_panel_title)

    # --- ILLUSTRATION 3: CYCLONE AKVAN ---
    def ill_cyclone(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Coastline (India / AP & Odisha)
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#E8EEF5")
        
        # Landmass (right side)
        draw.polygon([(cx + 20, y1 + 4), (x2 - 4, y1 + 4), (x2 - 4, y2 - 4), (cx - 20, y2 - 4)], fill="#D8E2D0")
        draw.text((cx + 30, y2 - 30), "INDIA (AP / ODISHA)", fill=c_dark_gray, font=font_subhead)

        # Cyclone spiral arcs (red/orange warning)
        for r in [50, 35, 20]:
            draw.arc([cx - r - 30, cy - r, cx + r - 30, cy + r], start=0, end=270, fill=c_red, width=4)
        
        # Eye of cyclone
        draw.ellipse([cx - 45, cy - 8, cx - 35, cy + 2], fill=c_black)

        # Alert banner
        draw.rectangle([x1 + 8, y1 + 8, x1 + 160, y1 + 32], fill=c_red)
        draw.text((x1 + 14, y1 + 10), "HIGH ALERT: AKVAN", fill="#FFFFFF", font=font_panel_body)

    # --- ILLUSTRATION 4: IRAN WAR & US BASES ---
    def ill_iran(x1, y1, x2, y2):
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Persian Gulf / Bases map concept
        draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill="#F0F4F8")
        
        # Radar dish / base icon (Left)
        bx = x1 + 50
        by = cy + 20
        draw.rectangle([bx - 15, by, bx + 15, by + 25], fill="#7F8C8D", outline=c_black, width=2)
        draw.arc([bx - 25, by - 25, bx + 25, by + 5], start=0, end=180, fill=c_black, width=3)
        draw.text((bx - 40, by + 30), "KUWAIT/BAHRAIN", fill=c_black, font=ImageFont.truetype(font_path_regular, 11))

        # Missile arc in middle
        draw.arc([bx, cy - 30, x2 - 40, cy + 30], start=190, end=350, fill=c_red, width=3)
        # Missile head arrowhead
        draw.polygon([(cx, cy - 12), (cx + 10, cy - 8), (cx + 4, cy - 18)], fill=c_red)

        # Qeshm Island / Iran target (Right)
        qx = x2 - 50
        qy = cy - 10
        draw.ellipse([qx - 20, qy - 15, qx + 20, qy + 15], fill="#D35400", outline=c_black, width=2)
        draw.text((qx - 35, qy + 20), "QESHM ISLAND", fill=c_black, font=ImageFont.truetype(font_path_regular, 11))

        # Warning banner
        draw.rectangle([x1 + 8, y1 + 8, x1 + 155, y1 + 32], fill=c_red)
        draw.text((x1 + 14, y1 + 10), "US & IRAN EXCHANGE", fill="#FFFFFF", font=font_panel_body)

    # Draw the 4 panels
    # Panel 1: US Politics
    draw_panel(36, 132, 494, 552, 
               "1. US POLITICS: JEFFRIES & SENATE",
               [
                   "Democrats nominate Hakeem Jeffries for House Speaker,",
                   "set to be the first African-American Speaker.",
                   "Mary Peltola wins in Alaska, giving Dems a 56–44 Senate majority."
               ], 
               ill_politics)

    # Panel 2: GTA VI
    draw_panel(530, 132, 988, 552,
               "2. GAMING: GTA VI GLOBAL ROLLOUT",
               [
                   "Grand Theft Auto VI begins its global rollout after",
                   "a historic 13-year wait.",
                   "Millions of eager gamers officially enter Vice City today."
               ],
               ill_gta)

    # Panel 3: Cyclone Akvan
    draw_panel(36, 568, 494, 920,
               "3. WEATHER: CYCLONE AKVAN",
               [
                   "Cyclone Akvan crosses the coast between Machilipatnam",
                   "and Puri (Andhra Pradesh and Odisha, India) on Nov 19.",
                   "Both states remain on extremely high alert."
               ],
               ill_cyclone)

    # Panel 4: Iran War
    draw_panel(530, 568, 988, 920,
               "4. CONFLICT: US & IRAN EXCHANGE FIRE",
               [
                   "Iran widens attacks, hitting a US base in Kuwait",
                   "and striking Bahrain again after previous US strikes",
                   "on missile launch sites at Qeshm Island."
               ],
               ill_iran)

    # --- BOTTOM TICKER STRIP ---
    # Ticker background box
    draw.rectangle([36, 932, 988, 992], fill=c_blue)
    draw.rectangle([40, 936, 984, 988], outline="#FFFFFF", width=1)

    # Ticker headline text (Also news items)
    ticker_text = "ALSO TODAY: · Nvidia CEO Jensen Huang resigns; Colette Kress is acting CEO · EU proposes €45B Ukraine loan · Trump, Xi & Putin to hold Shenzhen talks · Voyager 1 reaches 1 light-day · Islam set to be largest religion by 2035"
    
    # Draw ticker text centered or scrolling-style fit
    # Let's check width and fit nicely
    bbox_t = font_ticker.getbbox(ticker_text)
    tw_t = bbox_t[2] - bbox_t[0]
    # If too wide, we can place it with padding
    draw.text((50, 952), ticker_text, fill="#FFFFFF", font=font_ticker)

    # Save output
    img.save(output_path, "PNG")
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_entry_image()
