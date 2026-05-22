from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='foxglove_bridge',
            namespace='global',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen',
            parameters=[
                {'port': 8765},
            ],
        ),
        Node(
            package='visualizer',
            namespace='ego_vehicle',
            executable='visualizer',
            name='visualizer',
            parameters=[
                {"asset folder": os.path.abspath("../assets/maps/")}
            ]
        ),
        Node(
            package='simulated_vehicle',
            namespace='ego_vehicle',
            executable='simulated_vehicle',
            name='simulated_vehicle',
            parameters=[
                {"set_start_position_x": 1.0},
                {"set_start_position_y": -52.0},
                {"set_start_psi": 0.0},
                {"controllable": True},
                {"other_vehicle_namespaces": ["traffic_participant_2"]}
            ]
        ),
        Node(
            package='sumo_bridge',
            namespace='ego_vehicle',
            executable='sumo_bridge',
            name='sumo_bridge',
            output='screen',
            parameters=[
                {"sumo config file": "../assets/sumo/demo_sumo_bridge.sumocfg"}
            ]
        ),
        Node(
            package='decision_maker',
            namespace='ego_vehicle',
            executable='decision_maker',
            name='decision_maker',
            parameters=[
                {"debug_mode_active": False},
                {"optinlc_route_following": True}, # 0 for Lane following, 1 for OptiNLC route following
                {"planner_settings_keys": [ "wheel_base",
                                           "lateral_weight",
                                           "heading_weight",
                                           "maximum_velocity",
                                           "min_distance_to_vehicle_ahead",
                                           "look_ahead_for_curvature",
                                           "look_behind_for_curvature"]},
               {"planner_settings_values": [ 2.7,
                                               0.2,
                                               0.02,
                                               5.0,
                                               10.0,
                                               40.0,
                                               20.0]}
            ],
        ),
        Node(
            package='mission_control',
            namespace='ego_vehicle',
            executable='mission_control',
            name='mission_control',
            parameters=[
                {"R2S map file": os.path.abspath("../assets/tracks/circle50m.xodr")},
                {"goal_position_x" : 0.0},
                {"goal_position_y": 52.0}
            ]
        ),
       Node(
           package='trajectory_tracker',
           namespace='ego_vehicle',
           executable='trajectory_tracker_node',
           name='trajectory_tracker',
           parameters=[
               {"set_controller": 1}, # 0 for MPC, 1 for PID
               {"controller_settings_keys": [ "kp_x",
                                           "ki_x",
                                           "velocity_weight",
                                           "kp_y",
                                           "ki_y",
                                           "heading_weight",
                                           "kp_omega",
                                           "dt",
                                           "steering_comfort"]},

               {"controller_settings_values": [ 0.3,
                                               0.02,
                                               0.3,
                                               0.25,
                                               0.0,
                                               0.3,
                                               0.1,
                                               0.05,
                                               2.5]}
           ],
           #output={'both': 'log'},
       ),
    ]
)
