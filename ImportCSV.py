import unreal
import os

def reimport_data_table(data_table_path, csv_file_path):
    # Trova l'asset della data table
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

def main():
    # Ottieni il percorso del progetto Unreal
    project_content_dir = unreal.Paths.project_content_dir()
    python_scripts_path = os.path.join(project_content_dir, 'PythonScripts')

    # Percorsi dell'asset della data table e del file CSV
    data_table_path = '/Game/converted_paths'
    csv_file_path = os.path.join(python_scripts_path, 'converted_paths.csv')

    # Esegui la reimportazione
    reimport_data_table(data_table_path, csv_file_path)

if __name__ == "__main__":
    main()
