import csv
import os
import unreal

def convert_obj_to_csv(obj_file_path, csv_file_path):
    # Verifica che il file OBJ esista
    if not os.path.exists(obj_file_path):
        unreal.log_error(f"Il file {obj_file_path} non esiste.")
        return

    with open(obj_file_path, 'r') as obj_file:
        lines = obj_file.readlines()
        
    rows = []
    index = 0
    
    for line in lines:
        if line.startswith('v'):
            parts = line.split()
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            # Applica la riflessione sull'asse Y
            y = -y
            rows.append([index, x, y, z])
            index += 1
    
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['index', 'x', 'y', 'z'])  # Headers with index
            writer.writerows(rows)
        
        unreal.log(f"File salvato come {csv_file_path}")
    except Exception as e:
        unreal.log_error(f"Errore durante il salvataggio del file CSV: {e}")

def main():
    # Ottieni il percorso del progetto Unreal
    project_content_dir = unreal.Paths.project_content_dir()
    python_scripts_path = os.path.join(project_content_dir, 'PythonScripts')
    
    # Definisci i percorsi relativi
    obj_file_path = os.path.join(python_scripts_path, 'visualized_paths.obj')
    csv_file_path = os.path.join(python_scripts_path, 'converted_paths.csv')
    
    # Log dei percorsi per il debug
    unreal.log(f"Percorso del file OBJ: {obj_file_path}")
    unreal.log(f"Percorso del file CSV: {csv_file_path}")

    convert_obj_to_csv(obj_file_path, csv_file_path)

if __name__ == "__main__":
    main()
