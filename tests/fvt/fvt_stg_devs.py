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


class TestStgDevs(TestBase):
    default_schema = {"type": "object",
                      "properties": {"id": {"type": "string"},
                                     "mpath_count": {"type": "number"},
                                     "type": {"type": "string"},
                                     "name": {"type": "string"},
                                     "size": {"type": "string"},
                                     }
                      }

    uri_stgdevs = '/plugins/ginger/stgdevs'
    def test_s001_get_stg_devs(self):
        try:
            self.logging.info('--> TestStgDevs.test_get_stg_devs()')
            resp_devs = self.session.request_get_json(self.uri_stgdevs,[200])
            if resp_devs != []:
                for dev in resp_devs:
                    self.validator.validate_json(dev, self.default_schema)
            else:
                self.logging.debug('No storage devices found on the system')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestStgDevs.test_get_stg_devs()')



