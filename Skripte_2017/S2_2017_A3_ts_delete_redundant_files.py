##############################

# S2_2017_A3_ts_delete_redundant_files.py

# Löschen der überflüssigen Einzelband-Raster mit der ursprünglichen Auflösung von 20 m

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os

# Pfad zum übergeordneten Input Ordner
input_folder = r"[absoluter_Pfad]/Python/output_ts"

# Durchsucht alle Unterordner nach Dateien, die "B11_20m_10m_pollino", "B12_20m_10m_pollino" oder "SCL_20m_10m_pollino" im Dateinamen beinhalten und löscht diese
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if any(pattern in file for pattern in ["B11_20m_10m_pollino", "B12_20m_10m_pollino", "SCL_20m_10m_pollino"]):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Gelöscht: {file_path}")

print("Done!")
