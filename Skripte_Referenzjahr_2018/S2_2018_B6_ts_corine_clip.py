##############################

# S2_2018_B6_ts_corine_clip.py

# Zuschnitt der berechneten Index-Raster auf die CORINE Land Cover Waldklassen

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
import glob
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Pfad zum Shapefile
shapefile_path = "[absoluter_Pfad]/Python/2018/input_shp/corine_mask_forest.shp"

# Liste der Input-Ordner-Listen
all_input_folders = [
    [
        "[absoluter_Pfad]/Python/2018/output_ts_TUG1_SCL/EVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG1_SCL/NDMI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG1_SCL/NDVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG1_SCL/NDWI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG1_SCL/NMDI"
    ],
    [
        "[absoluter_Pfad]/Python/2018/output_ts_TUG2_SCL/EVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG2_SCL/NDMI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG2_SCL/NDVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG2_SCL/NDWI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG2_SCL/NMDI"
    ],
    [
        "[absoluter_Pfad]/Python/2018/output_ts_TUG3_SCL/EVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG3_SCL/NDMI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG3_SCL/NDVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG3_SCL/NDWI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG3_SCL/NMDI"
    ],
    [
        "[absoluter_Pfad]/Python/2018/output_ts_TUG4_SCL/EVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG4_SCL/NDMI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG4_SCL/NDVI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG4_SCL/NDWI",
        "[absoluter_Pfad]/Python/2018/output_ts_TUG4_SCL/NMDI"
    ]
]

# Laden des Shapefiles
shapefile = gpd.read_file(shapefile_path)
geometry = shapefile.geometry.values[0]
geom = [geometry.__geo_interface__]

# Für jede Liste von Input-Ordnern
for input_folders in all_input_folders:
    # Für jeden Input-Ordner in der aktuellen Liste
    for input_folder in input_folders:
        # Finden des corine Unterordners
        corine_folder = os.path.join(input_folder, "corine_forest")
        os.makedirs(corine_folder, exist_ok=True)
        
        # Finden aller .tif Dateien im aktuellen Ordner
        tif_files = glob.glob(os.path.join(input_folder, "*.tif"))
        
        # Für jede .tif Datei im aktuellen Ordner
        for tif_file in tif_files:
            # Öffnen des GeoTIFF
            with rasterio.open(tif_file) as src:
                # Setzen des no-data-Wertes
                nodata = src.nodata if src.nodata is not None else -9999
                
                # Zuschneiden des Rasters mit dem Shapefile und Setzen der no-data-Werte
                out_image, out_transform = mask(src, geom, crop=True, nodata=nodata)
                
                # Metadaten des ursprünglichen Rasters
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                    "nodata": nodata
                })
                
                # Generieren des neuen Dateinamens mit dem Zusatz "_corine_forest"
                base_name = os.path.basename(tif_file)
                name, ext = os.path.splitext(base_name)
                output_file = os.path.join(corine_folder, f"{name}_corine_forest{ext}")
                
                # Schreiben des zugeschnittenen Rasters
                with rasterio.open(output_file, "w", **out_meta) as dest:
                    dest.write(out_image)
                    
print("Done!")
