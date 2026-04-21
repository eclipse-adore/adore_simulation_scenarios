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

import os
import sys
# import utm

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

launch_file_dir = os.path.dirname(os.path.realpath(__file__))
vehicle_parameters_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/vehicle_params/"))
maps_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/tracks/"))
odd_folder = os.path.abspath(os.path.join(launch_file_dir, "../assets/odd/"))

def create_simulated_vehicle(
    namespace: str,
    start_pose_utm: Tuple[float, float, int, str, float],
    goal_position_utm: Tuple[float, float, int, str, float],
    vehicle_id: int,
    v2x_id: int,
    vehicle_parameters_file: str = "NGC.json",
    map_file: str = "de_bs_borders_wfs.r2sr",
    controllable: bool = True
) -> List[Action]:

    """Create standalone ROS 2 nodes for the simulated vehicle stack."""

    planner_params = {
        "dt": 0.1,
        "horizon_steps": 40,
        "lane_error": 0.3,
        "long_error": 0.01,
        "speed_error": 1.0,
        "heading_error": 0.5,
        "steering_angle": 1.0,
        "acceleration": 0.1,
        "max_iterations": 300,
        "max_ms": 80,
        "debug": 0.0,
        "max_lateral_acceleration": 2.0,
        "idm_time_headway": 3.0,
        "ref_traj_length": 200
    }

    controller_pid_params = {
        "kp_x": 0.0,
        "ki_x": 0.0,
        "velocity_weight": 0.0,
        "kp_y": 0.4,
        "ki_y": 0.0,
        "heading_weight": 0.75,
        "kp_omega": 0.0,
        "dt": 0.05,
        "steering_comfort": 10000.25,
        "acceleration_comfort": 400.0,
        "acceleration_threshold": 0.25,
        "velocity_threshold": 0.25,
        "constant_brake": -1.0,
        "lookahead_time": 0.0
    }

    return [
        Node(
            package="simulated_vehicle",
            executable="simulated_vehicle",
            name="simulated_vehicle",
            namespace=namespace,
            parameters=[
                {"set_start_utm_position_x": start_pose_utm[0]},
                {"set_start_utm_position_y": start_pose_utm[1]},
                {"set_start_utm_zone_number": start_pose_utm[2]},
                {"set_start_utm_zone_letter": start_pose_utm[3]},
                {"set_start_psi": start_pose_utm[4]},
                {"vehicle_id": vehicle_id},
                {"v2x_id": v2x_id},
                {"controllable": controllable},
                {"vehicle_model_file": vehicle_parameters_folder + "/" + vehicle_parameters_file},
            ],
        ),
        Node(
            package="operational_design_domain",
            executable="operational_design_domain",
            name="operational_design_domain",
            namespace=namespace,
            parameters=[
                {"openodd_file": odd_folder + "/" + "simulation_odd.json" },
            ],
        ),
        Node(
            package="mission_control",
            executable="mission_control",
            name="mission_control",
            namespace=namespace,
            parameters=[
                {"map file": maps_folder + "/" + map_file},  # kept literal key as in original
                {"goal_position_x": goal_position_utm[0]},
                {"goal_position_y": goal_position_utm[1]},
                {"local_map_size": 100.0},
                # {"request_assistance_polygon": None},
            ],
        ),
        Node(
            package="decision_maker",
            executable="decision_maker",
            name="decision_maker",
            namespace=namespace,
            parameters=[
                {"planner_settings_keys": list(planner_params.keys())},
                {"planner_settings_values": list(planner_params.values())},
                {"vehicle_model_file": vehicle_parameters_folder + "/" + vehicle_parameters_file},
                {"v2x_id": v2x_id},
            ],
        ),
        Node(
            package="trajectory_tracker",
            executable="trajectory_tracker",
            name="trajectory_tracker",
            namespace=namespace,
            parameters=[
                {"set_controller": "PID"}, # MPC, PID, iLQR, Passthrough
                {"controller_settings_keys": list(
                    controller_pid_params.keys())},
                {"controller_settings_values": list(
                    controller_pid_params.values())},
                {"vehicle_model_file": vehicle_parameters_folder + "/" + vehicle_parameters_file},
            ],
        ),
    ]

