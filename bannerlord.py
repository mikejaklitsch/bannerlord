import argparse
import os
import shutil
import math

from datetime import datetime
from PIL import Image

BANNERS_PER_ROW = 7
BANNERS_PER_COLUMN = 3
DEFAULT_RIGHT_MARGIN = 44  # The default right margin of the banner files
TEMPLATE_SIZE = (1024, 1024)  # The size of the full page holding banners
CANVAS_SIZE = (
    980,
    1024,
)  # The space actually used by banners, there is a 44 pixel margin on the right
NORMAL_BANNER_SIZE = (
    math.ceil(CANVAS_SIZE[0] / BANNERS_PER_ROW),
    math.ceil(CANVAS_SIZE[1] / BANNERS_PER_COLUMN),
)  # The size of each individual banner, rounding up b/c running over the edge seemed preferable to a gap
HOUSE_BANNER_FOLDER_RELPATH = (
    "./house_banners"  # User created folder containing individual house banners
)
EXTRACTED_BANNER_FOLDER_RELPATH = (
    "./extracted_banners"  # Folder to save extracted banners to
)
BANNER_FILES = [  # Assumed to be in the same folder as this script, a backup will be made of each file edited
    "banners_a.dds",
    "banners_b.dds",
    "banners_c.dds",
    "banners_d.dds",
    "banners_e.dds",
    # "banners_f.dds",  # This file is not used for user selected banners
    "banners_g.dds",
]


# Previous manual adjustments of banner placements mean some files have a different total width allocated for banners
# Adjust this dictionary to match the right margin of each banner file to fix any issues with extraction of banners
# Expects current right margin in pixels, run a normalization first before finding these numbers in the output files
BANNER_FILE_RIGHT_MARGIN = {  # Any custom values are the numbers I found worked best when I was testing
    "banners_a.dds": DEFAULT_RIGHT_MARGIN,
    "banners_b.dds": 72,
    "banners_c.dds": 60,
    "banners_d.dds": DEFAULT_RIGHT_MARGIN,
    "banners_e.dds": DEFAULT_RIGHT_MARGIN,
    "banners_g.dds": DEFAULT_RIGHT_MARGIN,
}


def inject_banners():
    # Expects banner templates to be normalized to the same size of 1024x1024
    house_banner_file_names = os.listdir(HOUSE_BANNER_FOLDER_RELPATH)
    house_banner_file_relpaths = [
        os.path.join(HOUSE_BANNER_FOLDER_RELPATH, house_banner_file)
        for house_banner_file in house_banner_file_names
    ]

    while house_banner_file_relpaths and BANNER_FILES:
        template_file = BANNER_FILES.pop(0)
        shutil.copyfile(
            template_file, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{template_file}"
        )  # Make a backup of the original file
        template_image = Image.open(template_file)

        for i in range(BANNERS_PER_ROW):
            for j in range(BANNERS_PER_COLUMN):
                if house_banner_file_relpaths:
                    house_banner_file_relpath = house_banner_file_relpaths.pop(0)
                    house_banner_image = Image.open(house_banner_file_relpath)
                    house_banner_image = house_banner_image.resize(
                        NORMAL_BANNER_SIZE
                    )  # Resize each banner to fit the template
                    template_image.paste(
                        house_banner_image,
                        (NORMAL_BANNER_SIZE[0] * i, NORMAL_BANNER_SIZE[1] * j),
                    )
                    print(
                        f"Added '{os.path.basename(house_banner_file_relpath)}' to '{template_file}'"
                    )

        template_image.save(template_file)


def extract_banners():
    # Expects banner templates to be normalized to the same size of 1024x1024
    # Uses BANNER_FILE_RIGHT_MARGIN to calculate the right margin of each banner file to properly collect banners without cutting into the next one
    os.makedirs(EXTRACTED_BANNER_FOLDER_RELPATH, exist_ok=True)
    for template_file in BANNER_FILES:
        template_image = Image.open(template_file)
        this_canvas_size = (
            TEMPLATE_SIZE[0] - BANNER_FILE_RIGHT_MARGIN.get(template_file),
            TEMPLATE_SIZE[1],
        )
        this_banner_size = (
            math.ceil(this_canvas_size[0] / BANNERS_PER_ROW),
            math.ceil(this_canvas_size[1] / BANNERS_PER_COLUMN),
        )
        for j in range(BANNERS_PER_COLUMN):
            for i in range(BANNERS_PER_ROW):
                # Crop each banner from the template image using i and j to calculate the coordinates
                # The original image is untouched, the cropped image is saved to a new file in the extracted_banners folder
                banner_image = template_image.crop(
                    (
                        this_banner_size[0] * i,
                        this_banner_size[1] * j,
                        this_banner_size[0] * (i + 1),
                        this_banner_size[1] * (j + 1),
                    )
                )
                # Normalize the banner
                banner_image = banner_image.resize(NORMAL_BANNER_SIZE)
                banner_image.save(
                    os.path.join(
                        EXTRACTED_BANNER_FOLDER_RELPATH, f"{template_file}_{j}_{i}.png"
                    )
                )


def normalize_templates():
    # Normalize all templates to 1024x1024 or whatever you want to set TEMPLATE_SIZE to
    for template_file in BANNER_FILES:
        template_image = Image.open(template_file)
        if template_image.size != TEMPLATE_SIZE:
            shutil.copyfile(
                template_file,
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{template_file}",
            )  # Make a backup of the original file
            template_image = template_image.resize(TEMPLATE_SIZE)

            template_image.save(template_file)


# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject or extract house banners.")

    parser.add_argument(
        "--normalize", action="store_true", help="Normalize templates to 1024x1024"
    )
    parser.add_argument(
        "--inject", action="store_true", help="Inject banners into templates"
    )
    parser.add_argument(
        "--extract", action="store_true", help="Extract banners from templates"
    )

    args = parser.parse_args()

    if args.normalize:
        print("Running template normalization...")
        normalize_templates()
    elif args.extract:
        print("Running banner extraction...")
        extract_banners()
    elif args.inject:
        print("Running banner injection...")
        inject_banners()
    else:
        print(
            "Please specify --inject or --extract or --normalize. Use --normalize on first use."
        )
