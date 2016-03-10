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

import fs_utils
import utils

from diskparts import PartitionModel
from wok.exception import InvalidParameter, NotFoundError, OperationFailed
from wok.model.tasks import TaskModel
from wok.rollbackcontext import RollbackContext
from wok.utils import add_task, run_command, wok_log


class SwapsModel(object):
    """
    Model representing the collection of swap devices
    """

    def __init__(self, **kargs):
        self.objstore = kargs['objstore']
        self.task = TaskModel(**kargs)

    def create(self, params):

        file_loc = ''

        if 'file_loc' not in params or not params['file_loc']:
            wok_log.error("File location required for creating a swap device.")
            raise InvalidParameter('GINSP00001E')

        if 'type' not in params:
            wok_log.error("Type required for creating a swap device.")
            raise InvalidParameter('GINSP00002E')
        else:
            if params['type'] == 'file' and 'size' not in params:
                wok_log.error("Size is required file type swap device.")
                raise InvalidParameter('GINSP00003E')

            if params['type'] == 'device' or params['type'] == 'file':
                taskid = add_task(u'/swaps/file_loc/%s' % (file_loc),
                                  self._create_task, self.objstore, params)
                return self.task.lookup(taskid)
            else:
                wok_log.error("Incorrect swap type.")
                raise InvalidParameter('GINSP00004E')

    def _create_task(self, cb, params):
        type = params['type']
        file_loc = params['file_loc']

        cb('entering task to create swap file')
        with RollbackContext() as rollback:
            try:
                if type == 'file':
                    cb('create a file')
                    size = params['size']
                    utils._create_file(size, file_loc)

            except (InvalidParameter) as e:
                cb('OK', False)
                raise InvalidParameter("GINSP00020E")
            except (OperationFailed) as e:
                cb('OK', False)
                raise OperationFailed('GINSP00005E',
                                      {'file_loc': file_loc,
                                       'err': e.message})
            try:
                if type == 'device':
                    dev = file_loc.split("/")[-1]
                    if dev.startswith('dm-'):
                        dmname = utils.get_dm_name(file_loc.split("/")[-1])
                    else:
                        dmname = dev
                    part = PartitionModel(objstore=self.objstore)
                    dev_type = part.lookup(dmname)
                    if dev_type['type'] == 'part':
                        type = '82'   # hex value for type Linux Swap
                        part.change_type(dmname, type)

                cb('create swap from file')
                utils._make_swap(file_loc)

                cb('activate swap device')
                utils._activate_swap(file_loc)

                cb('persist swap device')
                import fs_utils
                fs_utils.persist_swap_dev(file_loc)

                cb('OK', True)

            except (OperationFailed) as e:
                rollback.prependDefer(SwapsModel.delete_swap_file, file_loc)
                cb('OK', False)
                raise OperationFailed('GINSP00005E',
                                      {'file_loc': file_loc,
                                       'err': e.message})

    @staticmethod
    def delete_swap_file(file_loc):
        """
        Method to delete a swap device
        :param file_loc: location of the file or device path
        :return:
        """

        try:
            # Remove only file type swap devices from filesystem
            if not file_loc.startswith('/dev'):
                os.remove(file_loc)

            utils._swapoff_device(file_loc)

        except Exception as e:
            wok_log.error("Error deleting a swap file, %s", e.message)
            raise OperationFailed('GINSP00006E')

    def get_list(self):
        out, err, rc = run_command(["cat", "/proc/swaps"])
        if rc != 0:
            raise OperationFailed("GINSP00007E", {'err': err})

        return utils._get_swapdev_list_parser(out)


class SwapModel(object):
    """
    Model representing a single swap device
    """

    def __init__(self, **kargs):
        pass

    def lookup(self, name):
        try:
            return utils._get_swap_output(device_name=name)

        except ValueError:
            raise NotFoundError("GINSP00008E", {'name': name})

    def delete(self, name):
        try:
            fs_utils.unpersist_swap_dev(name)
            utils._swapoff_device(name)
        except Exception as e:
            wok_log.error("Error deleting a swap device, %s", e.message)
            raise OperationFailed("GINSP00009E", {'err': e.message})
