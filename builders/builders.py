import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

from configs import NametagConfigs

class Nametags:
    def __init__(self, configs: NametagConfigs):
        self.configs = configs
        self.output_dir = os.path.join(outputconfigs.nametags_output)
        os.makedirs(self.output_dir, exist_ok=True)

    def _draw_text_autofit(self, draw, text, max_width, max_font_size, y_position, font_path):
        """
        Draws centered text. Shrinks font size until it fits within max_width.
        """
        font_size = max_font_size
        font = ImageFont.truetype(font_path, font_size)
        
        # Loop to reduce font size until it fits the allowed width
        while True:
            # Get bounding box of the text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width <= max_width or font_size <= 10: # 10 is absolute minimum size
                break
            font_size -= 2 # Shrink and try again
            font = ImageFont.truetype(font_path, font_size)

        # Calculate X position to center the text
        x_position = (self.TAG_SIZE_PX - text_width) / 2
        
        # Draw the text
        draw.text((x_position, y_position), text, fill="black", font=font)
        return text_height

    def generate_individual_tags(self):
        # Load data
        df = pd.read_csv(self.configs.csv_path)
        
        for index, row in df.iterrows():
            name = str(row['Name'])
            role = str(row['Role']).lower()
            country = str(row['Country'])
            committee = str(row['Committee'])
            wifi_id = str(row['WifiID'])
            wifi_pass = str(row['WifiPass'])
            
            front_template_path = f"template_{role}_front.png"
            back_template_path = f"template_{role}_back.png"
            
            try:
                front_img = Image.open(front_template_path).convert("RGBA")
                back_img = Image.open(back_template_path).convert("RGBA")
            except FileNotFoundError:
                print(f"Template missing for role: {role}. Skipping {name}.")
                continue
                
            front_draw = ImageDraw.Draw(front_img)
            back_draw = ImageDraw.Draw(back_img)
            
            # 2. Draw Front Details (Adjust the Y-coordinates to fit your template design)
            # Using 80 as max font size for Name, 50 for Country/Committee
            self._draw_text_autofit(front_draw, name, self.MAX_TEXT_WIDTH, max_font_size=80, y_position=300, font_path=self.font_path)
            self._draw_text_autofit(front_draw, country, self.MAX_TEXT_WIDTH, max_font_size=50, y_position=500, font_path=self.font_path)
            self._draw_text_autofit(front_draw, committee, self.MAX_TEXT_WIDTH, max_font_size=50, y_position=600, font_path=self.font_path)

            # 3. Draw Back Details (Wifi info)
            self._draw_text_autofit(back_draw, f"Network: {wifi_id}", self.MAX_TEXT_WIDTH, max_font_size=40, y_position=400, font_path=self.font_path)
            self._draw_text_autofit(back_draw, f"Password: {wifi_pass}", self.MAX_TEXT_WIDTH, max_font_size=40, y_position=450, font_path=self.font_path)

    def generate_pdf(self):
        # This function can be implemented to combine front and back images into a PDF
        pass

# Create an output folder
OUTPUT_DIR = "generated_tags"
os.makedirs(OUTPUT_DIR, exist_ok=True)



        # 4. Save individual files
        front_img.save(os.path.join(OUTPUT_DIR, f"{index:03}_{name}_front.png"))
        back_img.save(os.path.join(OUTPUT_DIR, f"{index:03}_{name}_back.png"))
        print(f"Generated tags for {name}")
