import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

from builders.builders import Nametags
from configs import Configs

def create_now_folder():
    output_dir = os.path.join("output", f"output_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

if __name__ == "__main__":

    # Load configurations
    configs = Configs()
    output_dir = create_now_folder()

    # Generate Nametags

    nametag_builder = Nametags(configs)
    nametag_builder.generate_individual_tags()
    print("Done generating all individual tags!")
    nametag_builder.generate_pdf()
    print("Done generating PDF of nametags!")

    # Generate Certificates

    certificates_builder = Certificates(os.path.join(output_dir, configs.certificate_output_folder), configs.csv_path)
    certificates_builder.generate_certificates()
    print("Done generating all certificates!")
    certificates_builder.generate_pdf()
    print("Done generating PDF of certificates!")

    # Generate Placards

    placards_builder = Placards(os.path.join(output_dir, configs.placard_output_folder), configs.placards_csv_path)
    placards_builder.generate_placards()
    print("Done generating all placards!")
    placards_builder.generate_pdf()
    print("Done generating PDF of placards!")
