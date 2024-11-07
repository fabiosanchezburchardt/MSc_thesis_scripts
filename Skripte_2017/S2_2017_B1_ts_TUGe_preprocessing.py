##############################

# S2_2017_B1_ts_TUGe_preprocessing.py

# Zuschneiden der Sentinel-2 Einzelband-Raster auf die Teiluntersuchungsgebiete

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
import glob
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Listen der übergeordneten Input- und Output-Ordner sowie der Shapefile-Pfade
input_parent_folders = [
    "[absoluter_Pfad]/Python/input_ts_TUG1",
    "[absoluter_Pfad]/Python/input_ts_TUG2",
    "[absoluter_Pfad]/Python/input_ts_TUG3",
    "[absoluter_Pfad]/Python/input_ts_TUG4"
]

output_parent_folders = [
    "[absoluter_Pfad]/Python/output_ts_TUG1",
    "[absoluter_Pfad]/Python/output_ts_TUG2",
    "[absoluter_Pfad]/Python/output_ts_TUG3",
    "[absoluter_Pfad]/Python/output_ts_TUG4"
]

shapefile_paths = [
    "[absoluter_Pfad]/Python/input_shp/TUG1.shp",
    "[absoluter_Pfad]/Python/input_shp/TUG2.shp",
    "[absoluter_Pfad]/Python/input_shp/TUG3.shp",
    "[absoluter_Pfad]/Python/input_shp/TUG4.shp"
]

# Iteration über alle übergeordneten Ordner
for input_parent_folder, output_parent_folder, shapefile_path in zip(input_parent_folders, output_parent_folders, shapefile_paths):
    # Liste der Unterordner im aktuellen übergeordneten Input-Ordner
    subfolders = [folder for folder in os.listdir(input_parent_folder) if os.path.isdir(os.path.join(input_parent_folder, folder))]

    # Für jeden Unterordner im aktuellen übergeordneten Input-Ordner
    for subfolder in subfolders:
        # Input-Ordner für den aktuellen Zeitpunkt-Unterordner
        timepoint_folder = os.path.join(input_parent_folder, subfolder)

        # Ausgabeverzeichnis für den aktuellen Zeitpunkt-Ordner im übergeordneten Output-Ordner (Clip)
        output_timepoint_folder_clip = os.path.join(output_parent_folder, subfolder)
        os.makedirs(output_timepoint_folder_clip, exist_ok=True)

        # Liste der Unterordner für verschiedene Spektralbänder im aktuellen Zeitpunkt-Unterordner
        spectral_folders = [folder for folder in os.listdir(timepoint_folder) if os.path.isdir(os.path.join(timepoint_folder, folder))]

        # Für jeden Spektralband-Unterordner im aktuellen Zeitpunkt-Unterordner
        for spectral_folder in spectral_folders:
            # Input-Ordner für den aktuellen Spektralband-Unterordner
            input_folder = os.path.join(timepoint_folder, spectral_folder)

            # Suchen nach jp2-Dateien im aktuellen Spektralband-Unterordner
            jp2_file = glob.glob(os.path.join(input_folder, "*.jp2"))[0]

            # Öffnen der jp2-Datei
            with rasterio.open(jp2_file) as src:
                # Laden des Shapefiles
                shapefile = gpd.read_file(shapefile_path)

                # Extrahieren der Geometrie aus dem Shapefile
                geometry = shapefile.geometry.values[0]
                geom = geometry.__geo_interface__

                # Ausschneiden des Bildes auf den exakten Ausschnitt des Shapefiles
                out_image, out_transform = mask(src, [geom], crop=True)

                # Update der Metadaten für die Ausgabedatei
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform
                })

                # Ausgabepfad für das zugeschnittene Bild des aktuellen Spektralband-Unterordners (Clip)
                output_cropped_path = os.path.join(output_timepoint_folder_clip, f"{subfolder}_{spectral_folder}_10m_pollino.tif")

                # Schreiben des zugeschnittenen Bildes als GeoTIFF (Clip)
                with rasterio.open(output_cropped_path, "w", **out_meta) as dest:
                    dest.write(out_image)

print("Done!")
