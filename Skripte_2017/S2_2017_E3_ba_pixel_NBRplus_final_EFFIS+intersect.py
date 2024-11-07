##############################

# S2_2017_E3_ba_pixel_NBRplus_final_EFFIS+intersect.py

# Berechnung des finalen Flächenanteils als verbrannt identifizierter NBR+-Pixel innerhalb und außerhalb der Gebiete der Referenzdatensätze

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np

# Input-Raster
input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_final_nur_ba_pixel.tif"

# Input-Shapefile EFFIS Referenzgebiete
input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/EFFIS_burned_area_2017_pollino_edit_area.shp"
# # Input-Shapefile extern überarbeitete Referenzgebiete
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/burned_area_intersect_merge.shp"

# Einlesen des Rasters
with rasterio.open(input_raster_path) as src:
    raster_data = src.read(1)
    raster_meta = src.meta
    pixel_size_x, pixel_size_y = src.res
    nodata_value = src.nodata

# Shapefile einlesen und Geometrie extrahieren
shapefile = gpd.read_file(input_shapefile_path)
geometries = shapefile.geometry

# Berechnen der Pixelgröße (in Quadratmetern)
pixel_area = abs(pixel_size_x * pixel_size_y)  # Fläche eines Pixels in Quadratmetern

# Gesamtanzahl der Pixel im gesamten Raster
total_pixel_count = np.sum(raster_data != nodata_value)
print(f"Gesamtanzahl der Pixel im Raster: {total_pixel_count}")

# Berechnen der Gesamtfläche des Rasters
total_area_m2 = total_pixel_count * pixel_area  # in Quadratmetern
total_area_ha = total_area_m2 / 10000  # in Hektar
print(f"Gesamtfläche des Rasters: {total_area_ha:.2f} Hektar")

# Zuschneiden des Rasters mit dem Shapefile (Bereiche innerhalb der Polygone)
with rasterio.open(input_raster_path) as src:
    out_image, out_transform = mask(src, geometries, crop=False, nodata=nodata_value)

# Maske für die Pixel innerhalb der Polygone
inside_polygon_mask = (out_image[0] != nodata_value)

# Pixelanzahl innerhalb der Polygone
inside_pixel_count = np.sum(inside_polygon_mask)
print(f"Anzahl der Pixel innerhalb der Polygone: {inside_pixel_count}")

# Berechnung der Fläche innerhalb der Polygone
inside_area_m2 = inside_pixel_count * pixel_area  # in Quadratmetern
inside_area_ha = inside_area_m2 / 10000  # in Hektar
print(f"Fläche innerhalb der Polygone: {inside_area_ha:.2f} Hektar")

# Pixelanzahl außerhalb der Polygone
outside_pixel_count = total_pixel_count - inside_pixel_count
print(f"Anzahl der Pixel außerhalb der Polygone: {outside_pixel_count}")

# Berechnung der Fläche außerhalb der Polygone
outside_area_m2 = outside_pixel_count * pixel_area  # in Quadratmetern
outside_area_ha = outside_area_m2 / 10000  # in Hektar
print(f"Fläche außerhalb der Polygone: {outside_area_ha:.2f} Hektar")

# Prozentualer Anteil der Fläche innerhalb und außerhalb der Polygone
inside_percentage = (inside_area_ha / total_area_ha) * 100 if total_area_ha > 0 else 0
outside_percentage = (outside_area_ha / total_area_ha) * 100 if total_area_ha > 0 else 0

print(f"Prozentualer Anteil der Fläche innerhalb der Polygone: {inside_percentage:.2f}%")
print(f"Prozentualer Anteil der Fläche außerhalb der Polygone: {outside_percentage:.2f}%")

print("Done!")
