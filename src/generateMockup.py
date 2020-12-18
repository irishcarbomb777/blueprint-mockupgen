# generateMockup.py

import sys
sys.path.append('../')
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
from src import image
import json
import imutils

def generateMockup(logo_path, prod_image_path, location, width, align, mockName):
    # Receive logo and create an image mask
    logo = image.Image.from_file(logo_path, 'MainLogo', color_model='unchanged')
    if(align == 'gaiter'):
        logo.image = imutils.rotate_bound(logo.image, 10)
    logo.resize(new_w = width)
    logo_nd = logo.duplicate('Logo Mask').image
    logo_mask = logo_nd[:,:,3]  # Create transparency mask
    logo_mask = image.Image(logo_mask, 'Logo Mask')
    logo_mask_nd = logo_mask.image
    logo_mask_nd[logo_mask_nd > 0] = 1

    # Receive product image and create an ndarray
    sys.path.append('../productimages')
    prod_image = image.Image.from_file(prod_image_path, 'Product Image Blank', color_model='unchanged')
    prod_image_nd = prod_image.image

    # Set mask location
    if align == 'top-left':
        logo_loc = location 
        full_mask_nd = np.zeros( (prod_image.image.shape[0], prod_image.image.shape[1]) )
        full_mask_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo_mask_nd
    
    if align == 'bottom-center':
        logo_loc = [location[0]-logo_mask.shape[0], location[1] - int((logo_mask.shape[1]/2))]
        full_mask_nd = np.zeros( (prod_image.image.shape[0], prod_image.image.shape[1]) )
        full_mask_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo_mask_nd
    
    if align == 'top-center':
        logo_loc = [location[0], location[1] - int((logo_mask.shape[1]/2))]
        full_mask_nd = np.zeros( (prod_image.image.shape[0], prod_image.image.shape[1]) )
        full_mask_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo_mask_nd
    
    if align == 'center-center':
        logo_loc = [ location[0] - int((location[0]-location[1]-logo_mask.shape[0])/2) - logo_mask.shape[0], location[2] - int(logo_mask.shape[1]/2) ]
        full_mask_nd = np.zeros( (prod_image.image.shape[0], prod_image.image.shape[1]) )
        full_mask_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo_mask_nd
    
    if align == 'gaiter':
        logo_loc = location 
        full_mask_nd = np.zeros( (prod_image.image.shape[0], prod_image.image.shape[1]) )
        full_mask_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo_mask_nd

    full_mask = image.Image(full_mask_nd, 'Full Mask Image')
    full_mask.image[full_mask.image>0] = 255

    prod_image_nd[full_mask_nd > 0] = [0,0,0,0]
    prod_image_masked = image.Image(prod_image_nd, 'Masked Image')
    prod_image_masked.color_space = 'BGRA'
    prod_image_masked.cvt_color(color='rgba')

    # logo = image.Image.from_file(logo_path, 'Color Logo', color_model='unchanged')
    # logo.resize(new_w=width)
    logo.image[logo.image[:,:,3]<130] = [0,0,0,0]
    prod_image_nd[ logo_loc[0]:logo_loc[0]+logo_mask_nd.shape[0], logo_loc[1]:logo_loc[1]+logo_mask_nd.shape[1] ] += logo.image

    color_mockup = image.Image(prod_image_nd, 'Colored Mockup')
    color_mockup.color_space = 'BGRA'
    color_mockup.cvt_color(color='rgba')

    color_mockup_output = image.Image(color_mockup.image, 'Color Mockup Output')
    cv2.imwrite(mockName, color_mockup_output.image)

with open('trades.json') as f:
    package_data = json.load(f)

shirts  = package_data['tshirts']
hoodies = package_data['hoodies']
beanies = package_data['beanies']
jackets = package_data['jackets']
caps    = package_data['caps']
gaiters = package_data['gaiters']

logo_path = 'ajLeblanc.png'
for shirt in shirts:
    generateMockup(logo_path, shirt['filepath'], shirt['position'],
                   shirt['width'], shirt['align'], shirt['mockname'])

for hoodie in hoodies:
    generateMockup(logo_path, hoodie['filepath'], hoodie['position'],
                   hoodie['width'],hoodie['align'], hoodie['mockname'])

for beanie in beanies:
    generateMockup(logo_path, beanie['filepath'], beanie['position'],
                   beanie['width'],beanie['align'], beanie['mockname'])

for jacket in jackets:
    generateMockup(logo_path, jacket['filepath'], jacket['position'],
                   jacket['width'],jacket['align'], jacket['mockname'])

for cap in caps:
    generateMockup(logo_path, cap['filepath'], cap['position'],
                   cap['width'], cap['align'], cap['mockname'])

for gaiter in gaiters:
    generateMockup(logo_path, gaiter['filepath'], gaiter['position'],
                   gaiter['width'], gaiter['align'], gaiter['mockname'])



