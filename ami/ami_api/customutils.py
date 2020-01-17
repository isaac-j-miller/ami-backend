import os, sqlite3, sys
sys.path.append('..')

IMAGE_STORAGE = os.path.abspath('./images')
OVERLAY_STORAGE = os.path.abspath('./images/overlays')
STITCH_STORAGE = os.path.abspath('./images/stitched')


def generate_name_base(requestdata):
    #TODO: make this generate an output filename base
    return str()

