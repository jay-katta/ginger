#!/usr/bin/python
# Project Kimchi
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301USA

import os

from tests.fvt.fvt_base import TestBase, APIRequestError

class TestCfginterfaces(TestBase):
    """
    Common storage test cases
    """
    uri_cfginterfaces = '/plugins/ginger/network/cfginterfaces'
    loopback = "lo"

    @classmethod
    def setUpClass(cls):
        super(TestCfginterfaces, cls).setUpClass()
        cls.logging = cls.session.logging

    def test_S001_list_allcfginterfaces(self):
            """
             List all cfginterface details
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_S001_list_allcfginterfaces() ')
            try:
                self.logging.debug('Retrieve a details list of all defined '
                                   'interfaces')
                resp_json = self.session.request_get_json(
                    TestCfginterfaces.uri_cfginterfaces)
                self.logging.debug('Interfaces found : %s' %(resp_json))
                if resp_json is not None:
                    for repo_json in resp_json:
                        self.logging.debug('Cfginterfaces : %s' %(repo_json))
                        # self.validator.validate_json(repo_json, Repository.default_schema)
                else:
                    self.logging.debug('No interfaces found : %s' %(
                        resp_json))
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_S001_list_allcfginterfaces() ')

    def test_S002_display_cfginterface_details(self):
            """
             Display cfginterface details
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_S002_display_cfginterface_details() ')
            try:
                self.logging.debug('Retrieve detailed information of an '
                                   'interface')
                uri_lo = \
                    TestCfginterfaces.uri_cfginterfaces + \
                    os.sep + TestCfginterfaces.loopback
                resp_json = self.session.request_get_json(uri_lo)
                self.logging.debug('Loopback repository details : %s' %(
                    resp_json))
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_S002_display_cfginterface_details()')
