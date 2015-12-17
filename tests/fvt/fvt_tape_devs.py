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


class TestTapeDevs(TestBase):
    default_schema = {"type": "object",
                      "properties": {"Vendor": {"type": "string"},
                                     "uuid": {"type": "string"},
                                     "Generic": {"type": "string"},
                                     "State": {"type": "string"},
                                     "Device": {"type": "string"},
                                     "Model": {"type": "string"},
                                     "Type": {"type": "string"},
                                     "Target": {"type": "string"}
                                     }
                      }
    uri_tapedevs = '/plugins/gingers390x/lstapes'
    def test_s001_get_tape_devs(self):
        try:
            self.logging.info('--> TestTapeDevs.test_get_tape_devs()')
            resp_tapes = self.session.request_get_json(self.uri_tapedevs,[200])
            if resp_tapes != []:
                for tape in resp_tapes:
                    self.validator.validate_json(tape, self.default_schema)
            else:
                self.logging.debug('No tape devices found in the machine') 
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestTapeDevs.test_get_tape_devs()')


