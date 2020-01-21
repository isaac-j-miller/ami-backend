import os, sqlite3, sys, subprocess
import json
sys.path.append('..')

IMAGE_STORAGE = os.path.abspath('./images')
OVERLAY_STORAGE = os.path.abspath('./images/overlays')
STITCH_STORAGE = os.path.abspath('./images/stitched')


def generate_name_base(requestdata):
    #TODO: make this generate an output filename base
    return str()

def get_tif_bbox(filename):
    answer=subprocess.check_output(['gdalinfo',filename,'-json'])
    jsonAnswer = json.loads(answer)
    left = jsonAnswer['cornerCoordinates']['upperLeft'][0]
    bottom = jsonAnswer['cornerCoordinates']['lowerLeft'][1]
    right = jsonAnswer['cornerCoordinates']['upperRight'][0]
    top = jsonAnswer['cornerCoordinates']['upperLeft'][1]
    print(filename, jsonAnswer['cornerCoordinates'])
    return [left, bottom, right, top]
    
    

