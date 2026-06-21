from dataclasses import dataclass
import os

@dataclass
class NametagConfigs:
    
    csv_path: str = f"database/trial.csv"

    # File paths for fonts and templates
    name_font: str = "arial.ttf"
    country_font: str = "arial.ttf"
    committee_font: str = "arial.ttf"
    wifi_font: str = "courier.ttf"

    assets_folder: str = "assets"
    name_font_path: str = os.path.join(assets_folder, "fonts", name_font)
    country_font_path: str = os.path.join(assets_folder, "fonts", country_font)
    committee_font_path: str = os.path.join(assets_folder, "fonts", committee_font)
    wifi_font_path: str = os.path.join(assets_folder, "fonts", wifi_font)
    
    nametag_template_folder: str = os.path.join(assets_folder, "templates", "nametags")
    committee_nametag_template: str = os.path.join(nametag_template_folder, "template_front_committee.png")
    organizer_nametag_template: str = os.path.join(nametag_template_folder, "template_front_organizer.png")
    vip_nametag_template: str = os.path.join(nametag_template_folder, "template_front_vip.png")
    observer_nametag_template: str = os.path.join(nametag_template_folder, "template_front_observer.png")
    jp_back_nametag_template: str = os.path.join(nametag_template_folder, "template_back_jp.png")
    eng_back_nametag_template: str = os.path.join(nametag_template_folder, "template_back_eng.png")
    
    nametags_output: str = "output_nametags"

    # Dimensions and layout

    ppcm: float = 118.11 # Pixels per cm for 300 DPI
    tag_size_px: float = int(9.0 * ppcm) # 9cm
    margin_px: float = int(1.5 * ppcm) # 1.5cm
    max_text_width: float = tag_size_px - (margin_px * 2)


    # === CERTIFICATE CONFIGURATIONS ===
    certificate_output_folder: str = "output_certificates"

    # === PLACARD CONFIGURATIONS ===
    placard_output_folder: str = "output_placards"
    