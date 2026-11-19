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
#
# vehicle side only, the pipeline runs separately
from launch import LaunchDescription

import sys
import os
sys.path.append(os.path.dirname(__file__))

from position import Position, Waypoint, WaypointBehavior
from simulated_vehicle import create_simulated_vehicle
from visualizer import create_visualizer

# campus road, southbound
start_position = Position(lat_long=(52.315849, 10.562169), psi=0.0)
goal_positions = [
    Waypoint(Position(utm=(606438.66, 5797159.46, 32, "U")), WaypointBehavior.STOP),
]

# x, y, label - on straight sections of the route
virtual_stops = [
    (606511.45, 5797314.30, "haltestelle_1"),
    (606484.89, 5797239.29, "haltestelle_2"),
    (606441.40, 5797190.10, "haltestelle_3"),
]


def generate_launch_description():
    return LaunchDescription([
        *create_simulated_vehicle(
            namespace="ego_vehicle",
            start_position_utm=start_position.get_utm_coordinates(),
            goals=goal_positions,
            vehicle_id=111,
            v2x_id=0,
            virtual_stops=virtual_stops,
        ),
        *create_visualizer(
            whitelist=["ego_vehicle"],
            visualization_offset=start_position.get_utm_coordinates(),
        ),
    ])
