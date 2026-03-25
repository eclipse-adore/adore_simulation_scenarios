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
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from launch import Action
from launch_ros.actions import Node

import sys
import os
import utm

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

def create_visualizer(
    whitelist: [str],
    visualization_offset_lat_lon: Tupple[float, float],
) -> List[Action]:

    visualization_offset_utm_x, visualization_offset_utm_y, visualization_offset_utm_zone_number, visualization_offset_utm_zone_letter = utm.from_latlon(visualization_offset_lat_lon[0], visualization_offset_lat_lon[1])

    return [
        Node(
            package='rosapi',
            executable='rosapi_node',
            name='rosapi',
            output='screen'
        ),
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge_websocket',
            output='screen',
            parameters=[
                {'port': 9090},
                {'address': '0.0.0.0'},
                {'use_compression': False},
                {'fragment_timeout': 600},
                {'delay_between_messages': 0.0},
                {'max_message_size': 10000000},
                {'unregister_timeout': 10.0}
            ]
        ),
        Node(
            package='visualizer',
            namespace="visualizer",
            executable='visualizer',
            name='visualizer',
            parameters=[
                {"whitelist": whitelist},
                {"visualization_offset_x": float(visualization_offset_utm_x)},
                {"visualization_offset_y": float(visualization_offset_utm_y)},
            ]
        )
    ]