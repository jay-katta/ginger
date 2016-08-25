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


import utils
import time
from tests.fvt.fvt_base import TestBase
#from tests.fvt.restapilib import Validator


class TestDASDPartitions(TestBase):

    """
    Represents test case that could help in testing the REST API supported for DASD Partitions.

    Attributes:
        \param TestBase
         config file which contains all configuration information with sections
    """
    default_dasd_partitions_schema = {"type": "object",
                                  "properties": {"available": {"type": "boolean"},
                                                 "name": {"type": "string"},
                                                 "fstype": {"type": "string"},
                                                 "path": {"type": "string"},
                                                 "mountpoint": {"type": "string"},
                                                 "type": {"type": "string"},
                                                 "size": {"type": "string"}
                                                 }
                                  }
    uri_dasdpartitions = '/plugins/ginger/dasdpartitions'

    @classmethod
    def setUpClass(self):
        super(TestDASDPartitions, self).setUpClass()
        self.logging.info('--> TestDASDPartitions.setUpClass()')
        self.logging.debug('enabling and formatting the eckd'
                           'device specified in config file')
        bus_id = utils.readconfig(self, 'config', 'DASDdevs', 'bus_id')
        try:
            utils.enable_eckd(bus_id)
            self.dev = utils.fetch_dasd_dev(bus_id)
            utils.format_eckd(self.dev)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.setUpClass()')

    def test_f001_create_dasdpart_with_devicename_missing(self):
        """
        Create DASD Partition without specifying the device name. Fails with 400
        """

        self.logging.info('--> TestDASDPartitions.test_create_dasdpart_with_devicename_missing()')
        try:
            size = utils.readconfig(self, 'config', 'DASDPartitions', 'size')
            part_data = {'size': size}
            self.session.request_post(uri=self.uri_dasdpartitions, body=part_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.test_create_dasdpart_with_devicename_missing()')

    def test_f002_create_dasdpart_with_partsize_missing(self):
        """
        Create DASD Partition without specifying the partition size. Fails with 400
        """

        self.logging.info('--> TestDASDPartitions.test_create_dasdpart_with_partsize_missing()')
        try:
            part_data = {'dev_name': self.dev.split('/')[-1]}
            self.session.request_post(uri=self.uri_dasdpartitions, body=part_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.test_create_dasdpart_with_partsize_missing()')

    def test_S001_create_dasd_part(self):
        """
        Create DASD Partition by passing the DASD device name and partition size specified in the config file
        :return:
        """
        self.logging.info('--> TestDASDPartitions.test_create_dasd_part()')
        try:
            size = int(utils.readconfig(self, 'config', 'DASDPartitions', 'size'))
            part_data = {'dev_name': self.dev.split('/')[-1], 'size': size}
            self.session.request_post(uri=self.uri_dasdpartitions, body=part_data, expected_status_values=[201])
            time.sleep(5)
            self.logging.debug('Creation of partition on DASD device Successful : %s' % self.dev.split('/')[-1])
        except Exception, err:
            self.logging.error(err)
            raise Exception(err)
        finally:
            self.logging.info('<-- TestDASDPartitions.test_create_dasd_part()')

    def test_S002_listDASDPartitions(self):
        """
        Retrieve a summarized list of all DASD Partitions
        """
        self.logging.info('--> TestDASDPartitions.test_listDASDPartitions() ')
        try:
            self.logging.debug('Listing all DASD Partitions ')
            resp_dasd_part = self.session.request_get_json(self.uri_dasdpartitions,[200])
            if resp_dasd_part is not None:
                self.logging.debug('List of DASD Partitions: %s', resp_dasd_part)
                for part in resp_dasd_part:
                    self.validator.validate_json(part, self.default_dasd_partitions_schema)
            else:
                self.logging.debug('No DASD Partition found')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.test_listDASDPartitions()')

    def test_S003_get_DASDPartition_details(self):
        """
        Retrieve the Information of a single DASD Partition
        """
        self.logging.info('--> TestDASDPartitions.test_get_DASDPartition_details() ')
        try:
            self.logging.debug('Get DASD Partition information')
            part_name = self.dev.split('/')[-1] + '1'
            part_details = self.session.request_get_json(self.uri_dasdpartitions + '/' + part_name,[200])
            self.validator.validate_json(part_details, self.default_dasd_partitions_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.test_get_DASDPartition_details()')

    def test_S004_delete_dasd_part(self):
        """
        Delete the DASD Partition specified in the config file
        :return:
        """
        self.logging.info('--> TestDASDPartitions.test_delete_dasd_part()')
        try:
            part_name = self.dev.split('/')[-1] + '1'
            self.session.request_delete(uri=self.uri_dasdpartitions + '/' + part_name, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDPartitions.test_delete_dasd_part()')



