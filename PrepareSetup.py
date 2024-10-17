import unreal

def open_level(level_name, level_path):
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

    # Build the full path to the level
    full_level_path = f"{level_path}/{level_name}.{level_name}"
    
    # Check if the level exists
    if unreal.EditorAssetLibrary.does_asset_exist(full_level_path):
        # Load the level
        level_editor_subsystem.load_level(full_level_path)
        unreal.log(f"Successfully loaded level: {full_level_path}")
    else:
        unreal.log_error(f"Level {level_name} not found at path: {level_path}")

def main():
    level_name = "Start"
    level_path = "/Game"
    open_level(level_name, level_path)

if __name__ == "__main__":
    main()
