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

from launch_ros.actions import Node
from typing import List, Optional, Tuple

import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

def create_visualizer(
    whitelist: List[str],
    visualization_offset: Tuple[float, float, int, str, float],
    ns: str = "visualizer",
    use_center_ego: bool = True,
    port: int = 9090,
) -> list:
    """
    Returns a list of nodes for visualization (rosbridge, rosapi and visualizer).

    Args:
        whitelist: List of namespaces to display.
        asset_folder: Path to the map image folder.
        visualization_offset: Accepted for API compatibility but unused by the
            installed visualizer package.
        ns: Namespace for the visualizer node.
        use_center_ego: Whether the visualizer centers on the ego vehicle.
        port: Port for rosbridge WebSocket server.
    """
    return [
        Node(
            package="rosapi",
            executable="rosapi_node",
            name="rosapi",
            output="screen",
        ),
        Node(
            package="rosbridge_server",
            executable="rosbridge_websocket",
            name="rosbridge_websocket",
            output="screen",
            parameters=[
                {"port": port},
                {"address": "0.0.0.0"},
                {"use_compression": False},
                {"fragment_timeout": 600},
                {"delay_between_messages": 0.0},
                {"max_message_size": 10000000},
                {"unregister_timeout": 10.0},
            ],
        ),
        Node(
            package="visualizer",
            executable="visualizer",
            name="visualizer",
            namespace=ns,
            parameters=[
                {"whitelist": whitelist},
                {"visualization_offset_x": visualization_offset[0]},
                {"visualization_offset_y": visualization_offset[1]},
            ],
        ),
    ]
