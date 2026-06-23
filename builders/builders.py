from unittest import case

import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
from fpdf import FPDF
import os
import re

from configs import NametagConfigs, CertificateConfigs, PlacardConfigs

class Nametags:
    def __init__(self, configs: NametagConfigs):
        self.configs = configs

    def _draw_text_autofit(self, draw: ImageDraw.Draw, text: str, max_width: float, default_font_size: int, y_position: float, font_path: str, color: str = "#133521", position: str = "sub"):
        """
        Draws centered text. Shrinks font size until it fits within max_width.
        If it hits the minimum font size and still doesn't fit, wraps to the next line.
        """
        font_size = default_font_size
        font = ImageFont.truetype(font_path, font_size)
        
        # Calculate minimum font size cleanly
        min_font_size = int(16 * self.configs.pt_to_px)
        
        # 1. Loop to reduce font size until it fits the allowed width
        while font_size > min_font_size:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                break
                
            font_size -= 2 # Shrink and try again
            font = ImageFont.truetype(font_path, font_size)

        # 2. Re-calculate bounding box after the loop finishes
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Exact horizontal center of the tag
        center_x = self.configs.tag_size_px / 2

        # 3. If it STILL doesn't fit, apply the multi-line wrap
        if text_width > max_width:
            # Estimate character width to find safe line breaks
            char_bbox = draw.textbbox((0, 0), "M", font=font)
            avg_char_width = char_bbox[2] - char_bbox[0]
            
            max_chars_per_line = max(1, int(max_width / avg_char_width)) + 5
            wrapped_lines = textwrap.wrap(text, width=max_chars_per_line)
            
            line_height = char_bbox[3] - char_bbox[1]
            line_spacing = 8  # Tight line spacing in pixels
            
            y_position = 4.0 * self.configs.ppcm if position == "main" else y_position

            current_y = y_position
            for line in wrapped_lines:
                draw.text((center_x, current_y), line, fill=color, font=font, anchor="mt")
                current_y += line_height + line_spacing
                
            total_height = current_y - y_position
            return total_height
            
        # 4. If it fits perfectly on one line, draw normally
        else:
            text_height = bbox[3] - bbox[1]
            draw.text((center_x, y_position), text, fill=color, font=font, anchor="mt")
            return text_height

    def generate_individual_tags(self, output_dir: str = None):
        # Load data
        df = pd.read_csv(self.configs.csv_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        for index, row in df.iterrows():
            role = str(row['Role']).upper()
            name = str(row['Name']) if pd.notna(row['Name']) else ""
            committee = str(row['Committee'])
            country = str(row['Country/Affiliation']) if pd.notna(row['Country/Affiliation']) else ""
            photo = str(row['Photo'])
            day1 = str(row['Bento1']) if pd.notna(row['Bento1']) else None
            day2 = str(row['Bento2']) if pd.notna(row['Bento2']) else None
            wifi_id = str(row['WifiID']) if 'WifiID' in row and pd.notna(row['WifiID']) else ""
            wifi_pass = str(row['WifiPass']) if 'WifiPass' in row and pd.notna(row['WifiPass']) else ""

            type = None
            if role == "DELEGATE" or role == "CHAIR" or role == "CO-CHAIR":
                type = "committee"
            elif role == "STAFF" or role == "VOLUNTEER":
                type = "organizer"
            elif role == "SUPPORTER":
                type = "vip"
            elif role == "OBSERVER":
                type = "observer"

            lang = None
            if committee in ["WHO", "ECOSOC", "UNSC"]:
                lang = "eng"
            elif committee in ["UNEP", "UNHRC"]:
                lang = "jp"
            else:
                lang = "eng"

            photo_perm = None # Placeholder for future photo integration
            if photo == "Yes":
                photo_perm = ""
            elif photo == "No":
                photo_perm = "_alt"
            
            front_template_path = getattr(self.configs, f"{type}_nametag_template{photo_perm}", None)
            back_template_path = getattr(self.configs, f"{lang}_back_nametag_template", None)
            
            try:
                front_img = Image.open(front_template_path).convert("RGBA")
                back_img = Image.open(back_template_path).convert("RGBA")
            except FileNotFoundError:
                print(f"Template missing for type: {type}. Skipping {name}.")
                continue

            # Initializing drawer
                
            front_draw = ImageDraw.Draw(front_img)
            back_draw = ImageDraw.Draw(back_img)

            # Drawing the main text

            if role == "DELEGATE":
                font_choice_path = self.configs.country_font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(country)) else self.configs.name_font_path
                self._draw_text_autofit(front_draw, 
                                        country.upper(), 
                                        self.configs.max_text_width, 
                                        default_font_size=self.configs.main_text_default_font_size, 
                                        y_position=self.configs.main_text_y_position, 
                                        font_path=font_choice_path,
                                        color="#ffffff" if photo == "No" else "#133521",
                                        position="main")
            else:
                font_choice_path = self.configs.name_font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(name)) else self.configs.name_font_path
                self._draw_text_autofit(front_draw, 
                                        name, 
                                        self.configs.max_text_width, 
                                        default_font_size=self.configs.main_text_default_font_size, 
                                        y_position=self.configs.main_text_y_position, 
                                        font_path=font_choice_path,
                                        color="#ffffff" if photo == "No" else "#133521",
                                        position="main")

            # Drawing the role

            self._draw_text_autofit(front_draw, 
                                    role, 
                                    self.configs.max_text_width, 
                                    default_font_size=self.configs.role_default_font_size, 
                                    y_position=self.configs.role_y_position, 
                                    font_path=self.configs.role_font_path, 
                                    color="#ffffff")

            # Drawing the subtext
            if role == "DELEGATE":
                font_choice_path = self.configs.name_font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(name)) else self.configs.country_font_path
                self._draw_text_autofit(front_draw, 
                                        name, 
                                        self.configs.max_text_width, 
                                        default_font_size=self.configs.sub_text_default_font_size, 
                                        y_position=self.configs.sub_text_y_position, 
                                        font_path=font_choice_path,
                                        color="#ffffff" if photo == "No" else "#133521",
                                        position="sub")
            if role == "SUPPORTER" or role == "OBSERVER":
                font_choice_path = self.configs.country_font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(country)) else self.configs.country_font_path
                self._draw_text_autofit(front_draw, 
                                        country, 
                                        self.configs.max_text_width, 
                                        default_font_size=self.configs.sub_text_default_font_size, 
                                        y_position=self.configs.sub_text_y_position, 
                                        font_path=font_choice_path,
                                        color="#ffffff" if photo == "No" else "#133521")

            # Drawing the committee
            if role == "DELEGATE" or role == "CHAIR" or role == "CO-CHAIR":
                self._draw_text_autofit(front_draw, 
                                        committee, 
                                        self.configs.max_text_width, 
                                        default_font_size=self.configs.committee_default_font_size, 
                                        y_position=self.configs.committee_y_position, 
                                        font_path=self.configs.committee_font_path,
                                        color="#ffffff" if photo == "No" else "#133521")

            # Drawing the wifi info
            wifi_font = ImageFont.truetype(self.configs.wifi_font_path, self.configs.wifi_default_font_size)
            back_draw.text((self.configs.wifi_x_position, self.configs.wifiid_y_position), wifi_id, fill="#133521", font=wifi_font)
            back_draw.text((self.configs.wifi_x_position, self.configs.wifipass_y_position), wifi_pass, fill="#133521", font=wifi_font)
            
            if day1 is not None:
                bento1 = Image.open(getattr(self.configs, day1)).resize(self.configs.bento_size)
                back_img.paste(bento1, (self.configs.day1_bento_x_position, self.configs.day1_bento_y_position), bento1)
                
            if day2 is not None:
                bento2 = Image.open(getattr(self.configs, day2)).resize(self.configs.bento_size)
                # The third argument acts as the transparency mask!
                back_img.paste(bento2, (self.configs.day2_bento_x_position, self.configs.day2_bento_y_position), bento2)

            # 4. Save individual files
            front_img.save(os.path.join(output_dir, f"{index:03}_front.png"))
            back_img.save(os.path.join(output_dir, f"{index:03}_back.png"))
            print(f"Generated tags for {name}")

    def generate_pdf(self, input_dir: str = None, output_dir: str = None, dpi: int = 300):
        # A4 dimensions in points
        PAGE_WIDTH = 595.28
        PAGE_HEIGHT = 841.89
        
        pdf = FPDF(unit="pt", format="A4")
        
        # --- CONVERT PIXELS TO POINTS ---
        # Formula: Points = (Pixels * 72) / DPI
        tag_size_px = self.configs.tag_size_px
        tag_size_pt = (tag_size_px * 72) / dpi
        
        # Define your layout parameters
        columns = 2
        rows_per_page = 3
        items_per_page = columns * rows_per_page  # 6 items total
        
        # Calculate margins to center the entire 2x3 grid on the A4 page
        # Note: We are using tag_size_pt here so the math aligns with A4's point dimensions!
        grid_width = columns * tag_size_pt
        grid_height = rows_per_page * tag_size_pt
        
        # Safety Check: Warn if the image is too large for the page at this DPI
        if grid_width > PAGE_WIDTH or grid_height > PAGE_HEIGHT:
            print(f"Warning: At {dpi} DPI, your {tag_size_px}px tags create a grid that is too large for an A4 page. Consider raising the DPI or lowering the px size.")

        margin_x = (PAGE_WIDTH - grid_width) / 2
        margin_y = (PAGE_HEIGHT - grid_height) / 2

        # Total number of pairs (assumes files are named 000_front.png, 001_front.png, etc.)
        num_pairs = len([f for f in os.listdir(input_dir) if f.endswith('_front.png')])
        
        # Iterate by index
        for i in range(num_pairs):
            front_path = os.path.join(input_dir, f"{i:03}_front.png")
            back_path = os.path.join(input_dir, f"{i:03}_back.png")
            
            # --- Handle Front Image ---
            item_index_front = (i * 2) % items_per_page
            if item_index_front == 0:
                pdf.add_page()
                
            row_f = item_index_front // columns
            col_f = item_index_front % columns
            x_f = margin_x + (col_f * tag_size_pt)
            y_f = margin_y + (row_f * tag_size_pt)
            
            pdf.image(front_path, x_f, y_f, tag_size_pt, tag_size_pt)
            
            # --- Handle Back Image ---
            item_index_back = (i * 2 + 1) % items_per_page
            if item_index_back == 0:
                pdf.add_page()
                
            row_b = item_index_back // columns
            col_b = item_index_back % columns
            x_b = margin_x + (col_b * tag_size_pt)
            y_b = margin_y + (row_b * tag_size_pt)
            
            pdf.image(back_path, x_b, y_b, tag_size_pt, tag_size_pt)
        
        pdf.output(os.path.join(output_dir, "print_nametags.pdf"))


