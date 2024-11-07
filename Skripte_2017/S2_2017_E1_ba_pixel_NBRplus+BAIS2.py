##############################

# S2_2017_E1_ba_pixel_NBRplus+BAIS2.py

# Berechnung der Anzahl der als verbrannt und unverbrannt klassifizierten Pixel,
# der verbrannten Fläche in Hektar
# und dem prozentualen Anteil der verbrannten Fläche an der Gesamtfläche
# anhand der Indizes BAIS2 und NBR+ vom 17.09.2017,
# sowohl für die CORINE Land Cover Waldklassen als auch für ausgewählten Vegetationsklassen
# Zusätzlich: Berechnung für das finale NBR+-Raster

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import numpy as np
import os

### Berechnung für die ausgewählten CLC-Vegetationsklassen ###

# Dateipfade: Berechnung für BAIS2
input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/BAIS2_20170917_SCL_corine_forest.tif"
output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/BAIS2_20170917_SCL_corine_forest_2Klassen.tif"
# Klassen-Grenzen für verbrannte Pixel des BAIS2
class_1_min = 0.41462621092796
class_1_max = 0.91422557830811

# # Dateipfade: Berechnung für NBR+
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917_SCL_corine_forest.tif"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/NBRplus_20170917_SCL_corine_forest_2Klassen.tif"
# # Klassen-Grenzen für verbrannte Pixel des NBR+
# class_1_min = -0.46960747241974
# class_1_max = -0.20897236466408


### Berechnung für die CLC-Waldklassen ###

# # Dateipfade: Berechnung für BAIS2
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/BAIS2_20170917_SCL_corine_veg.tif"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/BAIS2_20170917_SCL_corine_veg_2Klassen.tif"
# # Klassen-Grenzen für verbrannte Pixel des BAIS2
# class_1_min = 0.41462621092796
# class_1_max = 0.96698421239853

# # Dateipfade: Berechnung für NBR+
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917_SCL_corine_veg.tif"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/NBRplus_20170917_SCL_corine_veg_2Klassen.tif"
# # Klassen-Grenzen für verbrannte Pixel des NBR+
# class_1_min = -0.46960747241974
# class_1_max = -0.16947513818741


### Berechnung für die finale NBR+ burned area ###

# # Dateipfade: Berechnung für NBR+ final
# input_raster_path = "[absoluter_Pfad]/Python/px_ba/input/NBRplus_20170917_SCL_corine_forest_final_clip.tif"
# output_raster_path = "[absoluter_Pfad]/Python/px_ba/output/NBRplus_20170917_SCL_corine_forest_final_clip_2Klassen.tif"
# # Klassen-Grenzen für verbrannte Pixel des NBR+ final
# class_1_min = -0.46960747241974
# class_1_max = -0.20897236466408

###

# Einlesen des Rasters
with rasterio.open(input_raster_path) as src:
    raster_data = src.read(1)
    raster_meta = src.meta
    pixel_size_x, pixel_size_y = src.res
    nodata_value = src.nodata

# Klassenbildung
# Alle Werte in Klasse 1 (verbrannt) oder Klasse 2 (unverbrannt) einteilen
class_1_mask = (raster_data >= class_1_min) & (raster_data <= class_1_max)
classified_data = np.where(class_1_mask, 1, 2)

# no-data-Werte auf 0 setzen
nodata_mask = (np.isnan(raster_data)) | (raster_data == nodata_value)
classified_data[nodata_mask] = 0

# Berechnung der Anzahl der Pixel pro Klasse
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
with rasterio.open(output_raster_path, "w", **raster_meta) as dest:
    dest.write(classified_data, 1)

print(f"Das klassifizierte Raster wurde erfolgreich gespeichert: {output_raster_path}")

print("Done!")
