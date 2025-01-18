Bannerlord takes existing individual banner files, with no known limits on filetype(png definitely works), and injects them into existing banner texture images.

Expects Python 3.12.6, earlier versions may or may not work

To run:
> pip install --upgrade pip
> pip install -r requirements.txt # its only 1 package but whatevs

# Make a copy of banner texture images and paste them in the same directory as bannerlord.py
# 'banners_a'-'banners_e' and 'banners_g' are expected

# From the same directory normalize copied images to 1024x1024
# It's important to do this first or everything else won't work properly

> python3 bannerlord.py --normalize

# Extract individual banners from existing texture files
# This will create a new directory with banner images named based
# on their position in the previous textures

> python3 bannerlord.py --extract

# Create a new directory house_banners at the same level as bannerlord.py
# This will pull images from house_banners and inject them into the banners texture files

> python3 bannerlord.py --inject