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

start_position = Position(xy=(50.0, 0.0), psi=3.14/2)
goal_position  = Position(xy=(-50.0, 0.0))

SOURCE_DIRECTORY = os.environ["SOURCE_DIRECTORY"]
SUMO_CONFIG_DIRECTORY = os.environ["SUMO_CONFIG_DIRECTORY"]
SUMO_CONFIG_FILE = os.environ["SUMO_CONFIG_FILE"]
SUMO_CONFIG_PATH = os.path.join(SOURCE_DIRECTORY, SUMO_CONFIG_DIRECTORY, SUMO_CONFIG_FILE)

def generate_launch_description():
    return LaunchDescription([
        *create_visualizer(
            whitelist=["ego_vehicle"],
            visualization_offset=start_position.get_utm_coordinates(),
        ),
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_pose_utm=start_position.get_utm_coordinates(),
            goal_position_utm=goal_position.get_utm_coordinates(),
            vehicle_id=111,
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
               {"sumo_config_file": SUMO_CONFIG_PATH},
               {"use_gui": True} 
            ],
        ),
    ])
