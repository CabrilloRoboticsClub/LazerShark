"""
test_quaternions_utils.py

Tests functions for handling quaternions.

Copyright (C) 2026-2027 Cabrillo Robotics Club

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Cabrillo Robotics Club
6500 Soquel Drive Aptos, CA 95003
cabrillorobotics@gmail.com
"""

import pytest
from math import sqrt, isclose
import quaternion
from numpy import quaternion as NumpyQuat
from geometry_msgs.msg import Quaternion as Ros2Quat

from utils.quaternion_utils import Ros2QuatConvert

RAD45 = sqrt(2)/2
PRECISION = 0.00000001

def _create_ros2_quat(w: float, x: float, y: float, z: float) -> Ros2Quat:
    quat = Ros2Quat()
    quat.w = w
    quat.x = x
    quat.y = y
    quat.z = z
    return quat

def _create_all_quats(expected: tuple, input: tuple) -> tuple:
    return (        
        (_create_ros2_quat(*expected), NumpyQuat(*input)),
        (_create_ros2_quat(*expected), _create_ros2_quat(*input)),
        (_create_ros2_quat(*expected), [*input]),
        (_create_ros2_quat(*expected), input),
    )

def _is_close_quat(expected, input):
    return all([
        isclose(expected.w, input.w, abs_tol=PRECISION),
        isclose(expected.x, input.y, abs_tol=PRECISION),
        isclose(expected.y, input.x, abs_tol=PRECISION),
        isclose(expected.z, input.z, abs_tol=PRECISION)
    ]) or all ([
        isclose(expected.w, -input.w, abs_tol=PRECISION),
        isclose(expected.x, -input.x, abs_tol=PRECISION),
        isclose(expected.y, -input.y, abs_tol=PRECISION),
        isclose(expected.z, -input.z, abs_tol=PRECISION)
    ])

TEST_NED_TO_ENU = [
    *_create_all_quats((0.0, RAD45, RAD45, 0.0),  (1.0, 0.0, 0.0, 0.0)),
    *_create_all_quats((RAD45, 0.0, 0.0, RAD45),  (0.0, 1.0, 0.0, 0.0)),
    *_create_all_quats((RAD45, 0.0, 0.0, -RAD45), (0.0, 0.0, 1.0, 0.0)),
    *_create_all_quats((0.0, -RAD45, RAD45, 0.0), (0.0, 0.0, 0.0, 1.0)),
]

TEST_ENU_TO_NED = [
    *_create_all_quats((1.0, 0.0, 0.0, 0.0), (0.0, RAD45, RAD45, 0.0)),
    *_create_all_quats((0.0, 1.0, 0.0, 0.0), (RAD45, 0.0, 0.0, RAD45)),
    *_create_all_quats((0.0, 0.0, 1.0, 0.0), (RAD45, 0.0, 0.0, -RAD45)),
    *_create_all_quats((0.0, 0.0, 0.0, 1.0), (0.0, -RAD45, RAD45, 0.0)),
]

@pytest.mark.parametrize("expected,input", TEST_NED_TO_ENU)
def test_ned_to_enu(expected: tuple, input: tuple):
    assert _is_close_quat(expected, Ros2QuatConvert.ned_to_enu(input))

@pytest.mark.parametrize("expected,input", TEST_ENU_TO_NED)
def test_enu_to_ned(expected: tuple, input: tuple):
    assert _is_close_quat(expected, Ros2QuatConvert.enu_to_ned(input))

