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
sys.path.append(os.path.dirname(__file__)) # this line is very importatnt to find the helper functions

from position import Position
from simulated_vehicle import create_simulated_vehicle
from simulated_infrastructure import create_simulated_infrastructure
from visualizer import create_visualizer

def generate_launch_description():
    return LaunchDescription([
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_pose_utm=Position(lat_long=(52.314331, 10.53793), psi=3.14).get_utm_coordinates(),
            goal_position_utm=Position(lat_long=(52.314279, 10.54017), psi=0.0).get_utm_coordinates(),
            vehicle_id=111,
            v2x_id=111,
        ),
        *create_simulated_vehicle(
            namespace="second_vehicle",
            start_pose_utm=Position(lat_long=(52.314319, 10.536283), psi=0.0).get_utm_coordinates(),
            goal_position_utm=Position(lat_long=(52.314937, 10.537309), psi=0.0).get_utm_coordinates(),
            vehicle_id=222,
            v2x_id=222,
        ),
        *create_simulated_vehicle(
            namespace="third_vehicle",
            start_pose_utm=Position(lat_long=(52.314984, 10.53725), psi=-1.8).get_utm_coordinates(),
            goal_position_utm=Position(lat_long=(52.314937, 10.537309), psi=0.0).get_utm_coordinates(),
            vehicle_id=333,
            v2x_id=333,
        ),
        *create_simulated_infrastructure(
            infrastructure_position_utm=Position(lat_long=(52.314486, 10.537275), psi=0.0).get_utm_coordinates(),
            polygon_utm=[
                Position(lat_long=(52.31432, 10.536243), psi=0.0).get_utm_coordinates(),
                Position(lat_long=(52.314778, 10.536259), psi=0.0).get_utm_coordinates(),
                Position(lat_long=(52.314763, 10.537417), psi=0.0).get_utm_coordinates(),
                Position(lat_long=(52.314304, 10.537401), psi=0.0).get_utm_coordinates(),
            ],
        ),
        *create_visualizer(
            whitelist=["infrastructure"],
            visualization_offset=Position(lat_long=(52.315849, 10.562169), psi=0.0).get_utm_coordinates(),
        )
    ])
