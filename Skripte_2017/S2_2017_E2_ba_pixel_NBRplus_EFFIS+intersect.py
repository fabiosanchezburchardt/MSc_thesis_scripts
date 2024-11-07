##############################

# S2_2017_E2_ba_pixel_NBRplus_EFFIS+intersect.py

# Berechnung der Anzahl der als verbrannt und unverbrannt klassifizierten Pixel,
# der verbrannten Fläche in Hektar
# und dem prozentualen Anteil der verbrannten Fläche an der Gesamtfläche
# anhand des Index NBR+ vom 17.09.2017
# für die Gebiete der Referenzdatensätze zur Bewertung der Genauigkeit des Index

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
import os

########## Teil 1: Berechnungen mit EFFIS Gebieten ##########

# Dateipfade: Berechnung ohne SCL
input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/EFFIS_burned_area_2017_pollino_edit.shp"
output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/EFFIS_NBRplus_20170917_2Klassen.tif"

# # Dateipfade: Berechnung mit SCL
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917_SCL.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/EFFIS_burned_area_2017_pollino_edit.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/EFFIS_NBRplus_20170917_SCL_2Klassen.tif"

# # Dateipfade: Berechnung für TUG1
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/TUG1.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/EFFIS_NBRplus_20170917_2Klassen_TUG1.tif"

# # Dateipfade: Berechnung für TUG2
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/TUG2.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/EFFIS_NBRplus_20170917_2Klassen_TUG2.tif"

########## Ende Teil 1 ##########

########## Teil 2: Berechnungen mit extern digitalisierten Gebieten ##########

# # Dateipfade: Berechnung ohne SCL
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/burned_area_intersect_merge.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/digi_extern_NBRplus_20170917_2Klassen.tif"

# # Dateipfade: Berechnung mit SCL
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917_SCL.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/burned_area_intersect_merge.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/digi_extern_NBRplus_20170917_SCL_2Klassen.tif"

# # Dateipfade: Berechnung für TUG1
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/burned_area_intersect_TUG1.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/digi_extern_NBRplus_20170917_2Klassen_TUG1.tif"

# # Dateipfade: Berechnung für TUG2
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917.tif"
# input_shapefile_path = "[absoluter_Pfad]/Python/input_shp/burned_area_intersect_TUG2.shp"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/digi_extern_NBRplus_20170917_2Klassen_TUG2.tif"

########## Ende Teil 2 ##########

# Klassen-Grenzen für verbrannte Pixel
class_1_min = -0.46960747241974
class_1_max = -0.16947513818741

# Einlesen des Rasters
with rasterio.open(input_raster_path) as src:
    raster_data = src.read(1)
    raster_meta = src.meta
    pixel_size_x, pixel_size_y = src.res
    nodata_value = src.nodata

# Shapefile einlesen und Geometrie extrahieren
shapefile = gpd.read_file(input_shapefile_path)
geometries = shapefile.geometry

# Raster mit dem Shapefile zuschneiden
with rasterio.open(input_raster_path) as src:
    out_image, out_transform = mask(src, geometries, crop=True, nodata=0)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

# Klassenbildung
# Alle Werte in Klasse 1 (verbrannt) oder Klasse 2 (unverbrannt) einteilen
class_1_mask = (out_image[0] >= class_1_min) & (out_image[0] <= class_1_max)
classified_data = np.where(class_1_mask, 1, 2)

# Pixel außerhalb des Shapefiles oder mit no-data-Werten auf 0 setzen
mask_outside = (out_image[0] == 0) | (np.isnan(out_image[0])) | (out_image[0] == nodata_value)
classified_data[mask_outside] = 0

# Anzahl der Pixel pro Klasse berechnen
class_1_count = np.sum(classified_data == 1)
class_2_count = np.sum(classified_data == 2)
total_count = class_1_count + class_2_count

print(f"Anzahl der Pixel in Klasse 1 (verbrannt): {class_1_count}")
print(f"Anzahl der Pixel in Klasse 2 (unverbrannt): {class_2_count}")

# Prozentualer Anteil der Klasse 1 (verbrannt) an der Gesamtpixelanzahl
class_1_percentage = (class_1_count / total_count) * 100 if total_count > 0 else 0
print(f"Prozentualer Anteil der Klasse 1 (verbrannt) an der Gesamtpixelanzahl: {class_1_percentage:.2f}%")

# Berechnung der Fläche der Klasse 1 (verbrannt) und Umwandlung in Hektar
pixel_area = abs(pixel_size_x * pixel_size_y)  # Fläche eines Pixels in Quadratmetern
class_1_area_ha = (class_1_count * pixel_area) / 10000  # Gesamtfläche der Klasse 1 (verbrannt) in Hektar
print(f"Gesamte Fläche der Klasse 1 (verbrannt): {class_1_area_ha:.2f} Hektar")

# Speichern des neue Rasters mit den gleichen Metadaten
with rasterio.open(output_raster_path, "w", **out_meta) as dest:
    dest.write(classified_data, 1)

print(f"Das klassifizierte Raster wurde erfolgreich gespeichert: {output_raster_path}")

print("Done!")
