from launch import LaunchDescription
from launch_ros.actions import Node
import os
from scenario_helpers.simulated_vehicle import create_simulated_vehicle_nodes
from scenario_helpers.simulated_infrastructure import create_infrastructure_nodes
from scenario_helpers.visualizer import create_visualization_nodes


def generate_launch_description():
    launch_file_dir = os.path.dirname(os.path.realpath(__file__))
    map_image_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/maps/"))
    map_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/tracks/"))
    vehicle_param = os.path.abspath(os.path.join(launch_file_dir, "../assets/vehicle_params/"))
    map_file = map_folder + "/de_bs_borders_wfs.r2sr"
    vehicle_model_file = vehicle_param + "/NGC.json"

    return LaunchDescription([
        # ================ visualization ==================
        *create_visualization_nodes(
            whitelist=["ego_vehicle", "sim_vehicle_1", "sim_vehicle_2", "infrastructure"],
            asset_folder=map_image_folder,
            use_center_ego=False,
            ns="infrastructure"
        ),
        # ================ Infrastructure ===================
        *create_infrastructure_nodes(
            position=(604790.5, 5797129.8),
            polygon=[
                604750.5, 5797109.8,
                604750.5, 5797160.8,
                604799.5, 5797160.8,
                604799.5, 5797109.8
            ],
            map_file=map_file
        ),
        # ================ Vehicles ========================
        *create_simulated_vehicle_nodes(
            namespace="ego_vehicle",
            start_pose=(604835.481, 5797113.518, 3.14),
            goal_position=(604988.297, 5797111.0),
            vehicle_id=111,
            v2x_id=111,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0)
        ),

        *create_simulated_vehicle_nodes(
            namespace="sim_vehicle_1",
            start_pose=(604731.230, 5797112.750, 0.0),
            goal_position=(604791.7, 5797180.0),
            vehicle_id=222,
            v2x_id=222,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0)
        ),

        *create_simulated_vehicle_nodes(
            namespace="sim_vehicle_2",
            start_pose=(604787.6, 5797185.2, -1.8),
            goal_position=(604791.7, 5797180.0),
            vehicle_id=333,
            v2x_id=333,
            model_file=vehicle_model_file,
            map_file=map_file,
            shape=(4.5, 2.0, 2.0)
        ),
    ])
