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


class TestVolGroups(TestBase):
    default_schema = {"type": "object",
                      "properties": {"vgName": {"type": "string"},
                                     "vgStatus": {"type": "string"},
                                     "vgSize": {"type": "number"},
                                     "maxLV": {"type": "string"},
                                     "freePESize": {"type": "number"},
                                     "format": {"type": "string"},
                                     "curLV": {"type": "number"},
                                     "metadataAreas": {"type": "string"},
                                     "permission": {"type": "string"},
                                     "allocPE": {"type": "string"},
                                     "pvNames": {"type": "array"},
                                     "peSize": {"type": "number"},
                                     "systemID": {"type": ["string", "null"]},
                                     "curPV": {"type": "string"},
                                     "freePE": {"type": "string"},
                                     "maxPV": {"type": "string"},
                                     "totalPE": {"type": "string"},
                                     "vgUUID": {"type": "string"},
                                     "allocPESize": {"type": "number"},
                                     "metadataSequenceNo": {"type": "string"}
                                     }
                      }
    default_task_schema = {"type" : "object",
                          "properties": {"status": {"type": "string"},
                                         "message": {"type": "string"},
                                         "id": {"type": "string"},
                                         "target_uri": {"type": "string"},
                                         }
                          }

    uri_vgs = '/plugins/ginger/vgs'
    uri_task = '/plugins/ginger/tasks'

    @classmethod
    def setUpClass(self):
        super(TestVolGroups, self).setUpClass()
        self.logging.info('--> TestVolGroups.setUpClass()')
        self.logging.debug('creating pv and vg on the eckd'
                           'device specified in config file')
        bus_id = utils.readconfig(self, 'config', 'DASDdevs', 'bus_id')
        try:
            utils.enable_eckd(bus_id)
            self.dev = utils.fetch_dasd_dev(bus_id)
            #utils.format_eckd(self.dev)
            utils.partition_eckd(self.dev)
            time.sleep(5)
            utils.partition_eckd(self.dev)
            time.sleep(5)
            utils.create_pv(self.dev+'1')
            utils.create_pv(self.dev+'2')
            self.vgname = utils.readconfig(self, 'config', 'VG', 'vgname')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.setUpClass()')

    def test_f001_create_vg_with_vgname_missing(self):
        """
        Create VG without specifying the VG name. Fails with 400
        """
        try:
            self.logging.info('--> TestVolGroups.test_create_vg_with_vgname_missing()')
            vg_data = {'pv_paths': [self.dev+'1']}
            self.session.request_post(uri=self.uri_vgs,body=vg_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_create_vg_with_vgname_missing()')

    def test_f002_create_vg_with_pvpaths_missing(self):
        """
        Create VG without specifying the PV Paths. Fails with 400
        """
        try:
            self.logging.info('--> TestVolGroups.test_create_vg_with_pvpaths_missing()')
            vg_data = {'vg_name': 'testvg'}
            self.session.request_post(uri=self.uri_vgs,body=vg_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_create_vg_with_pvpaths_missing()')

    def test_S001_create_vg(self):
        """
        Create VG by passing the VG name and PV paths specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestVolGroups.test_create_vg()')
            pvpaths = [self.dev+'1']
            vg_data = {'vg_name' : self.vgname, 'pv_paths' : pvpaths}
            resp = self.session.request_post_json(uri=self.uri_vgs, body=vg_data, expected_status_values=[202])
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
                    self.logging.debug('Create VG is successful')
                else:
                    self.assertFalse(True)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_create_vg()')

    def test_S002_get_vgs(self):
        try:
            self.logging.info('--> TestVolGroups.test_get_vgs()')
            resp_vgs = self.session.request_get_json(self.uri_vgs,[200])
            if resp_vgs != []:
                for vg in resp_vgs:
                    self.validator.validate_json(vg, self.default_schema)
            else:
                self.logging.debug('No volume groups found on the machine')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_get_vgs()')

    def test_S003_get_single_vg(self):
        try:
            self.logging.info('--> TestVolGroups.test_get_single_vg()')
            resp_vg = self.session.request_get_json(self.uri_vgs + '/' + self.vgname,[200])
            self.validator.validate_json(resp_vg, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_get_single_vg()')

    def test_S004_extend_vg(self):
        """
        Extend the VG with the additional PVs specified in config file
        :return:
        """
        try:
            self.logging.info('--> TestVolGroups.test_extend_vg()')
            pvnames = [self.dev+'2']
            pv_data = {'pv_paths' : pvnames}
            self.session.request_post(uri=self.uri_vgs + '/' + self.vgname + '/extend', body=pv_data)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_extend_vg()')

    def test_S005_reduce_vg(self):
        """
        Reduce the VG by removing the PVs specified in config file
        :return:
        """
        try:
            self.logging.info('--> TestVolGroups.test_reduce_vg()')
            pvnames = [self.dev+'2']
            pv_data = {'pv_paths' : pvnames}
            self.session.request_post(uri=self.uri_vgs + '/' + self.vgname + '/reduce', body=pv_data)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_reduce_vg()')

    def test_S006_delete_vg(self):
        """
        Delete the VG specified in the config file
        :return:
        """
        try:
            self.logging.info('--> TestVolGroups.test_delete_vg()')
            self.session.request_delete(uri=self.uri_vgs + '/' + self.vgname, expected_status_values=[204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestVolGroups.test_delete_vg()')

    @classmethod
    def tearDownClass(self):
        """
        clean up
        :return:
        """
        self.logging.info('--> TestVolGroups.tearDownClass()')
        self.logging.debug('delete the pv and vg created in setup class')
        utils.delete_pv(self.dev+'1')
        utils.delete_pv(self.dev+'2')
        time.sleep(5)
        utils.del_eckd_partition(self.dev)
        utils.del_eckd_partition(self.dev)
        self.logging.info('<-- TestVolGroups.tearDownClass()')
