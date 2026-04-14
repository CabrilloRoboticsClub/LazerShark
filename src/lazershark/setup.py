"""
setup.py

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

import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'lazershark'

setup(
    name=package_name,
    version='0.0.0',
    packages=['auv', 'auv.sensors', 'resource', 'utils'],
    data_files=[
        (os.path.join('share', package_name), ['package.xml']),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ], 
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='stephanielh1111@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "targetpoint=auv.sensors.targetpoint:main"
        ],
    },
)
