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
from launch_ros.actions import Node

import sys
import os
sys.path.append(os.path.dirname(__file__))

from position import Position
from simulated_vehicle import create_simulated_vehicle
from visualizer import create_visualizer

SOURCE_DIRECTORY      = os.environ["SOURCE_DIRECTORY"]
SUMO_CONFIG_DIRECTORY = os.environ["SUMO_CONFIG_DIRECTORY"]
SUMO_CONFIG_PATH      = os.path.join(SOURCE_DIRECTORY, SUMO_CONFIG_DIRECTORY, "example_scenario/osm.sumocfg")
GUI_SETTINGS_PATH     = os.path.join(SOURCE_DIRECTORY, SUMO_CONFIG_DIRECTORY, "gui_settings.xml")

EGO_START      = Position(lat_long=(52.314366, 10.537373), psi=2.748)
EGO_VEHICLE_ID = 111

def generate_launch_description():
    ego_utm = EGO_START.get_utm_coordinates()  # (x, y, zone, hemisphere, psi)
    ego_lat, ego_lon, ego_psi = EGO_START.get_lat_long_coordinates()
    return LaunchDescription([
        *create_visualizer(
            whitelist=["ego_vehicle"],
            visualization_offset=ego_utm,
        ),
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_pose_utm=ego_utm,
            goals=[(604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 0),  # CONTINUE
                   (604633, 5797104, 0),  # CONTINUE
                   (604730, 5797121, 1),  # STOP
                  ],
            vehicle_id=EGO_VEHICLE_ID,
            v2x_id=EGO_VEHICLE_ID,
        ),
        Node(
            package='sumo_bridge',
            namespace='ego_vehicle',
            executable='sumo_bridge',
            name='sumo_bridge',
            output='screen',
            parameters=[
                {"sumo_config_file":           SUMO_CONFIG_PATH},
                {"use_gui":                    True},
                {"gui_settings_file":          GUI_SETTINGS_PATH},
                {"gui_zoom":                   5000.0},
                {"gui_follow_ego":             True},
                {"ego_tracking_id":            EGO_VEHICLE_ID},
                {"ego_vehicle_color":          "255,255,255"},
                {"ego_start_position":         f"{ego_lat},{ego_lon},{ego_psi}"},
                {"initial_traffic_count":      20},
                {"initial_traffic_spacing":    10.0},
                {"initial_traffic_veh_type":   "veh_passenger"},
            ],
        ),
    ])
