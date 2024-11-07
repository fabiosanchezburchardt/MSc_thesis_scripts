##############################

# S2_2017_D7_ba_differenced_indices.py

# Berechnung der Differenzindizes dNBR, dBAIS2 und dNBR+

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import numpy as np

# Funktion zum Lesen der Input-Raster
def read_raster(file_path):
    with rasterio.open(file_path, "r", driver="GTiff") as dataset:
        array = dataset.read(1)
        metadata = dataset.meta
        return array, metadata

# Funktion zum Schreiben der Output-Raster
def write_raster(file_path, array, metadata):
    with rasterio.open(file_path, "w", **metadata) as dataset:
        dataset.write(array, 1)

# Funktion zur Berechnung der Differenzindizes
def calculate_difference(pre_array, post_array, nodata, method='subtract'):
    rows, cols = pre_array.shape
    result_array = np.empty((rows, cols))

    for gx in range(cols):
        for gy in range(rows):
            # no-data-Werte aus der Berechnung rauslassen
            if pre_array[gy, gx] == nodata or post_array[gy, gx] == nodata:
                result_array[gy, gx] = nodata
                continue
            
            # Berechnen der Differenz durch Subtraktion der post-Werte von den pre-Werten
            if method == 'subtract':
                result_array[gy, gx] = float(pre_array[gy, gx]) - float(post_array[gy, gx])
            # Berechnen der Differenz durch Subtraktion der pre-Werte von den post-Werten
            elif method == 'add':
                result_array[gy, gx] = float(post_array[gy, gx]) - float(pre_array[gy, gx])
    return result_array


### ohne vorherige SCL-Anwendung ###

# Pfade der Input-Raster
input_paths = {
    "NBR_pre": "[absoluter_Pfad]/Python/output_ba/NBR/NBR_20170612.tif",
    "NBR_post": "[absoluter_Pfad]/Python/output_ba/NBR/NBR_20170917.tif",
    "NBRplus_pre": "[absoluter_Pfad]/Python/output_ba/NBRplus/NBRplus_20170612.tif",
    "NBRplus_post": "[absoluter_Pfad]/Python/output_ba/NBRplus/NBRplus_20170917.tif",
    "BAIS2_pre": "[absoluter_Pfad]/Python/output_ba/BAIS2/BAIS2_20170612.tif",
    "BAIS2_post": "[absoluter_Pfad]/Python/output_ba/BAIS2/BAIS2_20170917.tif",
}

# Pfade für die Output-Raster
output_paths = {
    "dNBR": "[absoluter_Pfad]/Python/output_ba/NBR/dNBR.tif",
    "dNBRplus": "[absoluter_Pfad]/Python/output_ba/NBRplus/dNBRplus.tif",
    "dBAIS2": "[absoluter_Pfad]/Python/output_ba/BAIS2/dBAIS2.tif",
}

###

### mit vorheriger SCL-Anwendung ###

# # Pfade der Input-Raster
# input_paths = {
#     "NBR_pre": "[absoluter_Pfad]/Python/output_ba/NBR/NBR_20170612_SCL.tif",
#     "NBR_post": "[absoluter_Pfad]/Python/output_ba/NBR/NBR_20170917_SCL.tif",
#     "NBRplus_pre": "[absoluter_Pfad]/Python/output_ba/NBRplus/NBRplus_20170612_SCL.tif",
#     "NBRplus_post": "[absoluter_Pfad]/Python/output_ba/NBRplus/NBRplus_20170917_SCL.tif",
#     "BAIS2_pre": "[absoluter_Pfad]/Python/output_ba/BAIS2/BAIS2_20170612_SCL.tif",
#     "BAIS2_post": "[absoluter_Pfad]/Python/output_ba/BAIS2/BAIS2_20170917_SCL.tif",
# }

# # Pfade für die Output-Raster
# output_paths = {
#     "dNBR": "[absoluter_Pfad]/Python/output_ba/NBR/dNBR_SCL.tif",
#     "dNBRplus": "[absoluter_Pfad]/Python/output_ba/NBRplus/dNBRplus_SCL.tif",
#     "dBAIS2": "[absoluter_Pfad]/Python/output_ba/BAIS2/dBAIS2_SCL.tif",
# }

###


# Lesen der Input-Raster
NBR_pre, metadata = read_raster(input_paths["NBR_pre"])
NBR_post, _ = read_raster(input_paths["NBR_post"])
NBRplus_pre, _ = read_raster(input_paths["NBRplus_pre"])
NBRplus_post, _ = read_raster(input_paths["NBRplus_post"])
BAIS2_pre, _ = read_raster(input_paths["BAIS2_pre"])
BAIS2_post, _ = read_raster(input_paths["BAIS2_post"])

nodata = metadata['nodata']

# Berechnung der Differenzindizes
dNBR = calculate_difference(NBR_pre, NBR_post, nodata, method='subtract')
dNBRplus = calculate_difference(NBRplus_pre, NBRplus_post, nodata, method='add')
dBAIS2 = calculate_difference(BAIS2_pre, BAIS2_post, nodata, method='add')

# Schreiben der Output-Raster
write_raster(output_paths["dNBR"], dNBR, metadata)
write_raster(output_paths["dNBRplus"], dNBRplus, metadata)
write_raster(output_paths["dBAIS2"], dBAIS2, metadata)

print("Done!")
