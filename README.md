# MSc_thesis_scripts

Dieses repository beinhaltet alle Python-Skripte, welche für die Durchführung der Masterarbeit mit dem Titel "Untersuchung von Trockenstress und Waldbränden anhand von Sentinel-2 Daten unter Berücksichtigung verschiedener spektraler Indizes im Nationalpark Pollino (Italien) im Sommer 2017" verwendet wurden. Der Ordner "Skripte_2017" umfasst alle Skripte für den Untersuchungszeitraum 2017, im Ordner "Skripte_Referenzjahr_2018" liegen alle Skripte für das Referenzjahr 2018.

#### Conda Version:
23.11.0

#### Python Version:
3.10.13

#### Verwendete Python Pakete und Version:
- gdal (3.9.0)
- geopandas (0.9.0)
- glob (3.10.13)
- numpy (1.26.4)
- os (3.10.13)
- rasterio (1.3.10)
- spyndex (0.6.0)
- xarray (2024.3.0)

#### Reihenfolge der Skripte:

Skripte zur Vorbereitung der Trockenstressuntersuchung im gesamten UG 2017 (S2_2017_A)
1. S2_2017_A1_ts_preprocessing.py
2. S2_2017_A2_ts_resampling.py
3. S2_2017_A3_ts_delete_redundant_files.py
4. S2_2017_A4_ts_SCL.py
5. S2_2017_A5_ts_indices.py
6. S2_2017_A6_ts_corine_clip.py

Skripte zur Vorbereitung der Trockenstressuntersuchung in den TUGen 2017 (S2_2017_B)
7. S2_2017_B1_ts_TUGe_preprocessing.py
8. S2_2017_B2_ts_TUGe_resampling.py
9. S2_2017_B3_ts_TUGe_delete_redundant_files.py
10. S2_2017_B4_ts_TUGe_SCL.py
11. S2_2017_B5_ts_TUGe_indices.py
12. S2_2017_B6_ts_TUGe_corine_clip.py
13. S2_2017_B7_ts_TUG1+2_ohne_SCL.py
14. S2_2017_B8_ts_TUG1+2_ohne_SCL_corine_clip.py

Skripte zu den pixelbasierten Berechnungen für die Trockenstressuntersuchung 2017 (S2_2017_C)
S2_2017_C1_ts_indices_ranges.py
S2_2017_C2_ts_NMDI_ranges.py
S2_2017_C3_ts_pixel_TUG1.py
S2_2017_C4_ts_pixel_TUG2.py
S2_2017_C5_ts_pixel_TUG3.py
S2_2017_C6_ts_pixel_TUG4.py

Skripte zur Vorbereitung der Waldbranduntersuchung 2017 (S2_2017_D)
S2_2017_D1_ba_preprocessing.py
S2_2017_D2_ba_resampling.py
S2_2017_D3_ba_delete_redundant_files.py
S2_2017_D4_ba_rename_TCI_files.py
S2_2017_D5_ba_indices.py
S2_2017_D6_ba_SCL.py
S2_2017_D7_ba_differenced_indices.py
S2_2017_D8_ba_corine_clip.py

Skripte zu den pixelbasierten Berechnungen für die Waldbranduntersuchung 2017 (S2_2017_E)
S2_2017_E1_ba_pixel_NBRplus+BAIS2.py
S2_2017_E2_ba_pixel_NBRplus_EFFIS+intersect.py
S2_2017_E3_ba_pixel_NBRplus_final_EFFIS+intersect.py

Skript zur Darstellung aktiver Brände 2017 (S2_2017_F)
S2_2017_F1_fire_live_stack.py

Skript zur Vorverarbeitung der ERA5-Daten 2017 (S2_2017_G)
S2_2017_G1_ERA5_nc_to_csv.py

Skripte zur Vorbereitung der Trockenstressuntersuchung in den TUGen 2018 (S2_2018_B)
S2_2018_B1_ts_TUGe_preprocessing.py
S2_2018_B2_ts_TUGe_resampling.py
S2_2018_B3_ts_TUGe_delete_redundant_files.py
S2_2018_B4_ts_TUGe_SCL.py
S2_2018_B5_ts_TUGe_indices.py
S2_2018_B6_ts_corine_clip.py

Skripte zu den pixelbasierten Berechnungen für die Trockenstressuntersuchung 2018 (S2_2018_C)
S2_2018_C1_ts_indices_ranges.py
S2_2018_C2_ts_NMDI_ranges.py

Skripte zur Vorbereitung der Waldbranduntersuchung 2018 (S2_2018_D)
S2_2018_D1_ba_preprocessing.py
S2_2018_D2_ba_resampling.py
S2_2018_D3_ba_delete_redundant_files.py
S2_2018_D4_ba_rename_TCI_files.py
S2_2018_D5_ba_indices.py
S2_2018_D6_ba_SCL.py
S2_2018_D7_ba_differenced_indices.py
S2_2018_D8_ba_corine_clip.py

Skript zur Vorverarbeitung der ERA5-Daten 2018 (S2_2018_G)
S2_2018_G1_ERA5_nc_to_csv.py

