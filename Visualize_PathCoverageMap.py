import csv
import os
import unreal

def modify_csv_data(csv_file_path, output_folder):
    modified_csv_file_path = os.path.join(output_folder, 'coverage_map_modified.csv')
    
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Modifica i valori delle colonne x, y, z
    for row in rows:
        row['x'] = float(row['x']) * 100
        row['y'] = float(row['y']) * 100
        row['z'] = float(row['z']) * 100

    # Scrivi i dati modificati in un nuovo file CSV
    with open(modified_csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return modified_csv_file_path

def reimport_data_table(data_table_path, csv_file_path):
    # Trova l'asset della data table
    unreal.log(f"Tentativo di caricamento dell'asset della data table da: {data_table_path}")
    data_table_asset = unreal.EditorAssetLibrary.load_asset(data_table_path)

    if not data_table_asset:
        unreal.log_error(f"Data table {data_table_path} non trovata.")
        return False

    # Verifica che l'asset caricato sia una DataTable
    if not isinstance(data_table_asset, unreal.DataTable):
        unreal.log_error(f"L'asset {data_table_path} non è una DataTable.")
        return False

    # Leggi il contenuto del file CSV
    with open(csv_file_path, 'r') as csv_file:
        csv_content = csv_file.read()

    # Riempie la DataTable con i dati del CSV
    success = unreal.DataTableFunctionLibrary.fill_data_table_from_csv_string(data_table_asset, csv_content)

    if success:
        unreal.EditorAssetLibrary.save_loaded_asset(data_table_asset)
        unreal.log(f"Reimportazione della data table {data_table_path} completata con successo.")
        return True
    else:
        unreal.log_error(f"Reimportazione della data table {data_table_path} fallita.")
        return False

# Ottieni il percorso del progetto Unreal
project_content_dir = unreal.Paths.project_content_dir()
python_scripts_path = os.path.join(project_content_dir, 'PythonScripts')

# Percorsi dell'asset della data table e del file CSV
data_table_path = '/Game/coverage_map'  # Assicurati che il percorso sia corretto
original_csv_file_path = os.path.join(python_scripts_path, 'coverage_map.csv')  # Percorso del file CSV originale

# Modifica i valori del file CSV
modified_csv_file_path = modify_csv_data(original_csv_file_path, python_scripts_path)

# Esegui la reimportazione
reimport_data_table(data_table_path, modified_csv_file_path)
