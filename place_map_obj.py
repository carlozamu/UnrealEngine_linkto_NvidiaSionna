import unreal
import os
def import_obj_to_unreal(obj_file_path, destination_path, asset_name):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Create an import task
    obj_import_task = unreal.AssetImportTask()
    obj_import_task.set_editor_property('filename', obj_file_path)
    obj_import_task.set_editor_property('destination_path', destination_path)
    obj_import_task.set_editor_property('destination_name', asset_name)
    obj_import_task.set_editor_property('save', True)
    obj_import_task.set_editor_property('replace_existing', True)
    obj_import_task.set_editor_property('automated', True)  # Avoid the confirmation prompt

    # Execute the import task
    asset_tools.import_asset_tasks([obj_import_task])

    # Verify and return the imported asset path
    imported_paths = obj_import_task.get_editor_property('imported_object_paths')
    for path in imported_paths:
        obj_asset = unreal.EditorAssetLibrary.load_asset(path)
        if isinstance(obj_asset, unreal.StaticMesh):
            unreal.log(f"File OBJ imported into Unreal Engine: {obj_asset.get_path_name()}")
            return obj_asset.get_path_name()

    unreal.log_error("OBJ file import failed or did not result in a StaticMesh.")
    return None

def place_obj_in_scene(obj_asset_path, location, scale):
    unreal.log(f"Placing object in the scene: {obj_asset_path}")
    obj_asset = unreal.EditorAssetLibrary.load_asset(obj_asset_path)

    if not obj_asset:
        unreal.log(f"Error: Unable to load asset {obj_asset_path}")
        return

    # Ensure the asset is a static mesh
    if isinstance(obj_asset, unreal.StaticMesh):
        # Place the object in the scene
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location)
        if actor:
            actor.set_actor_label("Mappa")
            static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
            if static_mesh_component:
                static_mesh_component.set_static_mesh(obj_asset)
                actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))

                # Set Collision Presets to NoCollision
                static_mesh_component.set_collision_profile_name('NoCollision')

                unreal.EditorLevelLibrary.save_current_level()
                unreal.log(f"Object placed in the scene: {actor} with scale {scale}.")
            else:
                unreal.log(f"Error: Unable to find StaticMeshComponent for actor {actor}.")
        else:
            unreal.log(f"Error: Unable to place asset {obj_asset_path} in the scene.")
    else:
        unreal.log(f"Error: The imported asset is not a StaticMesh. Asset type: {type(obj_asset)}")

def main():
    # Path to the OBJ file
    obj_file_relative_path = 'Mappa.obj'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    obj_file_path = os.path.join(script_dir, obj_file_relative_path)

    # Debug: verifica il percorso del file OBJ
    unreal.log(f"Percorso del file OBJ: {obj_file_path}")

    # Import the OBJ file
    destination_path = '/Game/Maps'
    asset_name = 'Mappa'
    obj_asset_path = import_obj_to_unreal(obj_file_path, destination_path, asset_name)

    # If the import was successful, place the object in the scene
    if obj_asset_path:
        location = unreal.Vector(0.0, 0.0, 0.0)  # Adjust this position as needed
        scale = 100.0  # Desired scale
        place_obj_in_scene(obj_asset_path, location, scale)

# Execute the main function if this file is run as a script
if __name__ == "__main__":
    main()