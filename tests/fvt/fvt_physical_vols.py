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

class TestPhysicalVols(TestBase):
    default_schema = {"type": "object",
                      "properties": {"PESize": {"type": "string"},
                                     "PVSize": {"type": "string"},
                                     "PVName": {"type": "string"},
                                     "FreePE": {"type": "string"},
                                     "PVUUID": {"type": "string"},
                                     "Allocatable": {"type": "string"},
                                     "TotalPE": {"type": "string"},
                                     "VGName": {"type": ["string", "null"]},
                                     "AllocatedPE": {"type": "string"}
                                     }
                      }
    default_task_schema = {"type" : "object",
                          "properties": {"status": {"type": "string"},
                                         "message": {"type": "string"},
                                         "id": {"type": "string"},
                                         "target_uri": {"type": "string"},
                                         }
                          }
    uri_pvs = '/plugins/ginger/pvs'
    uri_task = '/plugins/ginger/tasks'

    def test_f001_create_pv_with_pvname_missing(self):
        """
        Create PV without specifying the device name. Fails with 400
        """
        try:
            self.logging.info('--> TestPhysicalVols.test_create_pv_with_pvname_missing()')
            pv_data = {}
            self.session.request_post(uri=self.uri_pvs,body=pv_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPhysicalVols.test_create_pv_with_pvname_missing()')

    def test_S001_create_pv(self):
        """
        Create PV by passing the device name specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestPhysicalVols.test_create_pv()')
            pvname = utils.readconfig(self, 'config', 'PV', 'pvname')
            pv_data = {'pv_name' : pvname}
            resp = self.session.request_post_json(uri=self.uri_pvs, body=pv_data, expected_status_values=[202])
            if resp is not None:
                self.validator.validate_json(resp, self.default_task_schema)
                task_status = resp["status"]
                task_id = resp["id"]
                while task_status == "running":
                    time.sleep(5)
                    task_resp = self.session.request_get_json(
                        self.uri_task + '/' + task_id, [200])
                    task_status = task_resp["status"]
                    continue
                if task_status == "finished":
                    self.logging.debug('Create PV is successful')
                else:
                    self.assertFalse(True)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPhysicalVols.test_create_pv()')

    def test_S002_get_pvs(self):
        try:
            self.logging.info('--> TestPhysicalVols.test_get_pvs()')
            resp_pvs = self.session.request_get_json(self.uri_pvs,[200])
            for pv in resp_pvs:
                self.validator.validate_json(pv, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPhysicalVols.test_get_pvs()')

    def test_S003_get_single_pv(self):
        try:
            self.logging.info('--> TestPhysicalVols.test_get_single_pv()')
            pvname = utils.readconfig(self, 'config', 'PV', 'pvname')
            pv = pvname.replace("/", "%2F")
            resp_pv = self.session.request_get_json(self.uri_pvs + '/' + pv,[200])
            self.validator.validate_json(resp_pv, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPhysicalVols.test_get_single_pv()')

    def S004_delete_pv(self):
        """
        Delete the PV specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestPhysicalVols.test_delete_pv()')
            pvname = utils.readconfig(self, 'config', 'PV', 'pvname')
            pv = pvname.replace("/", "%2F")
            self.session.request_delete(uri=self.uri_pvs + '/' + pv, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestPhysicalVols.test_delete_pv()')


