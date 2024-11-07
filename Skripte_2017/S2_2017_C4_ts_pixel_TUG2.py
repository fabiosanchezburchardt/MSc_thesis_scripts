##############################

# S2_2017_C4_ts_pixel_TUG2.py

# Ermittlung der Werte zehn ausgewählter Pixel in den Index-Rastern von TUG2

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
import rasterio

# Verzeichnisse, in denen sich die Raster-Dateien befinden
# TUG2: EVI
input_dir = "[absoluter_Pfad]/Python/px_ts/input/TUG2/EVI_corine_forest"
# # TUG2: NDMI
# input_dir = "[absoluter_Pfad]/Python/px_ts/input/TUG2/NDMI_corine_forest"
# # TUG2: NDVI
# input_dir = "[absoluter_Pfad]/Python/px_ts/input/TUG2/NDVI_corine_forest"
# # TUG2: NDWI
# input_dir = "[absoluter_Pfad]/Python/px_ts/input/TUG2/NDWI_corine_forest"
# # TUG2: NMDI
# input_dir = "[absoluter_Pfad]/Python/px_ts/input/TUG2/NMDI_corine_forest"

# Liste der Rasterpositionen (column, row)
positions = [
    (77, 36),
    (135, 23),
    (83, 24),
    (36, 45),
    (49, 54),
    (63, 52),
    (35, 78),
    (66, 137),
    (39, 129),
    (18, 116)
]

# Funktion zum Auslesen der Pixelwerte an den angegebenen Positionen
def extract_pixel_values(raster_file, positions):
    with rasterio.open(raster_file) as src:
        # Erstelle eine leere Liste für die Pixelwerte
        pixel_values = []
        
        # Iterieren über die angegebenen Positionen
        for col, row in positions:
            # Lesen der Pixelwert an der angegebenen Position (row, col)
            # Rasterio verwendet die Reihenfolge row, col für den Indexzugriff
            value = src.read(1)[row, col]
            pixel_values.append((col, row, value))
    
    return pixel_values

# Iterieren über alle GeoTIFF-Dateien im Verzeichnis
for filename in os.listdir(input_dir):
    if filename.endswith(".tif"):
        file_path = os.path.join(input_dir, filename)
        
        # Ausgabe des Dateinamens
        print(f"Datei: {filename}")
        
        # Extrahieren der Pixelwerte für die aktuelle Datei
        pixel_values = extract_pixel_values(file_path, positions)
        
        # Ausgabe der Pixelwerte
        for col, row, value in pixel_values:
            print(f"Spalte {col}; Zeile {row}; {value}")
        
        print("\n" + "-" * 50 + "\n")

print("Done!")
