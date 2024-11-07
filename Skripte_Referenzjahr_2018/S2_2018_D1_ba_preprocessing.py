##############################

# S2_2018_D1_ba_preprocessing.py

# Vorverarbeitung der Sentinel-2 Einzelband-Raster für die Waldbranduntersuchung
# Zuschneiden auf das Untersuchungsgebiet

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
import glob
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
import geopandas as gpd

# Übergeordneter Input-Ordner
input_parent_folder = "[absoluter_Pfad]/Python/2018/input_ba"

# Übergeordneter Output-Ordner
output_parent_folder = "[absoluter_Pfad]/Python/2018/output_ba"

# Merge-Ordner
merge_parent_folder = "[absoluter_Pfad]/Python/2018/merge/ba"

# Pfad zum Shapefile
shapefile_path = "[absoluter_Pfad]/Python/2018/input_shp/pollino_np.shp"

# Liste der Unterordner im übergeordneten Input-Ordner
subfolders = [folder for folder in os.listdir(input_parent_folder) if os.path.isdir(os.path.join(input_parent_folder, folder))]

# Für jeden Unterordner im übergeordneten Input-Ordner
for subfolder in subfolders:
    # Input-Ordner für den aktuellen Zeitpunkt-Unterordner
    timepoint_folder = os.path.join(input_parent_folder, subfolder)
    
    # Ausgabeverzeichnis für den aktuellen Zeitpunkt-Ordner im übergeordneten Merge-Ordner
    output_timepoint_folder_merge = os.path.join(merge_parent_folder, subfolder)
    os.makedirs(output_timepoint_folder_merge, exist_ok=True)

    # Ausgabeverzeichnis für den aktuellen Zeitpunkt-Ordner im übergeordneten Output-Ordner (Clip)
    output_timepoint_folder_clip = os.path.join(output_parent_folder, subfolder)
    os.makedirs(output_timepoint_folder_clip, exist_ok=True)

    # Liste der Unterordner für verschiedene Spektralbänder im aktuellen Zeitpunkt-Unterordner
    spectral_folders = [folder for folder in os.listdir(timepoint_folder) if os.path.isdir(os.path.join(timepoint_folder, folder))]

    # Für jeden Spektralband-Unterordner im aktuellen Zeitpunkt-Unterordner
    for spectral_folder in spectral_folders:
        # Input-Ordner für den aktuellen Spektralband-Unterordner
        input_folder = os.path.join(timepoint_folder, spectral_folder)
        
        ##################################### Merge Raster #####################################

        # Suchen nach jp2-Dateien im aktuellen Spektralband-Unterordner
        jp2_files = glob.glob(os.path.join(input_folder, "*.jp2"))

        # Öffnen der jp2-Dateien und Lesen der Metadaten des ersten Bildes
        src_files_to_mosaic = []
        for jp2_file in jp2_files:
            src = rasterio.open(jp2_file)
            src_files_to_mosaic.append(src)

        # Zusammenführen der Bilder für den aktuellen Spektralband-Unterordner
        mosaic, out_trans = merge(src_files_to_mosaic)

        # Holen der Transformationsinformationen aus dem ersten Bild
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans})

        # Ausgabepfad für das zusammengefügte Bild des aktuellen Spektralband-Unterordners (Merge)
        output_merge_path = os.path.join(output_timepoint_folder_merge, f"{subfolder}_{spectral_folder}_20m_merge.tif")

        # Schreiben des zusammengefügten Bildes als GeoTIFF für den aktuellen Spektralband-Unterordner (Merge)
        with rasterio.open(output_merge_path, "w", **out_meta) as dest:
            dest.write(mosaic)

        ##################################### Clip Raster #####################################
        
        # Laden des Shapefiles
        shapefile = gpd.read_file(shapefile_path)

        # Öffnen der GeoTIFF-Datei für den aktuellen Spektralband-Unterordner (Merge)
        with rasterio.open(output_merge_path) as src:
            # Extrahieren der Geometrie aus dem Shapefile
            geometry = shapefile.geometry.values[0]
            geom = geometry.__geo_interface__

            # Ausschneiden des Bildes auf den exakten Ausschnitt des Shapefiles
            out_image, out_transform = mask(src, [geom], crop=True)

            # Update der Metadaten für das Ausgabebild
            out_meta = src.meta.copy()
            out_meta.update({"driver": "GTiff",
                             "height": out_image.shape[1],
                             "width": out_image.shape[2],
                             "transform": out_transform})

            # Ausgabepfad für das zugeschnittene Bild des aktuellen Spektralband-Unterordners (Clip)
            output_cropped_path = os.path.join(output_timepoint_folder_clip, f"{subfolder}_{spectral_folder}_20m_pollino.tif")

            # Schreiben des zugeschnittenen Bildes als GeoTIFF (Clip)
            with rasterio.open(output_cropped_path, "w", **out_meta) as dest:
                dest.write(out_image)

print("Done!")
