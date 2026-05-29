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
SUMO_CONFIG_FILE      = os.environ["SUMO_CONFIG_FILE"]
SUMO_CONFIG_PATH      = os.path.join(SOURCE_DIRECTORY, SUMO_CONFIG_DIRECTORY, SUMO_CONFIG_FILE)
GUI_SETTINGS_PATH     = os.path.join(SOURCE_DIRECTORY, SUMO_CONFIG_DIRECTORY, "gui_settings.xml")

EGO_START      = Position(xy=(50.0, 0.0), psi=3.14/2)
EGO_GOAL       = Position(xy=(-50.0, 0.0))
EGO_VEHICLE_ID = 111

def generate_launch_description():
    ego_utm = EGO_START.get_utm_coordinates()  # (x, y, zone, hemisphere, psi)
    return LaunchDescription([
        *create_visualizer(
            whitelist=["ego_vehicle"],
            visualization_offset=ego_utm,
        ),
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_pose_utm=ego_utm,
            goals=[(-50.0, 0.0, 1)],
            vehicle_id=EGO_VEHICLE_ID,
            v2x_id=0,
            map_file='circle50m.xodr',
        ),
        Node(
            package='sumo_bridge',
            namespace='ego_vehicle',
            executable='sumo_bridge',
            name='sumo_bridge',
            output='screen',
            parameters=[
                {"sumo_config_file":   SUMO_CONFIG_PATH},
                {"use_gui":            True},
                {"gui_settings_file":  GUI_SETTINGS_PATH},
                {"gui_zoom":           100.0},
                {"gui_follow_ego":     False},
                {"ego_tracking_id":    EGO_VEHICLE_ID},
                {"ego_vehicle_color":     "255,255,255"},
                {"use_geo_conversion": False},
                {"utm_zone":           ego_utm[2]},
                {"utm_letter":         ego_utm[3]},
            ],
        ),
    ])
