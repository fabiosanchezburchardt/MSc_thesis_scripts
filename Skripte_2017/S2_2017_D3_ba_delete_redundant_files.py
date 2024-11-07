##############################

# S2_2017_D3_ba_delete_redundant_files.py

# Löschen des überflüssigen Einzelband-Rasters mit der ursprünglichen Auflösung von 10 m

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os

# Pfad zum übergeordneten Input Ordner
input_folder = r"[absoluter_Pfad]/Python/output_ba"

# Durchsucht alle Unterordner nach Dateien, die "B08_10m_20m_pollino" im Dateinamen beinhalten und löscht diese
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if any(pattern in file for pattern in ["B08_10m_20m_pollino"]):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Gelöscht: {file_path}")

print("Done!")
