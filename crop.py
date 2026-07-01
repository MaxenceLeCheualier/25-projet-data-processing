import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import subprocess

coords = {}

def on_select(eclick,erelease):
    coords['x1'], coords['y1'] = int(eclick.xdata), int(eclick.ydata)
    coords['x2'], coords['y2'] = int(erelease.xdata), int(erelease.ydata)

Element=np.array(['Al-K','C-Kα','Ca-Kα','Cr-Kα','Fe-Kα','Mn-Kα','Na-Kα','O-Kα','P-Kα','S-Kα','Si-Kα','Ti-Kα','V-Kα'])

#ATTENTION AU CHEMIN D'ACCES - à modifier par ordinateur 
txt=f"Laitier1-x500_BSE-carto.tif"
img = Image.open(txt)
img_array = np.array(img)

#METHOD TO CROP THE IMAGE TO AVOID THE BORDERS AND LEGEND 
fig, ax = plt.subplots()
ax.imshow(img_array)
coords = {}

selector = RectangleSelector( ax, on_select, useblit = True, button = [1], minspanx = 5, minspany = 5, spancoords = 'pixels', interactive = True)

plt.show()
x1, x2 = sorted([coords['x1'], coords['x2']])
y1, y2 = sorted([coords['y1'], coords['y2']])
cropped_img = img_array[y1:y2, x1:x2]

new_image = Image.fromarray(cropped_img)


new_image.save(f"Laitier1-x500_BSE-carto_cropped.png")


    