##############################

# S2_2017_B3_ts_TUGe_delete_redundant_files.py

# Löschen der überflüssigen Einzelband-Raster mit der ursprünglichen Auflösung von 20 m

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os

# Liste der übergeordneten Input-Ordner
input_folders = [
    r"[absoluter_Pfad]/Python/output_ts_TUG1",
    r"[absoluter_Pfad]/Python/output_ts_TUG2",
    r"[absoluter_Pfad]/Python/output_ts_TUG3",
    r"[absoluter_Pfad]/Python/output_ts_TUG4"
]

# Muster der Dateinamen, die gelöscht werden sollen
patterns = ["B11_20m_10m_pollino", "B12_20m_10m_pollino", "SCL_20m_10m_pollino"]

# Durchsuche alle Unterordner nach Dateien, die eines der Muster im Dateinamen beinhalten und lösche diese
for input_folder in input_folders:
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if any(pattern in file for pattern in patterns):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Gelöscht: {file_path}")

print("Done!")
