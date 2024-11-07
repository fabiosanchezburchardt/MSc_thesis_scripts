##############################

# S2_2017_C2_ts_NMDI_ranges.py

# Bereinigung von Ausreißern in den Rasterdateien des Index NMDI

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
import rasterio
import numpy as np

def process_geotiff(file_path):
    # Öffnen der GeoTIFF-Datei
    with rasterio.open(file_path, 'r+') as src:
        # Lesen der Daten
        data = src.read(1)
        
        # Maskieren der Werte größer oder gleich 1 und kleiner oder gleich 0
        nodata_value = src.nodata if src.nodata is not None else -9999
        data = np.where((data >= 1) | (data <= 0), nodata_value, data)
        
        # Speichern der modifizierten Daten
        src.write(data, 1)
        
        # Aktualisieren des Nodata-Werts im Dataset (falls nicht gesetzt)
        if src.nodata is None:
            src.nodata = nodata_value

def process_folder(folder_path):
    # Durchsuchen des Ordners und Verarbeiten aller GeoTIFF-Dateien
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tif'):
                file_path = os.path.join(root, file)
                print(f"Verarbeiten der Datei: {file_path}")
                process_geotiff(file_path)

if __name__ == "__main__":
    folder_path = r"[absoluter_Pfad]/Python/output_ts_ranges_NMDI"
    process_folder(folder_path)
    print("Done!")
