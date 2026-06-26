import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

from builders.builders import Nametags, Placards, Certificates
from configs import NametagConfigs, CertificateConfigs, PlacardConfigs

def create_now_folder():
    output_dir = os.path.join("output", f"output_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

if __name__ == "__main__":

    # Load configurations
    nametag_configs = NametagConfigs()
    placard_configs = PlacardConfigs()
    certificate_configs = CertificateConfigs()
    output_dir = create_now_folder()

    # # # Generate Nametags

    # nametag_builder = Nametags(nametag_configs)
    # output_nametags_dir = os.path.join(output_dir, nametag_configs.nametags_output)
    # nametag_builder.generate_individual_tags(output_nametags_dir)
    # print("Done generating all individual tags!")
    # nametag_builder.generate_pdf(output_nametags_dir, output_dir)
    # print("Done generating PDF of nametags!")

    # # # Generate Certificates

    # certificates_builder = Certificates(certificate_configs)
    # output_certs_dir = os.path.join(output_dir, certificate_configs.certificate_output_name)
    # certificates_builder.generate_certificates(output_certs_dir)
    # certificates_builder.generate_pdf(output_certs_dir, output_dir)
    # print("Done generating PDF of certificates!")

    # Generate Placards

    placards_builder = Placards(placard_configs)
    output_placards_dir = os.path.join(output_dir, placard_configs.placard_output_folder)
    placards_builder.generate_placards(output_placards_dir)
    print("Done generating all placards!")
    placards_builder.generate_pdf(output_placards_dir, output_dir)
    print("Done generating PDF of placards!")
