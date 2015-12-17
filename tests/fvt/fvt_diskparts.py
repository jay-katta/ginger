#
# Project Ginger
#
# Copyright IBM, Corp. 2015
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

from tests.fvt.fvt_base import TestBase
import utils
import time


class TestPartitions(TestBase):
    default_schema = {"type": "object",
                      "properties": {"name": {"type": "string"},
                                     "fstype": {"type": "string"},
                                     "path": {"type": "string"},
                                     "mountpoint": {"type": "string"},
                                     "type": {"type": "string"},
                                     "size": {"type": "string"}
                                     }
                      }
    default_task_schema = {"type" : "object",
                           "properties": {"status": {"type": "string"},
                                          "message": {"type": "string"},
                                          "id": {"type": "string"},
                                          "target_uri": {"type": "string"},
                                          }
                           }

    uri_partitions = '/plugins/ginger/partitions'
    uri_task = '/plugins/ginger/tasks'

    def test_f001_create_part_with_devname_missing(self):
        """
        Create disk partition with device name missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_create_part_with_devname_missing()')
            part_size = utils.readconfig(self, 'config', 'PARTITIONS', 'part_size')
            part_data = {'partsize': part_size}
            self.session.request_post(uri=self.uri_partitions,body=part_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_create_part_with_devname_missing()')

    def test_f002_create_part_with_partsize_missing(self):
        """
        Create disk partition with partition size missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_create_part_with_partsize_missing()')
            devname = utils.readconfig(self, 'config', 'PARTITIONS', 'devname')
            part_data = {'devname' : devname}
            self.session.request_post(uri=self.uri_partitions, body=part_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_create_part_with_partsize_missing()')

    def test_s001_create_part(self):
        """
        Create disk partition by reading the device name and partition size from the config file
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_create_part()')
            devname = utils.readconfig(self, 'config', 'PARTITIONS', 'devname')
            part_size = utils.readconfig(self, 'config', 'PARTITIONS', 'part_size')
            part_data = {'devname' : devname, 'partsize': part_size}
            self.session.request_post(uri=self.uri_partitions, body=part_data, expected_status_values=[201])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_create_part()')

    def test_s002_get_partitions(self):
        try:
            self.logging.info('--> TestPartitions.test_get_partitions()')
            resp_parts = self.session.request_get_json(self.uri_partitions,[200])
            if resp_parts != []:
                for part in resp_parts:
                    self.validator.validate_json(part, self.default_schema)
            else:
                self.logging.debug('No disks or partitions found on the machine')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_get_partitions()')

    def test_s003_get_single_partition(self):
        self.logging.info('--> TestPartitions.test_get_single_partition()')
        partname = utils.readconfig(self, 'config', 'PARTITIONS', 'part_name')
        try:
            resp_part = self.session.request_get_json(self.uri_partitions + '/' + partname,[200])
            self.validator.validate_json(resp_part, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_get_single_partition()')


    def test_s004_format_partition(self):
        """
        Format the disk partition with the filesystem type specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_format_partition()')
            fstype = utils.readconfig(self, 'config', 'PARTITIONS', 'fstype')
            partname = utils.readconfig(self, 'config', 'PARTITIONS', 'format_part')
            part_data = {'fstype' : fstype}
            resp = self.session.request_post_json(TestPartitions.uri_partitions + '/' + partname + '/format', body=part_data)
            if resp is not None:
                self.validator.validate_json(resp, TestPartitions.default_task_schema)
                task_status = resp["status"]
                task_id = resp["id"]
                while task_status == "running":
                    time.sleep(5)
                    task_resp = self.session.request_get_json(
                        TestPartitions.uri_task + '/' + task_id, [200])
                    task_status = task_resp["status"]
                    continue
                if task_status == "finished":
                    self.logging.debug('Format partition is successful')
                else:
                    self.assertFalse(True)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_format_partition()')

    def test_s005_change_part_type(self):
        """
        Change the partition type with the type specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_change_part_type()')
            part_type = utils.readconfig(self, 'config', 'PARTITIONS', 'part_type_code')
            partname = utils.readconfig(self, 'config', 'PARTITIONS', 'part_name')
            part_data = {'type' : part_type}
            self.session.request_post(uri=self.uri_partitions + '/' + partname + '/change_type', body=part_data, expected_status_values=[200])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_change_part_type()')

    def test_s006_delete_part(self):
        """
        Delete the partition specified in config file
        :return:
        """
        try:
            self.logging.info('--> TestPartitions.test_delete_part()')
            partname = utils.readconfig(self, 'config', 'PARTITIONS', 'part_name')
            self.session.request_delete(uri=self.uri_partitions + '/' + partname, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPartitions.test_delete_part()')

