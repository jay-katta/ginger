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
import utils
from tests.fvt.fvt_base import TestBase

class TestSwaps(TestBase):

    """
    Represents test case that could help in testing the REST API supported for Swaps.

    Attributes:
        \param TestBase
         config file which contains all configuration information with sections
    """

    default_swaps_schema = {"type": "object",
                                  "properties": {"priority": {"type": "string"},
                                                 "size": {"type": "string"},
                                                 "type": {"type": "string"},
                                                 "used": {"type": "string"},
                                                 "filename": {"type": "string"}
                                                 }
                                  }
    uri_swaps = '/plugins/ginger/swaps'
    task_uri = '/plugins/ginger/tasks'

    def test_S001_create_swap(self):
        """
        Create Swap by passing the file location, type and size specified in the config file
        :return:
        """
        self.logging.info('--> TestSwaps.test_create_swap()')
        try:
            file_loc = utils.readconfig(self, 'config', 'Swaps', 'file_loc')
            type = utils.readconfig(self, 'config', 'Swaps', 'type')
            if type == "file":
                size = utils.readconfig(self, 'config', 'Swaps', 'size')
                swap_data = {'file_loc': file_loc, 'type': type, 'size': size}
            else:
                swap_data = {'file_loc': file_loc, 'type': type}
            resp_swap = self.session.request_post_json(uri=self.uri_swaps, body=swap_data, expected_status_values=[201, 202])
            task_status = resp_swap["status"]
            task_id = resp_swap["id"]
            while task_status == "running":
                time.sleep(5)
                task_resp = self.session.request_get_json(
                        self.task_uri + '/' + task_id)
                task_status = task_resp["status"]
                print "Status: %s" % (task_status)
                continue
            if task_status == "finished":
                self.logging.debug('Creation of swap Successful : %s' % file_loc)
            else:
                self.logging.error('Creation of swap failed')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestSwaps.test_create_swap()')

    def test_S002_listSwaps(self):
        """
        Retrieve a summarized list of Swaps
        """
        self.logging.info('--> TestSwaps.test_listSwaps() ')
        try:
            self.logging.debug('Listing Swaps ')
            resp_swaps = self.session.request_get_json(self.uri_swaps,[200])
            if resp_swaps is not None:
                self.logging.debug('List of Swaps: %s', resp_swaps)
                for swap in resp_swaps:
                    self.validator.validate_json(swap, self.default_swaps_schema)
            else:
                self.logging.debug('No Swap found')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestSwaps.test_listSwaps()')

    def test_S003_get_Swap_details(self):
        """
        Retrieve the Information of a single Swap
        """
        self.logging.info('--> TestSwaps.test_get_Swap_details() ')
        try:
            self.logging.debug('Get Swap information')
            file_loc = utils.readconfig(self, 'config', 'Swaps', 'file_loc')
            fl = file_loc.split('/')
            fl = '%2F' + fl[1] + '%2F' + fl[2]
            swap_details = self.session.request_get_json(self.uri_swaps + '/' + fl,[200])
            self.validator.validate_json(swap_details, self.default_swaps_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestSwaps.test_get_Swap_details()')

    def test_S004_delete_Swap(self):
        """
        Delete the Swap specified in the config file
        :return:
        """
        self.logging.info('--> TestSwaps.test_delete_Swap()')
        try:
            file_loc = utils.readconfig(self, 'config', 'Swaps', 'file_loc')
            fl = file_loc.split('/')
            fl = '%2F' + fl[1] + '%2F' + fl[2]
            self.session.request_delete(uri=self.uri_swaps + '/' + fl, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestSwaps.test_delete_Swap()')



