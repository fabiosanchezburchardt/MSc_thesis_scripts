##############################

# S2_2018_D5_ba_indices.py

# Berechnung der Indizes für die Waldbranduntersuchung

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import os
import numpy as np
import spyndex as sp

# Liste der Zeitpunkte
dates = ["20180612", "20180912"]

# Eingabe und Ausgabeverzeichnis
base_input_path = "[absoluter_Pfad]/Python/2018/output_ba"
base_output_path = "[absoluter_Pfad]/Python/2018/output_ba"

# Bänder, die eingelesen werden
bands = ["B02", "B03", "B04", "B06", "B07", "B08", "B8A", "B12"]

# Indizes, die berechnet werden sollen
indices = ["NBR", "NBRplus", "BAIS2"]

# Schleife über alle Zeitpunkte
for date in dates:
    print(f"Verarbeite Daten für den Zeitpunkt {date}...")

    # Einlesen der Bänder
    band_arrays = {}
    for band in bands:
        band_path = os.path.join(base_input_path, date, f"{date}_{band}_20m_pollino.tif")
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
            "RE2": band_arrays["B06"],
            "RE3": band_arrays["B07"],
            "N": band_arrays["B08"],
            "N2": band_arrays["B8A"],
            "S2": band_arrays["B12"]
        }
    )

    # Speichern der Indizes
    for i, index in enumerate(indices):
        out_array = idx[i]
        out_path = os.path.join(base_output_path, index, f"{index}_{date}.tif")
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

    print(f"NBR, NBRplus und BAIS2 für den {date} wurden erfolgreich erstellt.")

print("Done!")

