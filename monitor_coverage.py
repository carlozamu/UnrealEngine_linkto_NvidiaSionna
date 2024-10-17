import unreal

def spawn_coverage_actor():
    # Percorso della Blueprint Class di CoverageActor
    blueprint_path = '/Game/CoverageActor.CoverageActor_C'
    
    # Carica la Blueprint Class
    blueprint_class = unreal.load_asset(blueprint_path)
    
    if not blueprint_class:
        unreal.log_error(f"Blueprint class '{blueprint_path}' non trovata.")
        return False

    # Ottieni il mondo dell'editor
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    
    # Controlla se un attore di questo tipo è già presente nella scena
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in actors:
        if actor.get_class() == blueprint_class:
            unreal.log("Coverage Actor esiste già nella scena.")
            return True
    
    # Specifica la posizione e la rotazione dell'attore
    actor_location = unreal.Vector(0.0, 0.0, 0.0)
    actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    # Piazzare l'attore nella scena
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(blueprint_class, actor_location, actor_rotation)

    if not actor:
        unreal.log_error("Attore non è stato creato.")
        return False

    unreal.log("Coverage Actor creato con successo.")
    return True

# Esegui la funzione per piazzare l'attore
spawn_coverage_actor()
