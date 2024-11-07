##############################

# S2_2017_D4_ba_rename_TCI_files.py

# Umbennenung der TCI-Dateien

# Autor: Fabio Adrian Sanchez Burchardt
# 2024

##############################

import os

# Pfad zum übergeordneten Input Ordner
input_folder = r"[absoluter_Pfad]/Python/output_ba"

# Durchsucht alle Unterordner nach Dateien, die "TCI_10m_20m_pollino" im Dateinamen beinhalten und benennt diese um
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if "TCI_10m_20m_pollino" in file:
            file_path = os.path.join(root, file)
            new_file_name = file.replace("TCI_10m_20m_pollino", "TCI_10m_pollino")
            new_file_path = os.path.join(root, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"Umbenannt: {file_path} -> {new_file_path}")

print("Done!")
