# ********************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
# ********************************************************************************

from launch import LaunchDescription
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
from scenario_helpers.simulated_vehicle import create_simulated_vehicle_nodes
from scenario_helpers.simulated_vehicle import Position
from scenario_helpers.visualizer import create_visualization_nodes
from launch_ros.actions import Node

start_position = Position(utm=(604862.7, 5797111.9, 32, 'N'), psi=0.0)
goal_position = Position(utm=(604988.3, 5797111.0, 32, 'N'))

def generate_launch_description():
    launch_file_dir = os.path.dirname(os.path.realpath(__file__))
    map_image_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/maps/"))
    map_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/tracks/"))
    vehicle_param = os.path.abspath(os.path.join(launch_file_dir, "../assets/vehicle_params/"))
    map_file = map_folder + "/de_bs_borders_wfs.r2sr"
    vehicle_model_file = vehicle_param + "/NGC.json"
    
    return LaunchDescription([
        *create_visualization_nodes(
            whitelist=["ego_vehicle"],
            asset_folder=map_image_folder,
            use_center_ego=True
        ),
        Node(
            package='simulated_remote_operator',
            namespace='ego_vehicle',
            executable='simulated_remote_operator',
            name='simulated_remote_operator',
        ),
        *create_simulated_vehicle_nodes(
            namespace="ego_vehicle",
            start_position=start_position,
            goal_position=goal_position,
            map_file=map_file,
            model_file=vehicle_model_file,
            controllable=True,
            v2x_id=0,
            vehicle_id=0,
            controller=1,
            debug=False,
            request_assistance_polygon=[ 
                                        604852.718,
                                        5797101.860,
                                        604872.718,
                                        5797101.860,
                                        604872.718,
                                        5797121.860,
                                        604852.718,
                                        5797121.860,
                                        ]
        )
    ])
