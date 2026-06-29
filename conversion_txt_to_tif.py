import os
import numpy as np
import tifffile as tiff
from pathlib import Path

def convert_txt_to_tiff(file_path, out_dir):
    """
    Convert a .txt file to a numpy array.
    
    Parameters:
    file_path (str): Path to the .txt file.
    out_dir (str): Path to the output directory for the .tiff file.
    
    Returns:
    np.ndarray: Numpy array containing the data from the .txt file.
    """
    
    # Lire le fichier txt et convertir les données en un tableau numpy
    rows = []
    with open(file_path, 'r') as file:
        for line in file :
            line = line.strip()
            if line:  # Check if the line is not empty
                vals = [v for v in line.split(";") if v!=""]
                if vals:
                    rows.append([float(v) for v in vals])

    arr = np.array(rows)

    #Affichage des valeurs min et max 
    min_val = arr.min()
    max_val = arr.max()
    print(f"Min value: {min_val}, Max value: {max_val}")

    #Definir sur combien les valeurs sont codées
    signed = min_val < 0

    if signed:
        if min_val >= -32768 and max_val <= 32767:
            dtype = np.int16
        else:
            dtype = np.int32
    else:
        if max_val <= 65535:
            dtype = np.uint16
        else:
            dtype = np.uint32

    # Convertir le tableau en type de données approprié
    arr = arr.astype(dtype)

    file_path = Path(file_path)
    out_path = Path(out_dir) / (file_path.stem + ".tif")
    tiff.imwrite(str(out_path), arr)
    return out_path

def main(input_dir, out_dir):
    input_dir = Path(input_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for file_path in input_dir.glob("*.txt"):
        convert_txt_to_tiff(file_path, out_dir)

if __name__ == "__main__":
    main("projet_mines-Paris-data-processing_2026/donnees_XRF/export_text", "projet_mines-Paris-data-processing_2026/donnees_XRF/export_tiff")