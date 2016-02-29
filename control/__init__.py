#
# Project Ginger
#
# Copyright IBM Corp, 2016
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import os

from wok.control.utils import load_url_sub_node

from backup import Backup
from capabilities import Capabilities
from config import Config
from dasddevs import DASDdevs
from dasdpartitions import DASDPartitions
from diskparts import Partitions
from filesystems import FileSystems
from firmware import Firmware
from firmware import FirmwareProgress
from ibm_sep import Sep
from log_volumes import LogicalVolumes
from network import Network
from physical_vol import PhysicalVolumes
from powermanagement import PowerProfiles
from sanadapters import SanAdapters
from sensors import Sensors
from storage_devs import StorageDevs
from users import Users
from swaps import Swaps
from sysmodules import SysModules
from vol_group import VolumeGroups


sub_nodes = load_url_sub_node(os.path.dirname(__file__), __name__)

__all__ = [
    Backup,
    Capabilities,
    Config,
    DASDdevs,
    DASDPartitions,
    FileSystems,
    Firmware,
    FirmwareProgress,
    LogicalVolumes,
    Network,
    Partitions,
    PowerProfiles,
    PhysicalVolumes,
    SanAdapters,
    Sensors,
    Sep,
    StorageDevs,
    Swaps,
    SysModules,
    Users,
    VolumeGroups
    ]
