"""
quaternions_utils.py

Provides various functions for handling quaternions.

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
import quaternion
import numpy as np
from numpy import quaternion as NumpyQuat
from geometry_msgs.msg import Quaternion as Ros2Quat
from scipy.spatial.transform import Rotation

class QuatUtils():   
    @staticmethod
    def create_change_of_basis_quat(matrix: np.array) -> NumpyQuat:
        """
        Creates a change of basis quaternion corresponding to the given change of basis matrix.

        Args:
            matrix: A change of basis matrix
        
        Returns:
            The corresponding change of basis quaternion.        
        """
        return np.quaternion(*(Rotation.from_matrix(matrix).as_quat(scalar_first=True)))

class Ros2QuatConvert():
    # Change of basis matrix from NED coordinates to ENU coordinates
    NED_TO_ENU_MATRIX = np.array([
        [0, 1,  0],
        [1, 0,  0],
        [0, 0, -1]
    ])

    NED_TO_ENU_QUAT = QuatUtils.create_change_of_basis_quat(NED_TO_ENU_MATRIX)
    ENU_TO_NED_QUAT = np.conjugate(NED_TO_ENU_QUAT)

    @staticmethod
    def ned_to_enu(ned_quat) -> Ros2Quat:
        """
        Converts an orientation quaternion from NED coordinates to ENU coordinates.

        Args:
            ned_quat: A quaternion-like object in NED coordinates with scalar-first convention if list/tuple.
        
        Returns:
            A Ros2 quaternion in ENU coordinates.
        """
        return Ros2QuatConvert._numpy_to_ros2_quat(
            Ros2QuatConvert.NED_TO_ENU_QUAT * Ros2QuatConvert._create_numpy_quat(ned_quat)
            )
    
    @staticmethod
    def enu_to_ned(enu_quat) -> Ros2Quat:
        """
        Converts an orientation quaternion from ENU coordinates to NED coordinates.

        Args:
            ned_quat: A quaternion-like object in ENU coordinates with scalar-first convention if list/tuple.
        
        Returns:
            A Ros2 quaternion in NED coordinates.
        """
        return Ros2QuatConvert._numpy_to_ros2_quat(
            Ros2QuatConvert.ENU_TO_NED_QUAT * Ros2QuatConvert._create_numpy_quat(enu_quat)
            )
    
    @staticmethod
    def _create_numpy_quat(quat_like) -> NumpyQuat:
        """
        Take a quaternion-like object and convert it to a Numpy quaternion.

        Args:
            quat_like: A quaternion-like object with scalar first convention if a list/tuple.

        Returns:
            The quaternion as a Numpy Quaternion

        Raises:
            TypeError: If `quat_like` is not a Numpy/Ros2 Quaternion or a list/tuple
        """
        if type(quat_like) is NumpyQuat:
            return quat_like
        elif type(quat_like) is Ros2Quat:
            return Ros2QuatConvert._ros2_to_numpy_quat(quat_like)
        elif type(quat_like) is list or type(quat_like) is tuple:
            return NumpyQuat(*quat_like)
        else:
            raise TypeError("Unrecognized quatlike")

    @staticmethod
    def _numpy_to_ros2_quat(npquat: NumpyQuat) -> Ros2Quat:
        """
        Converts a Numpy Quaternion to a Ros2 Quaternion

        Args:
            npquat: A numpy quaternion

        Returns:
            The quaternion as a Ros2 Quaternion

        Raises:
            TypeError: If npquat is not a Numpy Quaternion
        """
        if type(npquat) is not NumpyQuat:
            raise TypeError("Not a Numpy quaternion")
        ros2quat = Ros2Quat()
        ros2quat.x = npquat.x
        ros2quat.y = npquat.y
        ros2quat.z = npquat.z
        ros2quat.w = npquat.w
        return ros2quat

    @staticmethod
    def _ros2_to_numpy_quat(ros2quat: Ros2Quat) -> NumpyQuat:
        """
        Converts a Ros2 Quaternion to a Numpy Quaternion

        Args:
            ros2quat: A Ros2 quaternion

        Returns:
            The quaternion as a Numpy Quaternion

        Raises:
            TypeError: If ros2quat is not a Ros2 Quaternion
        """
        if type(ros2quat) is not Ros2Quat:
            raise TypeError("Not a Ros2 quaternion")
        return NumpyQuat(ros2quat.w, ros2quat.x, ros2quat.y, ros2quat.z)