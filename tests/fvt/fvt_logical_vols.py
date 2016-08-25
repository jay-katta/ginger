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


class TestLogicalVols(TestBase):
    default_schema = {"type": "object",
                      "properties": {"lvName": {"type": "string"},
                                     "vgName": {"type": "string"},
                                     "lvPath": {"type": "string"},
                                     "segments": {"type": "string"},
                                     "#open": {"type": "string"},
                                     "blockDevice": {"type": "string"},
                                     "lvStatus": {"type": "string"},
                                     "lvCreationhost, time": {"type": "string"},
                                     "-currentlySetTo": {"type": "string"},
                                     "allocation": {"type": "string"},
                                     "lvUUID": {"type": "string"},
                                     "currentLE": {"type": "string"},
                                     "lvWriteAccess": {"type": "string"},
                                     "lvSize": {"type": "string"},
                                     "readAheadSectors": {"type": "string"}
                                     }
                      }
    default_task_schema = {"type" : "object",
                          "properties": {"status": {"type": "string"},
                                         "message": {"type": "string"},
                                         "id": {"type": "string"},
                                         "target_uri": {"type": "string"},
                                         
                                        }
                          }

    uri_lvs = '/plugins/ginger/lvs'
    uri_task = '/plugins/ginger/tasks'

    @classmethod
    def setUpClass(self):
        super(TestLogicalVols, self).setUpClass()
        self.logging.info('--> TestLogicalVols.setUpClass()')
        self.logging.debug('creating pv and vg on the eckd'
                           'device specified in config file')
        bus_id = utils.readconfig(self, 'config', 'DASDdevs', 'bus_id')
        try:
            utils.enable_eckd(bus_id)
            self.dev = utils.fetch_dasd_dev(bus_id)
            #utils.format_eckd(self.dev)
            utils.partition_eckd(self.dev)
            time.sleep(5)
            utils.create_pv(self.dev+'1')
            self.vgname = utils.readconfig(self, 'config', 'LV', 'vgname')
            utils.create_vg(self.vgname, self.dev+'1')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.setUpClass()')

    def test_f001_create_lv_with_vgname_missing(self):
        """
        Create LV without specifying the VG name. Fails with 400
        """
        try:
            self.logging.info('--> TestLogicalVols.test_create_lv_with_vgname_missing()')
            lv_data = {'size': '10M'}
            self.session.request_post(uri=self.uri_lvs,body=lv_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_create_lv_with_vgname_missing()')

    def test_f002_create_lv_with_size_missing(self):
        """
        Create LV without specifying the size. Fails with 400
        """
        try:
            self.logging.info('--> TestLogicalVols.test_create_lv_with_size_missing()')
            lv_data = {'vg_name': 'testvg'}
            self.session.request_post(uri=self.uri_lvs,body=lv_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_create_lv_with_size_missing()')

    def test_S001_create_lv(self):
        """
        Create LV by passing the VG name and Size specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestLogicalVols.test_create_lv()')
            size = utils.readconfig(self, 'config', 'LV', 'size')
            lv_data = {'vg_name' : self.vgname, 'size' : size}
            resp = self.session.request_post_json(uri=self.uri_lvs, body=lv_data, expected_status_values=[202])
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
                else:
                    self.assertFalse(True)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_create_lv()')

    def test_S002_get_lvs(self):
        try:
            self.logging.info('--> TestLogicalVols.test_get_lvs()')
            resp_lvs = self.session.request_get_json(self.uri_lvs,[200])
            if resp_lvs != []:
                for lv in resp_lvs:
                    self.validator.validate_json(lv, self.default_schema)
            else:
                self.logging.debug('No logical volumes found on the machine')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_get_lvs()')

    def test_S003_get_single_lv(self):
        try:
            self.logging.info('--> TestLogicalVols.test_get_single_lv()')
            lvname = utils.readconfig(self, 'config', 'LV', 'lvname')
            lv = '%2Fdev' + '%2F' + self.vgname + '%2F' + lvname
            resp_lv = self.session.request_get_json(self.uri_lvs + '/' + lv,[200])
            self.validator.validate_json(resp_lv, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_get_single_lv()')

    def test_S004_delete_lv(self):
        """
        Delete the LV specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestLogicalVols.test_delete_lv()')
            lvname = utils.readconfig(self, 'config', 'LV', 'lvname')
            lv = '%2Fdev' + '%2F' + self.vgname + '%2F' + lvname
            self.session.request_delete(uri=self.uri_lvs + '/' + lv, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestLogicalVols.test_delete_lv()')

    @classmethod
    def tearDownClass(self):
        """
        clean up
        :return:
        """
        self.logging.info('--> TestLogicalVols.tearDownClass()')
        self.logging.debug('delete the pv and vg created in setup class')
        utils.delete_vg(self.vgname)
        utils.delete_pv(self.dev+'1')
        time.sleep(5)
        utils.del_eckd_partition(self.dev)
        self.logging.info('<-- TestLogicalVols.tearDownClass()')
