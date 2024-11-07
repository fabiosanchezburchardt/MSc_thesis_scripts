##############################

# S2_2018_D6_ba_SCL.py

# Anwendung des Scene Classification Layers auf alle Index-Raster

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import numpy as np
import os

# Verzeichnis
base_dir = "[absoluter_Pfad]/Python/2018/output_ba/"

# Liste der Indizes
indices = ["BAIS2", "NBR", "NBRplus"]

# Liste der Zeitpunkte
dates = ["20180612", "20180912"]

# Pfade für die SCL-Raster
scl_paths = {
    "20180612": "[absoluter_Pfad]/Python/2018/output_ba/20180612/20180612_SCL_20m_pollino.tif",
    "20180912": "[absoluter_Pfad]/Python/2018/output_ba/20180912/20180912_SCL_20m_pollino.tif"
}

# Klassen, die auf no-data gesetzt werden sollen
no_data_classes = [2, 3, 6, 8, 9, 10, 11]

# Funktion zur Verarbeitung der Rasterdaten
def process_raster(index, date, scl_path):
    input_path = os.path.join(base_dir, index, f"{index}_{date}.tif")
    output_path = os.path.join(base_dir, index, f"{index}_{date}_SCL.tif")
    
    # Lesen der Input-Raster und ihrer Metadaten
    with rasterio.open(input_path) as src_raster:
        raster_data = src_raster.read(1)
        raster_meta = src_raster.meta
        
        # Lesen der SCL-Rasterdaten zur Erstellung der no-data-Maske
        with rasterio.open(scl_path) as src_scl:
            scl_data = src_scl.read(1)
            
            # Erstellen einer Maske für die no-data-Klassen
            mask = np.isin(scl_data, no_data_classes)
            
            # Anwenden der Maske auf die Rasterdaten
            raster_data[mask] = src_raster.nodata
            
            # Aktualisieren der Metadaten
            raster_meta.update({
                'dtype': 'float32',
                'nodata': src_raster.nodata
            })
            
            # Schreiben des Output-Rasters
            with rasterio.open(output_path, 'w', **raster_meta) as dst:
                dst.write(raster_data, 1)

# Iterieren über alle Index-Raster und Anwenden der Funktion zur Verarbeitung der Rasterdaten
for index in indices:
    for date in dates:
        scl_path = scl_paths[date]
        process_raster(index, date, scl_path)


print("Done!")
