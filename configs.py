from dataclasses import dataclass
import os

@dataclass
class NametagConfigs:
    
    csv_path: str = f"database/trial.csv"

    # File paths for fonts and templates
    name_font: str = "ITCBenguiatStdBoldCnIt.otf"
    name_font_jp: str = "YujiSyuku-Regular.ttf"
    country_font: str = "ITCBenguiatStdBookCn.otf"
    country_font_jp: str = "YujiSyuku-Regular.ttf"
    committee_font: str = "CerebriSans-Regular.ttf"
    role_font: str = "CerebriSans-Bold.ttf"
    wifi_font: str = "courbd.ttf"

    assets_folder: str = "assets"
    name_font_path: str = os.path.join(assets_folder, "fonts", name_font)
    name_font_jp_path: str = os.path.join(assets_folder, "fonts", name_font_jp)
    country_font_path: str = os.path.join(assets_folder, "fonts", country_font)
    country_font_jp_path: str = os.path.join(assets_folder, "fonts", country_font_jp)
    committee_font_path: str = os.path.join(assets_folder, "fonts", committee_font)
    role_font_path: str = os.path.join(assets_folder, "fonts", role_font)
    wifi_font_path: str = os.path.join(assets_folder, "fonts", wifi_font)
    
    nametag_template_folder: str = os.path.join(assets_folder, "templates", "nametags")
    committee_nametag_template: str = os.path.join(nametag_template_folder, "template_front_committee.png")
    committee_nametag_template_alt: str = os.path.join(nametag_template_folder, "template_front_committee_alt.png")
    organizer_nametag_template: str = os.path.join(nametag_template_folder, "template_front_organizer.png")
    vip_nametag_template: str = os.path.join(nametag_template_folder, "template_front_vip.png")
    observer_nametag_template: str = os.path.join(nametag_template_folder, "template_front_obs.png")
    jp_back_nametag_template: str = os.path.join(nametag_template_folder, "template_back_jp.png")
    eng_back_nametag_template: str = os.path.join(nametag_template_folder, "template_back_eng.png")
    
    bento_folder: str = os.path.join(assets_folder, "bento-icons")
    chicken: str = os.path.join(bento_folder, "chicken.png")
    fish: str = os.path.join(bento_folder, "fish.png")
    menchi: str = os.path.join(bento_folder, "menchi.png")
    nori: str = os.path.join(bento_folder, "nori.png")
    tonkatsu: str = os.path.join(bento_folder, "tonkatsu.png")
    veggie: str = os.path.join(bento_folder, "veggie.png")

    nametags_output: str = "output_nametags"

    # Dimensions and layout

    # --- MATH & CONVERSIONS ---
    DPI: int = 300
    ppcm: float = DPI / 2.54          # ~118.11 px per cm
    pt_to_px: float = DPI / 72.0      # ~4.166 px per pt

    tag_size_px: float = int(9.0 * ppcm) # 9cm
    margin_px: float = int(1.0 * ppcm)
    max_text_width: float = tag_size_px - (margin_px * 2)

    committee_y_position: float = 2.9*ppcm
    committee_default_font_size: float = 9*pt_to_px
    main_text_y_position: float = 4.25*ppcm
    main_text_default_font_size: float = 26*pt_to_px
    role_y_position: float = 7.8*ppcm
    role_default_font_size: float = 18*pt_to_px
    sub_text_y_position: float = 5.6*ppcm
    sub_text_default_font_size: float = 14*pt_to_px

    wifi_default_font_size: float = 8*pt_to_px
    wifi_x_position: float = 2.95*ppcm
    wifiid_y_position: float = 8*ppcm
    wifipass_y_position: float = 8.425*ppcm

    day1_bento_x_position: int = int(1.65*ppcm)
    day1_bento_y_position: int = int(0.45*ppcm)
    day2_bento_x_position: int = int(6.05*ppcm)
    day2_bento_y_position: int = int(0.45*ppcm)

    bento_size: tuple = (int(1.3*ppcm), int(1.3*ppcm))

@dataclass
class CertificateConfigs:
    certificate_template: str = "assets/templates/certificates/certificate_template.png"
    certificate_output_folder: str = "output_certificates"

@dataclass
class PlacardConfigs:
    csv_path: str = f"database/trial.csv"
    assets_folder: str = "assets"

    comm_logos_folder: str = os.path.join(assets_folder, "comm-logos")
    flags_folder: str = os.path.join(assets_folder, "flags")

    main_font: str = "BebasNeue-Regular.ttf"
    main_font_path: str = os.path.join(assets_folder, "fonts", main_font)

    sub_font: str = "CerebriSans-Bold.ttf"
    sub_font_path: str = os.path.join(assets_folder, "fonts", sub_font)

    committee_font: str = "CerebriSans-Bold.ttf"
    committee_font_path: str = os.path.join(assets_folder, "fonts", committee_font)

    font_jp: str = "YujiSyuku-Regular.ttf"
    font_jp_path: str = os.path.join(assets_folder, "fonts", font_jp)

    placard_template_chair: str = os.path.join(assets_folder, "templates", "placards", "placard_template_chair.png")
    placard_template_delegate: str = os.path.join(assets_folder, "templates", "placards", "placard_template_delegate.png")
    

    placard_output_folder: str = "output_placards"

    # Dimensions and layout

    # --- MATH & CONVERSIONS ---
    DPI: int = 300
    ppcm: float = DPI / 2.54          # ~118.11 px per cm
    pt_to_px: float = DPI / 72.0      # ~4.166 px per pt

    placard_length_px: float = int(29.7 * ppcm) # A4 length
    placard_height_px: float = int(21.0 * ppcm) # A4 width
    side_margin_px: float = int(5.2 * ppcm)
    top_margin_px: float = int(13.3 * ppcm)
    bottom_margin_px: float = int(3.9 * ppcm)
    max_text_width: float = placard_length_px - (side_margin_px * 2)
    
    main_text_y_position: float = top_margin_px
    main_text_default_font_size: float = 105*pt_to_px
    sub_text_y_position: float = placard_height_px - bottom_margin_px
    sub_text_default_font_size: float = 27*pt_to_px
    committee_y_position: float = 19.9*ppcm
    committee_default_font_size: float = 11*pt_to_px

    committee_logo_size: tuple = (int(3.5*ppcm), int(3.5*ppcm))
    committee_logo_y_position: int = int(16.75*ppcm)
    committee_logo_x_position: int = int(0.75*ppcm)

    flag_size: tuple = (int(4.35*ppcm), int(2.5*ppcm))
    flag_x_position: int = int(24.6*ppcm)
    flag_y_position: int = int(11.2*ppcm)
    