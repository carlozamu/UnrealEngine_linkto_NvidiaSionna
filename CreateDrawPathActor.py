import unreal

def spawn_draw_path_actor():
    # Percorso della classe Blueprint
    blueprint_path = "/Game/DrawPath"
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(blueprint_path)

    if not actor_class:
        unreal.log_error(f"Blueprint class '{blueprint_path}' non trovata.")
        return False

    # Ottenere il mondo dell'editor
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    
    # Controllare se esiste già un attore DrawPath nel mondo
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in all_actors:
        if actor.get_class() == actor_class:
            unreal.log("DrawPath actor esiste già nel mondo.")
            return True

    # Specifica la posizione e la rotazione dell'attore
    actor_location = unreal.Vector(0.0, 0.0, 0.0)
    actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    # Piazzare l'attore nella scena
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, actor_location, actor_rotation)

    if not actor:
        unreal.log_error("Attore non è stato creato.")
        return False

    unreal.log("DrawPath actor creato con successo.")
    return True

# Esegui la funzione
spawn_draw_path_actor()
