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

from position import Position, Waypoint, WaypointBehavior
from simulated_vehicle import create_simulated_vehicle
from simulated_infrastructure import create_simulated_infrastructure
from visualizer import create_visualizer

ego_start     = Position(lat_long=(52.314331, 10.53793),  psi=3.14)
second_start  = Position(lat_long=(52.314319, 10.536283), psi=0.0)
third_start   = Position(lat_long=(52.314984, 10.53725),  psi=-1.8)

ego_goal_positions = [
    Waypoint(Position(utm=(604988.29, 5797110.98, 32, "U")), WaypointBehavior.STOP),
]
second_goal_positions = [
    Waypoint(Position(utm=(604791.72, 5797180.02, 32, "U")), WaypointBehavior.STOP),
]
third_goal_positions = [
    Waypoint(Position(utm=(604791.72, 5797180.02, 32, "U")), WaypointBehavior.STOP),
]

infrastructure_position = Position(lat_long=(52.314486, 10.537275), psi=0.0)
infrastructure_polygon = [
    Position(lat_long=(52.31432,  10.536243)).get_utm_coordinates(),
    Position(lat_long=(52.314778, 10.536259)).get_utm_coordinates(),
    Position(lat_long=(52.314763, 10.537417)).get_utm_coordinates(),
    Position(lat_long=(52.314304, 10.537401)).get_utm_coordinates(),
]

visualizer_offset = Position(lat_long=(52.315849, 10.562169), psi=0.0)

def generate_launch_description():
    return LaunchDescription([
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_position_utm=ego_start.get_utm_coordinates(),
            goals=ego_goal_positions,
            vehicle_id=111,
            v2x_id=111,
        ),
        *create_simulated_vehicle(
            namespace="second_vehicle",
            start_position_utm=second_start.get_utm_coordinates(),
            goals=second_goal_positions,
            vehicle_id=222,
            v2x_id=222,
        ),
        *create_simulated_vehicle(
            namespace="third_vehicle",
            start_position_utm=third_start.get_utm_coordinates(),
            goals=third_goal_positions,
            vehicle_id=333,
            v2x_id=333,
        ),
        *create_simulated_infrastructure(
            infrastructure_position_utm=infrastructure_position.get_utm_coordinates(),
            polygon_utm=infrastructure_polygon,
        ),
        *create_visualizer(
            whitelist=["infrastructure"],
            visualization_offset=visualizer_offset.get_utm_coordinates(),
        )
    ])
