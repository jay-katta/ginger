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

import time

from tests.fvt.restapilib import Validator
from tests.fvt.fvt_base import TestBase, APIRequestError
import utils


class TestDASDdevs(TestBase):

    """
    Represents test case that could help in testing the REST API supported for DASD Devices.

    Attributes:
    \param TestBase
    config file which contains all configuration information with sections
    """

    default_dasd_devices_schema = {"type": "object",
                                  "properties": {"status": {"type": "string"},
                                                 "blocks": {"type": "string"},
                                                 "name": {"type": "string"},
                                                 "uid": {"type": "string"},
                                                 "type": {"type": "string"},
                                                 "eer_enabled": {"type": "string"},
                                                 "erplog": {"type": "string"},
                                                 "use_diag": {"type": "string"},
                                                 "readonly": {"type": "string"},
                                                 "device": {"type": "string"},
                                                 "blk_sz": {"type": "integer"},
                                                 "bus_id": {"type": "string"},
                                                 "size": {"type": "string"}

                                                 }
                                  }
    uri_dasddevs = '/plugins/ginger/dasddevs'
    task_uri = '/plugins/ginger/tasks'

    def test_S001_format_dasd(self):
        """
        Format DASD device by passing the bus_id and block size specified in the config file
        :return:
        """
        self.logging.info('--> TestDASDdevs.test_format_dasd()')
        try:
            bus_id = utils.readconfig(self, 'config', 'DASDdevs', 'bus_id')
            blk_size = utils.readconfig(self, 'config', 'DASDdevs', 'blk_size')
            format_data = {'blk_size': blk_size}
            resp_fmt = self.session.request_post_json(uri=self.uri_dasddevs + '/' + bus_id + '/' + 'format', body=format_data, expected_status_values=[202])
            task_status = resp_fmt["status"]
            task_id = resp_fmt["id"]
            while task_status == "running":
                time.sleep(5)
                task_resp = self.session.request_get_json(
                        self.task_uri + '/' + task_id)
                task_status = task_resp["status"]
                print "Status: %s" % (task_status)
                continue
            if task_status == "finished":
                self.logging.debug('Format of DASD device Successful : %s' % bus_id)
            else:
                self.logging.error('Format of DASD device is failed')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDdevs.test_format_dasd()')

    def test_S002_listDASDdevices(self):
        """
        Retrieve a summarized list of all DASD devices
        """
        self.logging.info('--> TestDASDdevs.test_listDASDdevices() ')
        try:
            self.logging.debug('Listing all DASD devices ')
            resp_dasd_dev = self.session.request_get_json(self.uri_dasddevs,[200])
            if resp_dasd_dev is not None:
                self.logging.debug('List of DASD Devices: %s', resp_dasd_dev)
                for dev in resp_dasd_dev:
                    self.validator.validate_json(dev, self.default_dasd_devices_schema)
            else:
                self.logging.debug('No DASD Device found')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDdevs.test_listDASDdevices()')

    def test_S003_get_DASDdevice_details(self):
        """
        Retrieve the Information of a single DASD Device
        """
        self.logging.info('--> TestDASDdevs.test_get_DASDdevice_details() ')
        try:
            self.logging.debug('Get DASD Device information')
            bus_id = utils.readconfig(self, 'config', 'DASDdevs', 'bus_id')
            dev_details = self.session.request_get_json(self.uri_dasddevs + '/' + bus_id,[200])
            self.validator.validate_json(dev_details, self.default_dasd_devices_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestDASDdevs.test_get_DASDdevice_details()')



