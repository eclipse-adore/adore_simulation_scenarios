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

start_position = Position(lat_long=(52.314572, 10.560468), psi=3.14)
#start_position = Position(utm=(606372, 5797172, 32, 'N'), psi=3.04)
goal_position = Position(lat_long=(52.314569, 10.560382))
#goal_position = Position(utm=(606380, 5797058, 32, 'N'))

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
        *create_simulated_vehicle_nodes(
            namespace="ego_vehicle",
            start_position=start_position,
            goal_position=goal_position,
            map_file=map_file,
            model_file=vehicle_model_file,
            controllable=True,
            optinlc_route_following=True,
            v2x_id=0,
            vehicle_id=0,
            controller=1,
            debug=False,
            composable=False
        )
    ])