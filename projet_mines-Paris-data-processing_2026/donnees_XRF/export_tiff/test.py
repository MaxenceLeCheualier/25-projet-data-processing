import tifffile as tiff
import matplotlib.pyplot as plt

arr = tiff.imread("Laitier1_Cr.tif")
plt.imshow(arr, cmap="gray")  # normalise automatiquement min/max
plt.colorbar()
plt.show()