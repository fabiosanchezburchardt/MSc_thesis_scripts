##############################

# S2_2017_D8_ba_corine_clip.py

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
shapefile_path = "[absoluter_Pfad]/Python/input_shp/corine_mask_forest.shp"
# shapefile_path = "[absoluter_Pfad]/Python/input_shp/corine_mask_veg.shp"   ## Version 2

# Ordner mit den Input GeoTIFF-Dateien
input_folders = [
    "[absoluter_Pfad]/Python/output_ba/NBR",
    "[absoluter_Pfad]/Python/output_ba/NBRplus",
    "[absoluter_Pfad]/Python/output_ba/BAIS2"
]

# Laden des Shapefiles
shapefile = gpd.read_file(shapefile_path)
geometry = shapefile.geometry.values[0]
geom = [geometry.__geo_interface__]

# Für jeden Input-Ordner
for input_folder in input_folders:
    # Finden des corine Unterordners
    corine_folder = os.path.join(input_folder, "corine_forest")
    # corine_folder = os.path.join(input_folder, "corine_veg")   ## Version 2
    os.makedirs(corine_folder, exist_ok=True)
    
    # Finden aller .tif Dateien im aktuellen Ordner
    tif_files = glob.glob(os.path.join(input_folder, "*.tif"))
    
    # Für jede .tif Datei im aktuellen Ordner
    for tif_file in tif_files:
        # Öffnen der GeoTIFF-Datei
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
            
            # Generieren des neuen Dateinamens mit dem Zusatz "_corine_forest" (oder "_corine_veg")
            base_name = os.path.basename(tif_file)
            name, ext = os.path.splitext(base_name)
            output_file = os.path.join(corine_folder, f"{name}_corine_forest{ext}")
            # output_file = os.path.join(corine_folder, f"{name}_corine_veg{ext}")   ## Version 2
            
            # Schreiben des zugeschnittenen Rasters
            with rasterio.open(output_file, "w", **out_meta) as dest:
                dest.write(out_image)
                
print("Done!")
