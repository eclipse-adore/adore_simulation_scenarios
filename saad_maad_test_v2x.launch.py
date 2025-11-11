
from launch import LaunchDescription
from launch_ros.actions import Node
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)


def generate_launch_description():
    from scenario_helpers.visualizer import create_visualization_nodes
    from scenario_helpers.simulated_infrastructure import create_infrastructure_nodes
    from scenario_helpers.simulated_vehicle import create_simulated_vehicle_nodes
    launch_file_dir = os.path.dirname(os.path.realpath(__file__))
    map_image_folder = os.path.abspath(
        os.path.join(launch_file_dir, "../assets/maps/"))
    map_folder = os.path.abspath(os.path.join(
        launch_file_dir, "../assets/tracks/"))
    vehicle_param = os.path.abspath(os.path.join(
        launch_file_dir, "../assets/vehicle_params/"))
    map_file = map_folder + "/de_bs_borders_wfs.r2sr"
    vehicle_model_file = vehicle_param + "/NGC.json"

    simulated_v2x_mode = True

    infrastructure_pos = (604790.5, 5797129.8)

    return LaunchDescription([
        # ================ visualization ==================
        *create_visualization_nodes(
            whitelist=["infrastructure", "ego_vehicle",
                       "sim_vehicle_1", "sim_vehicle_2"],
            asset_folder=map_image_folder,
            visualization_offset=(604790.5, 5797129.8),
            ns="visualization",
        ),
        # ================ Infrastructure ===================
        *create_infrastructure_nodes(
            position=infrastructure_pos,
            polygon=[
                604720.5, 5797109.8,
                604720.5, 5797160.8,
                604799.5, 5797160.8,
                604799.5, 5797109.8
            ],
            map_file=map_file,
            simulated_v2x_mode=simulated_v2x_mode
        ),

        Node(
            package='adore_v2x_interface',
            namespace='infrastructure',
            executable='infrastructure_v2x_interface_node',
            name='infra_v2x_interface',
            parameters=[
                {"cam_in_topic": "/CAM"},
                {"epu_out_topic": "/EPU"},
                {"publish_v2x_tracked_boxes": True},
                {"infrastructure_utm_x": infrastructure_pos[0]},
                {"infrastructure_utm_y": infrastructure_pos[1]},
                {"max_trajectory_size": 16},
                {"trajectory_increment": 3}
            ],
        ),
        Node(
            package='adore_v2x_interface',
            namespace='infrastructure',
            executable='tracked_box_spammer_node',
            name='tracked_box_spammer',
            parameters=[
                {'rate_hz': 20.0},
                {'num_boxes': 100},
            ]
        ),


        # ================ Vehicles ========================x
        *create_simulated_vehicle_nodes(
            namespace="sim_vehicle_1",
            start_pose=(604835.481, 5797113.518, 3.14),
            goal_position=(604833.297, 5797110.0),
            vehicle_id=111,
            v2x_id=111,
            simulated_v2x_mode=simulated_v2x_mode,
            model_file=vehicle_model_file,
            map_file=map_file,
            controller=0,
            composable=False
        ),
        Node(
            package='adore_v2x_interface',
            namespace='sim_vehicle_1',
            executable='ego_v2x_interface_node',
            name='ego_v2x_interface',
            parameters=[
                {"cam_out_topic": "/CAM"},
                {"epu_in_topic": "/EPU"},
            ],
        ),

        *create_simulated_vehicle_nodes(
            namespace="ego_vehicle",
            start_pose=(604723.230, 5797109.750, 0.0),
            goal_position=(604791.7, 5797180.0),
            vehicle_id=222,
            v2x_id=222,
            simulated_v2x_mode=simulated_v2x_mode,
            model_file=vehicle_model_file,
            map_file=map_file,
            controller=0,
            composable=False,
            debug=False
        ),
        Node(
            package='adore_v2x_interface',
            namespace='ego_vehicle',
            executable='ego_v2x_interface_node',
            name='ego_v2x_interface',
            parameters=[
                {"cam_out_topic": "/CAM"},
                {"epu_in_topic": "/EPU"},

            ],
        ),

        # *create_simulated_vehicle_nodes(
        #     namespace="sim_vehicle_2",
        #     start_pose=(604787.6, 5797185.2, -1.8),
        #     goal_position=(604791.7, 5797180.0),
        #     vehicle_id=333,
        #     v2x_id=333,
        #     model_file=vehicle_model_file,
        #     map_file=map_file,

        #     controller=0,
        #     composable=False
        # ),
    ])
