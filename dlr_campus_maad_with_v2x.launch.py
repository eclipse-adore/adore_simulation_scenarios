from launch import LaunchDescription
from launch_ros.actions import Node  # kept in case you add extras later
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)


def generate_launch_description():
    # Match the first file: import helpers inside the function
    from scenario_helpers.visualizer import create_visualization_nodes
    from scenario_helpers.simulated_infrastructure import create_infrastructure_nodes
    from scenario_helpers.simulated_vehicle import create_simulated_vehicle_nodes

    launch_file_dir = os.path.dirname(os.path.realpath(__file__))
    map_image_folder = os.path.abspath(
        os.path.join(launch_file_dir, "../assets/maps/")
    )
    map_folder = os.path.abspath(
        os.path.join(launch_file_dir, "../assets/tracks/")
    )
    vehicle_param = os.path.abspath(
        os.path.join(launch_file_dir, "../assets/vehicle_params/")
    )

    map_file = map_folder + "/de_bs_borders_wfs.r2sr"
    vehicle_model_file = vehicle_param + "/VC2.json"

    # Follow the first file’s pattern (switch to True if you want simulated V2X wiring)
    simulated_v2x_mode = True

    return LaunchDescription([
        # ================ visualization ==================
        *create_visualization_nodes(
            whitelist=["infrastructure", "ego_vehicle",
                       "sim_vehicle_1", "sim_vehicle_2"],
            asset_folder=map_image_folder,
            visualization_offset=(606453.910, 5797315.369),
        ),
        Node(
            package='adore_v2x_interface',
            namespace='ego_vehicle',
            executable='ego_v2x_interface_node',
            name='ego_v2x_interface',
            parameters=[
                {"ego_v2x_id": 222},
                {"cam_out_topic": "/CAM"},
                {"epu_in_topic": "/EPU"},
            ],
        ),
        Node(
            package='adore_v2x_interface',
            namespace='infrastructure',
            executable='infrastructure_v2x_interface_node',
            name='infra_v2x_interface',
            parameters=[
                {"cam_in_topic": "/CAM"},
                {"epu_out_topic": "/EPU"},
            ],
        ),

        # ================ Infrastructure ===================
        *create_infrastructure_nodes(
            position=(606453.910, 5797315.369),
            polygon=[
                606438.850, 5797325.544,
                606477.292, 5797323.258,
                606478.079, 5797312.037,
                606455.904, 5797299.986,
                606443.210, 5797300.491,
            ],
            map_file=map_file,
            simulated_v2x_mode=simulated_v2x_mode
        ),

        # ================ Vehicles =========================
        *create_simulated_vehicle_nodes(
            namespace="ego_vehicle",
            start_pose=(606425.120, 5797326.700, 0.0),
            goal_position=(606532.605, 5797313.325),
            vehicle_id=111,
            v2x_id=111,
            simulated_v2x_mode=simulated_v2x_mode,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0),
            controller=0,
            composable=False
        ),

        *create_simulated_vehicle_nodes(
            namespace="sim_vehicle_1",
            start_pose=(606451.140, 5797285.841, 3.14 / 2.0),
            goal_position=(606532.605, 5797313.325),
            vehicle_id=222,
            v2x_id=222,
            simulated_v2x_mode=simulated_v2x_mode,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0),
            controller=0,
            composable=False
        ),

        *create_simulated_vehicle_nodes(
            namespace="sim_vehicle_2",
            start_pose=(606497.528, 5797318.186, -3.14),
            goal_position=(606449.144, 5797290.938),
            vehicle_id=333,
            v2x_id=333,
            simulated_v2x_mode=simulated_v2x_mode,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0),
            controller=0,
            composable=False
        ),
    ])
