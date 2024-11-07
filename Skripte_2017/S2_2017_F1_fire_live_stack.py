##############################

# S2_2017_F1_fire_live_stack.py

# Erstellung von GeoTIFF-Stack-Dateien der Sentinel-2-Bänder B04, B11 und B12
# zu den beiden Zeitpunkten 12.07.2017 und 26.08.2017
# zur Darstellung aktiver Brände in einem Falschfarbenbild

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import xarray as xr

# Raster Pfade für den ersten Zeitpunkt (20170712)
in_B04_20170712 = "[absoluter_Pfad]/Python/fire_live/20170712/20170712_B04_20m_pollino.tif"
in_B11_20170712 = "[absoluter_Pfad]/Python/fire_live/20170712/20170712_B11_20m_pollino.tif"
in_B12_20170712 = "[absoluter_Pfad]/Python/fire_live/20170712/20170712_B12_20m_pollino.tif"

# Raster Pfade für den zweiten Zeitpunkt (20170826)
in_B04_20170826 = "[absoluter_Pfad]/Python/fire_live/20170826/20170826_B04_20m_pollino.tif"
in_B11_20170826 = "[absoluter_Pfad]/Python/fire_live/20170826/20170826_B11_20m_pollino.tif"
in_B12_20170826 = "[absoluter_Pfad]/Python/fire_live/20170826/20170826_B12_20m_pollino.tif"

# Pfade für die Output-Raster
out_stack_fire_live_20170712 = "[absoluter_Pfad]/Python/fire_live/20170712/20170712_stack_20m_pollino.tif"
out_stack_fire_live_20170826 = "[absoluter_Pfad]/Python/fire_live/20170826/20170826_stack_20m_pollino.tif"

def create_geotiff_stack(input_paths, output_path):
    # Öffnen der Rasterdateien
    datasets = [rasterio.open(path) for path in input_paths]

    # Extrahieren der Daten und Metadaten
    bands = ['B04', 'B11', 'B12']
    data_arrays = [xr.DataArray(dataset.read(1), dims=('y', 'x'), name=band) for dataset, band in zip(datasets, bands)]
    NROWS, NCOLS = datasets[0].shape
    trans = datasets[0].transform
    nodata = datasets[0].nodata
    crs = datasets[0].crs

    # Erstellen des Datensatzes
    stacked_ds = xr.Dataset({band: da for band, da in zip(bands, data_arrays)})

    # Erstellen des Output-Rasters
    ds_stack_BA = rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        height=NROWS,
        width=NCOLS,
        count=len(bands),  # Anzahl der Bänder im Stack
        dtype=stacked_ds[bands[0]].dtype,
        crs=crs,
        transform=trans,
        nodata=nodata
    )

    # Separates Schreiben jedes Bandes
    for i, band in enumerate(bands):
        ds_stack_BA.write(stacked_ds[band], i+1)

    ds_stack_BA.close()

    # Schließen der Input-Raster
    for dataset in datasets:
        dataset.close()

    print(f"Stack erfolgreich erstellt: {output_path}")

# Erstellen der Geotiff Stacks für beide Zeitpunkte
create_geotiff_stack([in_B04_20170712, in_B11_20170712, in_B12_20170712], out_stack_fire_live_20170712)
create_geotiff_stack([in_B04_20170826, in_B11_20170826, in_B12_20170826], out_stack_fire_live_20170826)

print("Done!")
