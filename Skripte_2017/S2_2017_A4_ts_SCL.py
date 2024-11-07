##############################
# S2_2017_A4_ts_SCL.py

# Anwendung des Scene Classification Layers auf alle Einzelband-Raster

# Autor: Fabio Adrian Sanchez Burchardt
# 2024
##############################

import rasterio
import numpy as np
import os
from rasterio.enums import Resampling

# Eingabe und Ausgabeverzeichnis
base_dir = "[absoluter_Pfad]/Python/output_ts/"
output_dir = "[absoluter_Pfad]/Python/output_ts_SCL/"

# zu verarbeitende Bänder
bands_to_process = ["B02", "B03", "B04", "B08", "B11", "B12"]

# Klassen, die auf no-data gesetzt werden sollen
no_data_classes = [2, 3, 6, 8, 9, 10, 11]

def process_raster(band_path, scl_data):
    with rasterio.open(band_path) as src_raster:
        raster_data = src_raster.read(1)
        raster_meta = src_raster.meta

        # Erstellen einer Maske für die no-data-Klassen
        mask = np.isin(scl_data, no_data_classes)
        
        # Anwenden der Maske auf die Rasterdaten
        raster_data = raster_data.astype('float32')
        raster_data[mask] = np.nan

        return raster_data, raster_meta

def main():
    # Iterieren über jeden Zeitpunkt-Ordner
    for timepoint_folder in os.listdir(base_dir):
        timepoint_path = os.path.join(base_dir, timepoint_folder)
        
        if os.path.isdir(timepoint_path):
            # Suchen der SCL-Datei im Zeitpunkt-Ordner
            scl_file = None
            for file in os.listdir(timepoint_path):
                if "SCL" in file:
                    scl_file = os.path.join(timepoint_path, file)
                    break

            if scl_file is None:
                print(f"Keine SCL-Datei gefunden in {timepoint_path}")
                continue
            
            # Lesen der SCL-Datei
            with rasterio.open(scl_file) as src_scl:
                scl_data = src_scl.read(1)

            # Prozessieren jedes Einzelband-Rasters im Zeitpunkt-Ordner
            for file in os.listdir(timepoint_path):
                if any(band in file for band in bands_to_process):
                    band_path = os.path.join(timepoint_path, file)
                    raster_data, raster_meta = process_raster(band_path, scl_data)

                    # Aktualisieren der Metadaten mit NaN als nodata-Wert
                    if "B02" in file:
                        base_meta = raster_meta

                    # Sicherstellen, dass das Ausgabeverzeichnis existiert
                    output_timepoint_path = os.path.join(output_dir, timepoint_folder)
                    os.makedirs(output_timepoint_path, exist_ok=True)

                    # Erstellen des neuen Dateinamens mit dem Suffix „_SCL“
                    base_filename, file_extension = os.path.splitext(file)
                    output_file_path = os.path.join(output_timepoint_path, f"{base_filename}_SCL{file_extension}")

                    # Aktualisierung der Metadaten mit dem NaN-Wert (nodata)
                    raster_meta.update({
                        'dtype': 'float32',
                        'nodata': np.nan
                    })

                    # Schreiben des Output-Rasters
                    with rasterio.open(output_file_path, 'w', **raster_meta) as dst:
                        dst.write(raster_data, 1)

    print("Done!")

if __name__ == "__main__":
    main()
