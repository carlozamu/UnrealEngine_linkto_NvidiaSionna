import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unreal
from sionna.rt import load_scene, Transmitter, Receiver, PlanarArray, CoverageMap, Camera

def configure_tensorflow(gpu_num=0):
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_num}"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_memory_growth(gpus[0], True)
        except RuntimeError as e:
            print(f"ERRORE: {e}")
    else:
        print("Nessuna GPU disponibile, uso della CPU.")
    tf.get_logger().setLevel('ERROR')

def get_player_start_position():
    editor_level_library = unreal.EditorLevelLibrary
    all_actors = editor_level_library.get_all_level_actors()
    player_start_actor = None
    for actor in all_actors:
        if actor.get_fname() == "PlayerStart_0":
            player_start_actor = actor
            break

    if player_start_actor:
        actor_location = player_start_actor.get_actor_location()
        return actor_location
    else:
        unreal.log_error("PlayerStart_0 not found in the scene.")
        return None

def get_actor_position(actor_label):
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = editor_actor_subsystem.get_all_level_actors()
    target_actor = None
    for actor in all_actors:
        if actor.get_actor_label() == actor_label:
            target_actor = actor
            break

    if target_actor:
        actor_location = target_actor.get_actor_location()
        return actor_location
    else:
        unreal.log_error(f"{actor_label} not found in the scene.")
        return None

def setup_scene(xml_path, tx_position, rx_position):
    scene = load_scene(xml_path)

    for obj in scene.objects:
        if isinstance(obj, str):
            continue
        if not hasattr(obj, 'name') or not hasattr(obj, 'material'):
            continue

    known_materials = ["itu_marble", "itu_metal", "itu_concrete"]

    for obj in scene.objects:
        if hasattr(obj, 'material'):
            material = getattr(obj, 'material', 'N/A')
            if material not in known_materials:
                obj.material = "itu_concrete"

    scene.tx_array = PlanarArray(num_rows=1,
                                 num_cols=1,
                                 vertical_spacing=0.5,
                                 horizontal_spacing=0.5,
                                 pattern="tr38901",
                                 polarization="V")

    scene.rx_array = PlanarArray(num_rows=1,
                                 num_cols=1,
                                 vertical_spacing=0.5,
                                 horizontal_spacing=0.5,
                                 pattern="dipole",
                                 polarization="cross")

    tx = Transmitter(name="tx", position=tx_position)
    scene.add(tx)

    rx = Receiver(name="rx", position=rx_position, orientation=[0, 0, 0])
    scene.add(rx)

    tx.look_at(rx)

    scene.frequency = 2.14e9
    scene.synthetic_array = True

    return scene

def compute_and_export_paths(scene, filename, max_depth=1, num_samples=1e6):
    paths = scene.compute_paths(max_depth=max_depth, num_samples=num_samples)
    paths.export(filename)

def process_coverage_map(cm, python_scripts_path):
    cell_centers = cm.cell_centers.numpy().reshape(-1, 3)
    coverage_values = cm.as_tensor().numpy().ravel()

    non_zero_coverage_mask = coverage_values > 0
    coverage_values = coverage_values[non_zero_coverage_mask]
    cell_centers = cell_centers[non_zero_coverage_mask]

    coverage_values_db = 10 * np.log10(coverage_values)
    coverage_values_db = np.round(coverage_values_db, 1)
    cell_centers = np.round(cell_centers, 1)
    cell_centers[:, 1] = -cell_centers[:, 1]

    data = {
        'index': range(len(coverage_values_db)),
        'x': cell_centers[:, 0],
        'y': cell_centers[:, 1],
        'z': cell_centers[:, 2],
        'coverage_db': coverage_values_db
    }
    df = pd.DataFrame(data)

    csv_path = os.path.join(python_scripts_path, 'coverage_map.csv')
    df.to_csv(csv_path, index=False)

    coverage_data = cm.as_tensor().numpy()[0, :, :]

    vmin = np.log10(coverage_data[coverage_data > 0].min() + 1e-15)
    vmax = np.log10(coverage_data.max() + 1e-15)
    log_coverage_data = np.log10(coverage_data + 1e-15)

    fig, ax = plt.subplots(figsize=(20, 20))
    cax = ax.imshow(log_coverage_data, cmap='viridis', origin='lower', vmin=vmin, vmax=vmax, interpolation='bilinear')
    ax.axis('off')
    cbar = fig.colorbar(cax)
    cbar.remove()

    image_save_path = os.path.join(python_scripts_path, 'coverage_map_high_res.png')
    plt.savefig(image_save_path, dpi=600, bbox_inches='tight', pad_inches=0)
    plt.close()

def create_2d_coverage_map(scene, cm, python_scripts_path):
    try:
        bird_pos = np.array(scene.transmitters["tx"].position).copy()
        bird_pos[-1] += 1000
        bird_pos[-2] -= 0.01

        tx_pos = scene.transmitters["tx"].position

        bird_cam = Camera("birds_view", position=bird_pos, look_at=tx_pos)
        scene.add(bird_cam)

        scene.render(camera="birds_view", coverage_map=cm, num_samples=512, resolution=[1920, 1080])

        # Generate plot using the _value attribute of the CoverageMap object
        coverage_data = cm._value[0, :, :]

        # Calculate log10 of coverage data for better visualization
        log_coverage_data = 10 * np.log10(coverage_data + 1e-15)

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 10))
        cax = ax.imshow(log_coverage_data, cmap='viridis', origin='lower', vmin=-150, vmax=-70)
        ax.set_xlabel('Cell index (X-axis)')
        ax.set_ylabel('Cell index (Y-axis)')
        cbar = fig.colorbar(cax, ax=ax)
        cbar.set_label('Path gain [dB]')

        # Save the plot
        image_save_path_2d = os.path.join(python_scripts_path, 'coverage_map_2d.png')
        plt.savefig(image_save_path_2d, format='png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"ERROR: {e}")


def main(*args):
    configure_tensorflow(gpu_num=0)

    python_scripts_path = os.path.dirname(os.path.realpath(__file__))
    xml_path = os.path.join(python_scripts_path, 'Mappa.xml')

    tx_position_actor = get_actor_position("Radio_Anten_01")
    if tx_position_actor:
        tx_position = [
            round(tx_position_actor.x / 100, 3),
            round(tx_position_actor.y / -100, 3),
            round((tx_position_actor.z + 300) / 100, 3)
        ]
    else:
        print("ERROR: Radio_Anten_01 non trovato nella scena.")
        return

    player_start_position = get_player_start_position()
    if player_start_position:
        rx_position = [
            round(player_start_position.x / 100, 3),
            round(player_start_position.y / -100, 3),
            round(player_start_position.z / 100, 3)
        ]
    else:
        print("ERROR: PlayerStart non trovato nella scena.")
        return

    output_path = os.path.join(python_scripts_path, 'visualized_paths.obj')

    scene = setup_scene(xml_path, tx_position, rx_position)
    compute_and_export_paths(scene, output_path)

    try:
        cm = scene.coverage_map()
    except AttributeError:
        print("ERROR: La scena non contiene un oggetto coverage_map.")
        return

    process_coverage_map(cm, python_scripts_path)
    create_2d_coverage_map(scene, cm, python_scripts_path)

if __name__ == "__main__":
    main()