class Placards:
    def __init__(self, configs: PlacardConfigs):
        self.configs = configs

    def _draw_text_autofit(self, draw: ImageDraw.Draw, 
                           text: str, 
                           max_width: float, 
                           default_font_size: int, 
                           y_position: float, 
                           font_path: str, 
                           color: str = "#133521", 
                           position: str = "sub"):
        """
        Draws centered text. Shrinks font size until it fits within max_width.
        If it hits the minimum font size and still doesn't fit, wraps to the next line.
        """
        font_size = default_font_size
        font = ImageFont.truetype(font_path, font_size)
        
        if position == "main":
            min_font_size = int(53 * self.configs.pt_to_px)
        elif position == "sub":
            min_font_size = int(18 * self.configs.pt_to_px)
        elif position == "committee":
            min_font_size = int(10 * self.configs.pt_to_px)

        
        # 1. Loop to reduce font size until it fits the allowed width
        while font_size > min_font_size:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                break
                
            font_size -= 2 # Shrink and try again
            font = ImageFont.truetype(font_path, font_size)

        # 2. Re-calculate bounding box after the loop finishes
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Exact horizontal center of the tag
        center_x = self.configs.placard_length_px / 2

        # 3. If it STILL doesn't fit, apply the multi-line wrap
        if text_width > max_width:
            # Estimate character width to find safe line breaks
            char_bbox = draw.textbbox((0, 0), "M", font=font)
            avg_char_width = char_bbox[2] - char_bbox[0]
            
            max_chars_per_line = max(1, int(max_width / avg_char_width)) + 10
            wrapped_lines = textwrap.wrap(text, width=max_chars_per_line)
            
            line_height = char_bbox[3] - char_bbox[1]
            line_spacing = 8  # Tight line spacing in pixels

            current_y = y_position
            for line in wrapped_lines:
                draw.text((center_x, current_y), line, fill=color, font=font, anchor="mt")
                current_y += line_height + line_spacing
                
            total_height = current_y - y_position
            return total_height
            
        # 4. If it fits perfectly on one line, draw normally
        else:
            if position == "main":
                text_height = bbox[3] - bbox[1]
                start_y = (y_position + self.configs.main_text_default_font_size/2) - text_height/2
                draw.text((center_x, start_y), text, fill=color, font=font, anchor="mt")
            else:
                text_height = bbox[3] - bbox[1]
                draw.text((center_x, y_position), text, fill=color, font=font, anchor="mt")
            return text_height
    
    def generate_placards(self, output_dir: str = None):
        
        df = pd.read_csv(self.configs.csv_path)
        os.makedirs(output_dir, exist_ok=True)

        for index, row in df.iterrows():
            role = str(row['Role']).upper()
            committee = str(row['Committee'])
            name = str(row['Name'])
            country = str(row['Country/Affiliation']) if pd.notna(row['Country/Affiliation']) else ""
            code = str(row['Code']).lower() if 'Code' in row and pd.notna(row['Code']) else False

            if role == "CHAIR" or role == "CO-CHAIR":
                template_path = self.configs.placard_template_chair
            elif role == "DELEGATE":
                template_path = self.configs.placard_template_delegate
            else:
                continue  # Skip other roles

            match committee:
                case "WHO":
                    comm_name = "WORLD HEALTH ORGANIZATION"
                case "ECOSOC":
                    comm_name = "ECONOMIC AND SOCIAL COUNCIL"
                case "UNSC":
                    comm_name = "UNITED NATIONS SECURITY COUNCIL"
                case "UNEP":
                    comm_name = "国際連合環境計画 (UNEP)"
                case "UNHCR":
                    comm_name = "国際連合難民高等弁務官事務所 (UNHCR)"

            try:
                img = Image.open(template_path).convert("RGBA")
            except FileNotFoundError:
                print(f"Template missing for type: {role}. Skipping {name}.")
                continue

            drawer = ImageDraw.Draw(img)

            if role == "DELEGATE":
                font_choice_path = self.configs.font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(country)) else self.configs.main_font_path
                self._draw_text_autofit(drawer, 
                                        country, 
                                        self.configs.max_text_width, 
                                        self.configs.main_text_default_font_size, 
                                        self.configs.main_text_y_position, 
                                        font_choice_path,
                                        color="#385644",
                                        position="main")
                print(f"Country '{country}' drawn for {name} with role {role}.")
                font_choice_path = self.configs.font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(name)) else self.configs.sub_font_path
                self._draw_text_autofit(drawer, 
                                        name,
                                        self.configs.max_text_width, 
                                        self.configs.sub_text_default_font_size, 
                                        self.configs.sub_text_y_position, 
                                        font_choice_path,
                                        color="#608155",
                                        position="sub")
                print(f"Name '{name}' drawn for {name} with role {role}.")
            else:
                font_choice_path = self.configs.font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(name)) else self.configs.sub_font_path
                self._draw_text_autofit(drawer, 
                                        name, 
                                        self.configs.max_text_width, 
                                        self.configs.main_text_default_font_size, 
                                        self.configs.main_text_y_position, 
                                        font_choice_path,
                                        color="#608155",
                                        position="main")
                print(f"Name '{name}' drawn for {name} with role {role}.")
                font_choice_path = self.configs.font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(role)) else self.configs.main_font_path
                self._draw_text_autofit(drawer, 
                                        role,
                                        self.configs.max_text_width, 
                                        self.configs.sub_text_default_font_size, 
                                        self.configs.sub_text_y_position, 
                                        font_choice_path,
                                        color="#385644",
                                        position="sub")
                print(f"Role '{role}' drawn for {name} with role {role}.")
            font_choice_path = self.configs.font_jp_path if bool(re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]').search(comm_name)) else self.configs.sub_font_path
            self._draw_text_autofit(drawer, 
                                    comm_name, 
                                    self.configs.max_text_width, 
                                    self.configs.committee_default_font_size, 
                                    self.configs.committee_y_position, 
                                    font_choice_path,
                                    color="#ffeed2")
            print(f"Committee '{comm_name}' drawn for {name} with role {role}.")

            comm_logo = Image.open(os.path.join(self.configs.comm_logos_folder, f"{committee}.png")).resize(self.configs.committee_logo_size)
            img.paste(comm_logo, (self.configs.committee_logo_x_position, self.configs.committee_logo_y_position), comm_logo)
            
            if code:
                flag_path = os.path.join(self.configs.flags_folder, f"{code}.png")
                try:
                    # 1. Open the flag and ensure it has an alpha channel
                    flag = Image.open(flag_path).convert("RGBA")
                    
                    # 2. ZOOM AND CROP (Object-fit: Cover)
                    # centering=(0.5, 0.5) ensures it crops equally from all sides
                    flag = ImageOps.fit(flag, self.configs.flag_size, centering=(0.5, 0.5))
                    
                    # 3. CREATE THE ROUNDED CORNER "COOKIE CUTTER" MASK
                    corner_radius = 40  # Change this number to make it more or less round!
                    
                    # Create a blank grayscale image ("L" mode) the exact size of the flag
                    mask = Image.new("L", self.configs.flag_size, 0)
                    draw = ImageDraw.Draw(mask)
                    
                    # Draw a solid white rounded rectangle on our mask
                    draw.rounded_rectangle((0, 0, self.configs.flag_size[0], self.configs.flag_size[1]), radius=corner_radius, fill=255)
                    
                    # 4. Apply the mask to the flag's alpha (transparency) layer
                    flag.putalpha(mask)
                    
                    # 5. Paste it! (We use 'flag' as the third argument so it respects our new rounded transparent corners)
                    img.paste(flag, (self.configs.flag_x_position, self.configs.flag_y_position), flag)
                
                except FileNotFoundError:
                    print(f"⚠️ Warning: Missing flag image at {flag_path}")

            img.save(os.path.join(output_dir, f"{index:03}_placard.png"))
            print(f"Generated placard for {name}")    

    
