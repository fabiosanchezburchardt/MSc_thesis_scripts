##############################

# S2_2017_B5_ts_TUGe_indices.py

# Berechnung der Vegetationsindizes für die Trockenstressuntersuchung in den Teiluntersuchungsgebieten

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import rasterio
import os
import numpy as np
import spyndex as sp

# Definieren der Input- und Output-Ordner sowie der entsprechenden Zeitpunkte
input_output_folders = [
    {
        "input": r"[absoluter_Pfad]/Python/output_ts_TUG1_SCL",
        "output": r"[absoluter_Pfad]/Python/output_ts_TUG1_SCL",
        "dates": [20170609, 20170612, 20170614, 20170617, 20170622, 20170624, 20170629, 20170704, 20170707, 20170709, 20170712, 20170714]
    },
    {
        "input": r"[absoluter_Pfad]/Python/output_ts_TUG2_SCL",
        "output": r"[absoluter_Pfad]/Python/output_ts_TUG2_SCL",
        "dates": [20170709, 20170712, 20170717, 20170719, 20170722, 20170724, 20170729, 20170801, 20170803, 20170806, 20170808, 20170813]
    },
    {
        "input": r"[absoluter_Pfad]/Python/output_ts_TUG3_SCL",
        "output": r"[absoluter_Pfad]/Python/output_ts_TUG3_SCL",
        "dates": [20170609, 20170612, 20170629, 20170704, 20170712, 20170717, 20170722, 20170729, 20170801, 20170806, 20170813, 20170816, 20170826, 20170831]
    },
    {
        "input": r"[absoluter_Pfad]/Python/output_ts_TUG4_SCL",
        "output": r"[absoluter_Pfad]/Python/output_ts_TUG4_SCL",
        "dates": [20170604, 20170612, 20170622, 20170629, 20170707, 20170712, 20170719, 20170727, 20170801, 20170806, 20170811, 20170818, 20170826, 20170831]
    }
]

# Bänder, die eingelesen werden
bands = ["B02", "B03", "B04", "B08", "B11", "B12"]

# Indizes, die berechnet werden sollen
indices = ["NDVI", "EVI", "NDWI", "NDMI", "NMDI"]

def process_timepoint(date, input_path, output_path):
    print(f"Verarbeite Daten für den Zeitpunkt {date}...")

    # Einlesen der Bänder
    band_arrays = {}
    for band in bands:
        band_file_path = os.path.join(input_path, str(date), f"{date}_{band}_10m_pollino_SCL.tif")
        with rasterio.open(band_file_path, "r", driver="GTiff") as dataset:
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
        output_index_path = os.path.join(output_path, index)
        os.makedirs(output_index_path, exist_ok=True)
        out_file_path = os.path.join(output_index_path, f"{index}_{date}_SCL.tif")
        
        with rasterio.open(
            out_file_path,
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

def main():
    for folder_info in input_output_folders:
        input_path = folder_info["input"]
        output_path = folder_info["output"]
        dates = folder_info["dates"]

        for date in dates:
            process_timepoint(date, input_path, output_path)

    print("Done!")

if __name__ == "__main__":
    main()
