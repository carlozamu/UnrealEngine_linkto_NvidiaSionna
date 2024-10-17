import os
import unreal

# Funzione per importare un file OBJ in Unreal Engine
def import_obj_to_unreal(obj_file_path, destination_path):
    unreal.log(f"DEBUG: Inizio importazione del file OBJ in Unreal Engine: {obj_file_path}")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.FbxFactory()
    import_options = unreal.FbxImportUI()

    # Configura le opzioni di importazione
    import_options.set_editor_property('automated_import_should_detect_type', False)
    import_options.set_editor_property('import_mesh', True)
    import_options.set_editor_property('import_textures', False)
    import_options.set_editor_property('import_materials', False)
    import_options.set_editor_property('import_as_skeletal', False)

    # Configura il task di importazione
    obj_import_task = unreal.AssetImportTask()
    obj_import_task.set_editor_property('filename', obj_file_path)
    obj_import_task.set_editor_property('destination_path', destination_path)
    obj_import_task.set_editor_property('factory', factory)
    obj_import_task.set_editor_property('options', import_options)
    obj_import_task.set_editor_property('save', True)
    obj_import_task.set_editor_property('replace_existing', True)
    obj_import_task.set_editor_property('automated', True)

    unreal.log(f"DEBUG: Esecuzione del task di importazione")
    # Esegui l'importazione
    asset_tools.import_asset_tasks([obj_import_task])
    imported_asset_paths = obj_import_task.get_editor_property('imported_object_paths')
    if imported_asset_paths:
        imported_asset = imported_asset_paths[0]
        unreal.log(f"DEBUG: File OBJ importato in Unreal Engine: {imported_asset}")
        return imported_asset
    else:
        unreal.log_error("ERRORE: Errore durante l'importazione del file OBJ.")
        return None

# Funzione per posizionare un asset nella scena
def place_asset_in_scene(asset_path, location):
    unreal.log(f"DEBUG: Inizio posizionamento dell'asset nella scena: {asset_path}")
    world = unreal.EditorLevelLibrary.get_editor_world()
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset:
        unreal.log_error(f"ERRORE: Impossibile caricare l'asset {asset_path}")
        return
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, unreal.Vector(*location))
    
    # Imposta la scala dell'attore
    actor.set_actor_scale3d(unreal.Vector(40, 40, 40))
    
    # Imposta la rotazione dell'attore
    actor.set_actor_rotation(unreal.Rotator(90, 0, 0), False)  # Imposta teleport_physics a False
    
    unreal.log(f"DEBUG: Asset posizionato nella scena: {actor}")
    return actor

# Funzione principale
def main():
    # Ottieni il percorso del progetto Unreal
    project_content_dir = unreal.Paths.project_content_dir()
    python_scripts_path = os.path.join(project_content_dir, 'PythonScripts')

    # Percorso del file OBJ
    obj_file_relative_path = 'Radio_Anten_01.obj'
    obj_file_path = os.path.join(python_scripts_path, obj_file_relative_path)
    destination_path = '/Game/ImportedAssets'

    # Ottieni la posizione dell'attore (sostituisci con la posizione effettiva se disponibile)
    attore_position = [-2900, 2500, 1350]

    unreal.log(f"DEBUG: Percorso del file OBJ: {obj_file_path}")
    unreal.log(f"DEBUG: Destinazione dell'asset in Unreal Engine: {destination_path}")

    # Importa il file OBJ
    asset_path = import_obj_to_unreal(obj_file_path, destination_path)

    # Posiziona l'asset nella scena se l'importazione è riuscita
    if asset_path:
        unreal.log(f"DEBUG: Inizio posizionamento dell'asset nella scena")
        place_asset_in_scene(asset_path, attore_position)
    else:
        unreal.log_error("ERRORE: Impossibile posizionare l'asset nella scena a causa di un errore di importazione.")
  
        
if __name__ == "__main__":
    main()