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

import os
from tests.fvt.fvt_base import TestBase, APIRequestError


class TestKernelModule(TestBase):
    """
    Common Kernel module stest cases
    """
    default_kernel_module_schema = {"type": "object",
                                  "properties": {"description": {"type": "string"},
                                                 "license": {"type": "string"},
                                                 "vermagic": {"type": "string"},
                                                 "intree": {"type": "string"},
                                                 "name": {"type": "string"},
                                                 "filename": {"type": "string"},
                                                 "depends": {"type": "array"},
                                                 "version": {"type": "number"},
                                                 "srcversion": {"type": "string"},
                                                 "features": {"type": "string"},
                                                 "authors": {"type": "array"},
                                                 "parms": {"type": "string"},
                                                 "aliases": {"type": "array"}
                                                 }
                                  }
    kernel_module = "fjes"
    uri_sysmodules = '/plugins/ginger/sysmodules'
    load_module_data = {"name": "fjes"}
    load_invalid_module_data = {"name": "fjesabc"}

    @classmethod
    def setUpClass(cls):
        super(TestKernelModule, cls).setUpClass()
        cls.logging = cls.session.logging
        cls.logging.info('<-- TestCioIgnoreList.setUpClass()')

    def test_s001_list_loaded_modules(self):
        """
        List all loaded kernel modules.
        """
        self.logging.info('--> TestKernelModule.'
                          'test_s001_list_loaded_modules() ')

        try:
            self.logging.debug('Retrieve a details list of all loaded '
                               'kernel module')
            resp_json = self.session.request_get_json(
                TestKernelModule.uri_sysmodules)
            self.logging.debug('Loaded Kernel modules found : %s' % resp_json)
            if resp_json is not None:
                for each_json in resp_json:
                    self.logging.debug('Kernel module : %s' % each_json)
                    # self.validator.validate_json(repo_json,
                    # Repository.default_schema)
            else:
                self.logging.debug('No kernel module found : %s' % resp_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
        finally:
            self.logging.info('--> TestKernelModule.'
                              'test_s001_list_loaded_modules() ')

    def test_s002_get_loaded_kernel_module_info(self):
        """
        List a particular  loaded kernel module
        """
        self.logging.info('--> TestKernelModule.'
                          'test_s002_get_loaded_kernel_module_info)')

        try:
            self.logging.debug('Retrieve detailed information of an '
                               'module')
            uri_module = \
                TestKernelModule.uri_sysmodules + \
                os.sep + TestKernelModule.kernel_module
            resp_json = self.session.request_get_json(uri_module)
            self.logging.debug('Fjes kernel module details : %s' %
                               resp_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
        finally:
            self.logging.info('--> TestKernelModule.'
                              'test_s002_get_loaded_kernel_module_info()')

    def test_s003_load_kernel_module(self):
        """
        Load a kernel module
        """

        self.logging.info('--> TestKernelModule.'
                          'test_s003_load_kernel_module')

        try:
            self.logging.debug('Load a kernel module')
            resp_json = self.session.request_post_json(
                TestKernelModule.uri_sysmodules,
                TestKernelModule.load_module_data,
                expected_status_values=[201])
            self.logging.debug('Module details : %s' % resp_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
        finally:
            self.logging.info('--> TestKernelModule.'
                              'test_s003_load_kernel_module')

    def test_s004_load_invalid_kernel_module(self):
        """
        Load a invalid kernel module
        """
        self.logging.info('--> TestKernelModule.'
                          'test_s004_load_invalid_kernel_module ')
        try:
            self.logging.debug('Load a invalid kernel module')
            resp_json = self.session.request_post_json(
                TestKernelModule.uri_sysmodules,
                TestKernelModule.load_invalid_module_data,
                expected_status_values=[400])
            self.logging.debug('Loading a kernel module failed : '
                               '%s' % resp_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
        finally:
            self.logging.info('--> TestKernelModule.'
                              'test_s004_load_invalid_kernel_module ')

    def test_s005_unload_kernel_module(self):
        """
        Unload a kernel module
        """
        self.logging.info('-->TestKernelModule.'
                          'test_s005_unload_kernel_module ')
        try:
            self.logging.debug('Unload a kernel module')
            uri_module = \
                TestKernelModule.uri_sysmodules + \
                os.sep + TestKernelModule.kernel_module
            self.session.request_delete(uri_module)
        except Exception, err:
            self.logging.error(str(err))
        finally:
            self.logging.info('-->TestKernelModule.'
                              'test_s005_unload_kernel_module ')
