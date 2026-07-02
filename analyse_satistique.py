import numpy as np
import tifffile as tiff
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import skgstat as skg
from niveau_de_gris import convert_gray

class TifflImage:

    def __init__(self, path): 
        '''Initialize the TifflImage with a path and name.'''
        self.path = path
        self.data = tiff.imread(path).astype(float)

        if self.data.ndim == 3:
            self.to_grayscale()
        
        if np.max(self.data) > 255 and np.max(self.data) <= 65535 :
            self.to_int8()

    def to_grayscale(self, channel=None):
        '''
        Convertit une image RGB(A) en image 2D (niveaux de gris).
        channel=None : luminance standard (0.299R + 0.587G + 0.114B)
        channel=0/1/2 : garde uniquement le canal Rouge/Vert/Bleu
        '''
        if channel is not None:
            self.data = self.data[:, :, channel]
        else:
            r, g, b = self.data[:, :, 0], self.data[:, :, 1], self.data[:, :, 2]
            self.data = 0.299 * r + 0.587 * g + 0.114 * b

    def to_int8(self):
        self.data = np.round((self.data/65535)*255)
        


    @property
    def shape(self):
        '''Return the shape of the image data.'''
        return self.data.shape
    
    def flatten_data(self):
        '''Flatten the image data into a 1D array.'''
        return self.data.flatten()

    def coords(self):
        '''Return the coordinates of the image data as a 2D array.'''
        nx, ny = self.shape
        x = np.arange(nx)
        y = np.arange(ny)
        xv, yv = np.meshgrid(x, y, indexing='ij')
        return np.column_stack((xv.flatten(), yv.flatten()))
    
    def compute_statistics(self):
        '''Compute basic statistics of the image data: mean, median, mode, standard deviation, min, and max.'''
        flattened_data = self.flatten_data()
        mean = np.mean(flattened_data)
        median = np.median(flattened_data)
        
        # Correction pour SciPy récent (keepdims garantit le comportement)
        mode_res = stats.mode(flattened_data, keepdims=True)
        mode = mode_res.mode[0]
        
        std_dev = np.std(flattened_data)
        min_val = np.min(flattened_data)
        max_val = np.max(flattened_data)
        
        return {
            "mean": mean,
            "median": median,
            "mode": mode,
            "std_dev": std_dev,
            "min": min_val,
            "max": max_val
        }
    
    def plot_histogram(self, bins=50):
        '''Plot a histogram of the image data.'''
        flattened_data = self.flatten_data()
        plt.hist(flattened_data, bins=bins, color='blue', alpha=0.7)
        plt.title(f'Histogram of {self.path}')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    
    def compute_variogram(self, n_lags=150, max_lag=None, sample_size=10000, model="spherical"):
        '''Compute the variogram of the image data using skgstat.'''
        coords = self.coords()
        values = self.flatten_data()

        valid = ~np.isnan(values)
        coords = coords[valid]
        values = values[valid]

        idx = np.random.choice(len(values), size=min(sample_size, len(values)), replace=False)

        V = skg.Variogram(coords[idx], values[idx], maxlag=max_lag, n_lags=n_lags, model=model)

        V.plot()
        plt.show()
        return V
    
if __name__ == "__main__":
    
    chemin_image = "Laitier1-x500_BSE-carto.tif"

    mon_image = TifflImage(path=chemin_image)
    
    print(f"Dimensions de l'image : {mon_image.shape}")
    
    stats_dict = mon_image.compute_statistics()
    print("\nStatistiques de l'image :")
    for cle, valeur in stats_dict.items():
        print(f"  - {cle.capitalize()} : {valeur:.2f}")
        

    print("\nAffichage de l'histogramme...")
    mon_image.plot_histogram(bins=30)

    print(mon_image.shape)
    mon_image.compute_variogram_circular()
    
    print("--- Fin du traitement ---")

