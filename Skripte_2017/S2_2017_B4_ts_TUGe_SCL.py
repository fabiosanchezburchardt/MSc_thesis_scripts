##############################

# S2_2017_B4_ts_TUGe_SCL.py

# Anwendung des Scene Classification Layers auf alle Einzelband-Raster

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import numpy as np
import os
from rasterio.enums import Resampling

# Listen der Input- und Output-Ordner
input_folders = [
    r"[absoluter_Pfad]/Python/output_ts_TUG1",
    r"[absoluter_Pfad]/Python/output_ts_TUG2",
    r"[absoluter_Pfad]/Python/output_ts_TUG3",
    r"[absoluter_Pfad]/Python/output_ts_TUG4"
]

output_folders = [
    r"[absoluter_Pfad]/Python/output_ts_TUG1_SCL",
    r"[absoluter_Pfad]/Python/output_ts_TUG2_SCL",
    r"[absoluter_Pfad]/Python/output_ts_TUG3_SCL",
    r"[absoluter_Pfad]/Python/output_ts_TUG4_SCL"
]

# Bänder, die verarbeitet werden sollen
bands_to_process = ["B02", "B03", "B04", "B08", "B11", "B12"]

# Klassen, die auf no-data gesetzt werden sollen
no_data_classes = [2, 3, 6, 8, 9, 10, 11]

def process_raster(band_path, scl_data, no_data_value):
    with rasterio.open(band_path) as src_raster:
        raster_data = src_raster.read(1)
        raster_meta = src_raster.meta
        
        # Konvertieren der Rasterdaten zu float32, bevor der no-data-Wert zugewiesen wird
        raster_data = raster_data.astype('float32')
        
        # Erstellen einer Maske für die no-data-Klassen
        mask = np.isin(scl_data, no_data_classes)
        
        # Anwenden der Maske auf die Rasterdaten
        raster_data[mask] = no_data_value

        return raster_data, raster_meta

def main():
    # Iterieren über alle Input- und Output-Ordner
    for input_folder, output_folder in zip(input_folders, output_folders):
        # Iterieren über jeden Zeitpunkts-Ordner
        for timepoint_folder in os.listdir(input_folder):
            timepoint_path = os.path.join(input_folder, timepoint_folder)
            
            if os.path.isdir(timepoint_path):
                # Suchen nach der SCL-Datei im Zeitpunkt-Ordner
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
                    no_data_value = src_scl.nodata

                # Setzen eines Standard-no-data-Wertes, falls nicht definiert
                if no_data_value is None:
                    no_data_value = -9999

                # Verarbeiten jeder Banddatei im Zeitpunkt-Ordner
                for file in os.listdir(timepoint_path):
                    if any(band in file for band in bands_to_process):
                        band_path = os.path.join(timepoint_path, file)
                        raster_data, raster_meta = process_raster(band_path, scl_data, no_data_value)

                        # Aktualisieren der Metadaten mit no-data-Informationen aus dem ersten Band (B02)
                        if "B02" in file:
                            base_meta = raster_meta

                        # Sicherstellen, dass das Ausgabeverzeichnis existiert
                        output_timepoint_path = os.path.join(output_folder, timepoint_folder)
                        os.makedirs(output_timepoint_path, exist_ok=True)

                        # Erstellen des neuen Dateinamens mit dem "_SCL"-Suffix
                        base_filename, file_extension = os.path.splitext(file)
                        output_file_path = os.path.join(output_timepoint_path, f"{base_filename}_SCL{file_extension}")

                        # Schreiben des verarbeiteten Rasters in eine neue Datei im Ausgabeverzeichnis
                        raster_meta.update({
                            'dtype': 'float32',
                            'nodata': no_data_value
                        })

                        with rasterio.open(output_file_path, 'w', **raster_meta) as dst:
                            dst.write(raster_data, 1)

    print("Done!")

if __name__ == "__main__":
    main()
