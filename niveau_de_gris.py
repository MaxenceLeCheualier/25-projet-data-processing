import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

def convert_gray(image):
    image_array = np.array(image)
    R=image_array[:,:,0]
    G=image_array[:,:,1]
    B=image_array[:,:,2]
    Gray =  np.round(0.2126*R + 0.7152*G + 0.0722*B).astype(np.uint8) #convention 709
    image_gray = Image.fromarray(Gray)
    return image_gray 

def on_select(eclick,erelease):
    coords['x1'], coords['y1'] = int(eclick.xdata), int(eclick.ydata)
    coords['x2'], coords['y2'] = int(erelease.xdata), int(erelease.ydata)

txt=f"projet_mines-Paris-data-processing_2026\donnes_MEB-EDS\export_tif\Laitier1_Al-K_cropped.png"
img = Image.open(txt)
img_gris= img.convert("L")
img_gris_array = np.array(img_gris)

h,l = np.shape(img_gris_array)
vmin = np.min(img_gris_array)
vmax = np.max(img_gris_array)

print("For Al The size is :", (h,l),  ". The minimum value is :", vmin, ". The maximum value is:", vmax)

Element=np.array(['C','Ca','Fe','Mn','Na','O','P','S','Si','Ti','V'])

for el in Element:
     #ATTENTION AU CHEMIN D'ACCES - à modifier par ordinateur 
    txt=f"projet_mines-Paris-data-processing_2026\donnes_MEB-EDS\export_tif\Laitier1_{el}-Kα.tif"
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
    cropped_img = img_gris_array[y1:y2, x1:x2]
    new_image = Image.fromarray(cropped_img)
    new_chemin = f"projet_mines-Paris-data-processing_2026\donnes_MEB-EDS\export_tif\Laitier1_{el}-Kα_cropped.png"
    new_image.save(new_chemin)
    cropped_image = Image.open(new_chemin)

    #CONVERT TO GRAY THE NEW IMAGE
    img_gris= cropped_image.convert("L") 
    img_gris_array = np.array(img_gris)


    h,l = np.shape(cropped_img)
    vmin = np.min(cropped_img)
    vmax = np.max(cropped_img)

    print("For", el, "The size is :", (h,l),  ". The minimum value is :", vmin, ". The maximum value is:", vmax)



