import numpy as np
import tifffile as tiff
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import skgstat as skg

class TifflImage:

    def __init__(self, path, name): 
        '''Initialize the TifflImage with a path and name.'''
        self.path = path
        self.name = name
        # Correction ici : on lit l'image puis on la convertit en float
        self.data = tiff.imread(path).astype(float)
    
    @property
    def shape(self):
        '''Return the shape of the image data.'''
        return self.data.shape
    
    def flatten_data(self):
        '''Flatten the image data into a 1D array.'''
        return self.data.flatten()
    
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
        plt.title(f'Histogram of {self.name}')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
-
if __name__ == "__main__":
    
    chemin_image = "projet_mines-Paris-data-processing_2026/donnes_MEB-EDS/export_tiff"
    nom_image = "Laitier1_Cr-Kα.tif"

    mon_image = TifflImage(path=chemin_image, name=nom_image)
    
    print(f"Dimensions de l'image : {mon_image.shape}")
    
    stats_dict = mon_image.compute_statistics()
    print("\nStatistiques de l'image :")
    for cle, valeur in stats_dict.items():
        print(f"  - {cle.capitalize()} : {valeur:.2f}")
        

    print("\nAffichage de l'histogramme...")
    mon_image.plot_histogram(bins=30)
    
    print("--- Fin du traitement ---")