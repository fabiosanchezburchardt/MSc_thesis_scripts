##############################

# S2_2017_G1_ERA5_nc_to_csv.py

# Konvertierung der ERA5 Temperatur- und Niederschlagsdatensätze vom NetCDF-Format ins CSV-Format

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import xarray as xr
import os

# Output-Verzeichnis für die CSV-Dateien
output_dir = r"[absoluter_Pfad]/Python/ERA5/output"

# # TUG1
# # Öffnen des NetCDF Datensatzes der '2m temperature' und Definieren der Output-Datei
DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_2mt_2017.nc")
output_filename = "TUG1_ERA5_2mt_2017.csv"
# # Öffnen des NetCDF Datensatzes der 'Total precipitation' und Definieren der Output-Datei
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_tp_2017.nc")
# output_filename = "TUG1_ERA5_tp_2017.csv"
# # Koordinaten in Dezimalgrad
longitude = 16.214523
latitude = 39.947357

# # TUG2
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_2mt_2017.nc")
# output_filename = "TUG2_ERA5_2mt_2017.csv"
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_tp_2017.nc")
# output_filename = "TUG2_ERA5_tp_2017.csv"
# longitude = 15.920507
# latitude = 39.726653

# # TUG3
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_2mt_2017.nc")
# output_filename = "TUG3_ERA5_2mt_2017.csv"
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_tp_2017.nc")
# output_filename = "TUG3_ERA5_tp_2017.csv"
# longitude = 15.948814
# latitude = 39.790776

# # TUG4
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_2mt_2017.nc")
# output_filename = "TUG4_ERA5_2mt_2017.csv"
# DS = xr.open_dataset("[absoluter_Pfad]/Python/ERA5/input/ERA5_tp_2017.nc")
# output_filename = "TUG4_ERA5_tp_2017.csv"
# longitude = 16.214523
# latitude = 39.947357


# Auswählen des nächsten Punktes im Datensatz zu den angegebenen Koordinaten (Nearest-Neighbour-Methode)
point_data = DS.sel(longitude=longitude, latitude=latitude, method='nearest')

# Erstellen des Output-Ordners, falls er nicht existiert
os.makedirs(output_dir, exist_ok=True)

# Speichern der CSV-Datei im angegebenen Verzeichnis
output_path = os.path.join(output_dir, output_filename)
point_data.to_dataframe().to_csv(output_path)

print("Done!")
