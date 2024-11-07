##############################

# S2_2017_A2_ts_resampling.py

# Anpassung der Pixelgröße (resampling) der Einzelband-Raster

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os
from osgeo import gdal

# GDAL-Ausnahmen verwenden
gdal.UseExceptions()

# Pfade zu den Eingabe- und Ausgabeverzeichnissen
input_directory = "[absoluter_Pfad]/Python/output_ts"
reference_band_path = "[absoluter_Pfad]/Python/output_ts/20170309/20170309_B08_10m_pollino.tif"  # Band B08 vom ersten Datum wird als Referenz verwendet

# Öffnen des Referenzbands (10m Auflösung), um die gewünschten Geometrieinformationen zu erhalten
reference_band = gdal.Open(reference_band_path)
reference_geotransform = reference_band.GetGeoTransform()
reference_projection = reference_band.GetProjection()
reference_width = reference_band.RasterXSize
reference_height = reference_band.RasterYSize

# Iterieren über alle Unterordner und Dateien im Eingabeverzeichnis
for root, dirs, files in os.walk(input_directory):
    for filename in files:
        if filename.endswith(".tif") and ("B11_20m_10m_pollino" in filename or "B12_20m_10m_pollino" in filename or "SCL_20m_10m_pollino" in filename):
            input_band_path = os.path.join(root, filename)
            output_resampled_band_path = os.path.join(root, filename.replace("_20m_10m_", "_10m_"))

            # Öffnen das Eingabebands (20m Auflösung)
            input_band = gdal.Open(input_band_path)

            # Resampling mit GDAL durchführen
            gdal.Warp(
                output_resampled_band_path,
                input_band,
                format='GTiff',
                width=reference_width,
                height=reference_height,
                xRes=10,
                yRes=10,
                resampleAlg=gdal.GRA_NearestNeighbour,  # Nearest Neighbour Resampling-Methode
                dstSRS=reference_projection,
                outputBounds=(
                    reference_geotransform[0],
                    reference_geotransform[3] + reference_geotransform[5] * reference_height,
                    reference_geotransform[0] + reference_geotransform[1] * reference_width,
                    reference_geotransform[3]
                )
            )

            print(f'Resampling abgeschlossen für {filename}. Die Ausgabedatei wurde gespeichert unter {output_resampled_band_path}')

print('Done!')
