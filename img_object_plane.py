import os
import unreal

def import_texture(texture_source_path, destination_path):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Check if the texture is already in the destination path
    texture_name = texture_source_path.split('/')[-1].split('.')[0]
    existing_texture = unreal.EditorAssetLibrary.load_asset(f'{destination_path}/{texture_name}')

    if existing_texture:
        # Delete the existing texture if present
        unreal.EditorAssetLibrary.delete_asset(existing_texture.get_path_name())

    # Import the texture
    task = unreal.AssetImportTask()
    task.filename = texture_source_path
    task.destination_path = destination_path
    task.automated = True
    task.save = True

    asset_tools.import_asset_tasks([task])

    # Check if the asset was imported successfully
    if task.imported_object_paths:
        imported_asset_path = task.imported_object_paths[0]
        texture = unreal.EditorAssetLibrary.load_asset(imported_asset_path)
        if texture:
            return texture
        else:
            unreal.log_error(f"Failed to load imported texture from {imported_asset_path}")
            return None
    else:
        unreal.log_error(f"Failed to import texture from {texture_source_path}")
        return None

def create_or_get_material(texture, material_name):
    material_path = f'/Game/Materials/{material_name}'
    material = unreal.EditorAssetLibrary.load_asset(material_path)
    
    if not material:
        material_factory = unreal.MaterialFactoryNew()
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(material_name, '/Game/Materials', unreal.Material, material_factory)
    
    material_editor = unreal.MaterialEditingLibrary
    texture_sample_node = material_editor.create_material_expression(material, unreal.MaterialExpressionTextureSample)
    texture_sample_node.texture = texture
    material_editor.connect_material_property(texture_sample_node, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
    
    unreal.EditorAssetLibrary.save_asset(material.get_path_name())
    material_editor.recompile_material(material)
    
    return material

def replace_material_on_actor(actor_name, target_material_name, new_material):
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_subsystem.get_all_level_actors()
    
    for actor in actors:
        if actor.get_actor_label() == actor_name:
            static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
            if static_mesh_component:
                materials = static_mesh_component.get_materials()
                for i, material in enumerate(materials):
                    if material.get_name() == target_material_name or material.get_name() == "M_CoverageMap":
                        static_mesh_component.set_material(i, new_material)
                        actor.modify()
                        return True
            else:
                unreal.log_error(f"L'attore {actor_name} non ha un componente StaticMesh.")
            return False
    
    unreal.log_error(f"L'attore {actor_name} non è stato trovato nella scena")
    return False

# Ottieni il percorso del progetto Unreal
project_content_dir = unreal.Paths.project_content_dir()
python_scripts_path = os.path.join(project_content_dir, 'PythonScripts')
textures_path = os.path.join(python_scripts_path, 'coverage_map_high_res.png')

# Percorsi relativi
texture_source_path = textures_path
texture_destination_path = '/Game/Textures'
material_name = 'M_CoverageMap'
actor_name = 'Mappa'
target_material_name = 'itu_concrete'

# Import texture, create material and apply it to the specified material slot on the actor
texture = import_texture(texture_source_path, texture_destination_path)
if texture:
    material = create_or_get_material(texture, material_name)
    success = replace_material_on_actor(actor_name, target_material_name, material)

    if success:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
        unreal.log(f"Material {target_material_name} on actor {actor_name} successfully replaced with new material.")
