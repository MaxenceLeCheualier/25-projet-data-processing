import numpy as np
from PIL import Image 

img = Image.open(r"projet_mines-Paris-data-processing_2026\donnes_MEB-EDS\export_tif\Laitier1_Al-K.tif")

def convert_gray(image):
    image_array = np.array(image)
    R=image_array[:,:,0]
    G=image_array[:,:,1]
    B=image_array[:,:,2]
    Gray =  (0.2126*R + 0.7152*G + 0.0722*B).astype(np.uint8) #convention 709
    image_gray = Image.fromarray(Gray)
    return image_gray 


img_gris= convert_gray(img)
img_gris_array = np.array(img_gris)

h,l = np.shape(img_gris_array)
vmin = np.min(img_gris_array)
vmax = np.max(img_gris_array)

print("The size is :", (h,l),  ". The minimum value is :", vmin, ". The maximum value is:", vmax)
