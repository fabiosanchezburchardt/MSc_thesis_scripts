##############################

# S2_2017_A5_ts_indices.py

# Berechnung der Vegetationsindizes für die Trockenstressuntersuchung

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import os
import numpy as np
import spyndex as sp

# Liste der Zeitpunkte
dates = ["20170309", "20170321", "20170329", "20170408", "20170415", "20170423", "20170505", "20170513", "20170528", "20170607", "20170612", "20170629", "20170709", "20170719", "20170729", "20170806", "20170816", "20170826", "20170905", "20170917", "20171005", "20171017", "20171022", "20171104", "20171124"]

# Eingabe und Ausgabeverzeichnis
base_input_path = "[absoluter_Pfad]/Python/output_ts_SCL"
base_output_path = "[absoluter_Pfad]/Python/output_ts_SCL"

# Bänder, die eingelesen werden
bands = ["B02", "B03", "B04", "B08", "B11", "B12"]

# Indizes, die berechnet werden sollen
indices = ["NDVI", "EVI", "NDWI", "NDMI", "NMDI"]

# Schleife über alle Zeitpunkte
for date in dates:
    print(f"Verarbeite Daten für den Zeitpunkt {date}...")

    # Einlesen der Bänder
    band_arrays = {}
    for band in bands:
        band_path = os.path.join(base_input_path, date, f"{date}_{band}_10m_pollino_SCL.tif")
        with rasterio.open(band_path, "r", driver="GTiff") as dataset:
            band_arrays[band] = dataset.read(1).astype(np.float32) / 10000
            if band == "B02":  # Metadaten von Band B02 extrahieren
                nrows, ncols = dataset.height, dataset.width
                transform = dataset.transform
                nodata = dataset.nodata
                crs = dataset.crs

    # Berechnung der Indizes
    idx = sp.computeIndex(
        index=indices,
        params={
            "B": band_arrays["B02"],
            "G": band_arrays["B03"],
            "R": band_arrays["B04"],
            "N": band_arrays["B08"],
            "S1": band_arrays["B11"],
            "S2": band_arrays["B12"],
            "g": 2.5,
            "C1": 6.0,
            "C2": 7.5,
            "L": 1.0
        }
    )

    # Speichern der Indizes
    for i, index in enumerate(indices):
        out_array = idx[i]
        out_path = os.path.join(base_output_path, index, f"{index}_{date}_SCL.tif")
        with rasterio.open(
            out_path,
            "w",
            driver="GTiff",
            height=nrows,
            width=ncols,
            count=1,
            dtype=out_array.dtype,
            crs=crs,
            transform=transform,
            nodata=nodata
        ) as out_dataset:
            out_dataset.write(out_array, 1)

    print(f"Alle Indizes für den {date} wurden erstellt.")

print("Done!")
