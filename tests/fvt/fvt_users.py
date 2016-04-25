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

import time
import unittest

from tests.fvt.fvt_base import TestBase
from tests.fvt.restapilib import APIRequestError


class TestUsers(TestBase):
    """
    Represents test cases that could help in testing the REST API /users

    Attributes:
        \param TestBase
         config file which contains all configuration
             information with sections
    """
    # Response json of a user looks like
    # {"profile":"admin", "gid":1003, "group":["testadm"],
    # "name":"testadm","uid":1003}
    default_schema = {"type": "object",
                      'required': ['profile', 'gid', 'group', 'name', 'uid'],
                      "properties":
                          {"profile": {"type": "string",
                                       "pattern": "^regularuser|virtuser|admin$"},
                           "gid": {"type": "number",
                                   },
                           "group": {"type": "array",
                                     "items": {"type": "string"},
                                     "minItems": 1,
                                     },
                           "name": {"type": "string"},
                           "uid": {"type": "number"},
                           }
                      }
    uri_users = '/plugins/ginger/users'

    def test_t001s_get_users(self):
        """
        method retrieve detailed information of all users
        """
        self.logging.info(
            '-->TestUsers.test_t001s_get_users()')
        try:
            self.logging.debug(
                'Retrieving summarized list of all users using uri %s'
                % self.uri_users)
            resp = self.session.request_get_json(
                self.uri_users, expected_status_values=[200])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                for each_json in resp:
                    self.logging.debug(
                        'validating json %s against default json schema '
                        'of user %s' % (each_json, self.default_schema))
                    self.validator.validate_json(
                        each_json, self.default_schema)
            else:
                self.logging.debug('Response is None/Empty')
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t001s_get_users()')

    def test_t002f_get_invalid_user(self):
        """
        method to test GET, for non existing user
        """
        self.logging.info(
            '-->TestUsers.test_t002f_get_invalid_user()')
        try:
            user_uri = self.uri_users + '/non_existing_user'
            self.logging.debug(
                'Negative test case to retrieve detailed information of '
                'non-existing user, with uri %s' % user_uri)
            resp = self.session.request_get_json(
                user_uri, expected_status_values=[404])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.info('As expected, received 404 status code')
            else:
                self.fail('Received empty response for GET non-exisiting user'
                          ' instead of 404 error. URI: %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t002f_get_invalid_user()')

    def test_t003s_create_user_with_default(self):
        """
        method to create user without group, profile and no_login attributes
        in post json. it should create regular user with log in shell
        """
        self.logging.info(
            '-->TestUsers.test_t003s_create_user_with_default()')
        try:
            self.logging.debug(
                'Creating user with default options for group, profile and'
                'no_login with uri %s' % self.uri_users)
            username = 'fake_fvt_user'
            ip_json = {'name': username, 'password': 'fake_password'}
            resp = self.session.request_post_json(
                self.uri_users, body=ip_json, expected_status_values=[201])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                found = False
                users = self.session.request_get_json(
                    self.uri_users, expected_status_values=[200])
                for user in users:
                    if user['name'] == username:
                        self.validator.validate_json(
                            user, self.default_schema)
                        found = True
                        break
                if not found:
                    self.fail('Failed to create user with defaults')
            else:
                self.fail('Received empty response for create user'
                          ' with %s' % ip_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t003s_create_user_with_default()')

    def test_t004s_get_regular_user(self):
        """
        method to test GET, for user with regularuser profile
        """
        self.logging.info(
            '-->TestUsers.test_t004s_get_regular_user()')
        try:
            # using the username created in previous test.
            # test case numbering ensures that this test case is executed
            # after test_t003s_create_user_with_default()
            user_uri = self.uri_users + '/fake_fvt_user'
            self.logging.debug(
                'Retrieve detailed information of user with regularuser '
                'profile with uri %s' % user_uri)
            resp = self.session.request_get_json(
                user_uri, expected_status_values=[200])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                if resp['profile'] != 'regularuser':
                    self.fail('Retrieved user profile is not "reguleruser"')
            else:
                self.fail('Received empty response for GET user with '
                          'regularuser profile with uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t004s_get_regular_user()')

    def test_t005s_create_user_with_nologin(self):
        """
        method to create regular user with no_login shell
        """
        self.logging.info(
            '-->TestUsers.test_t005s_create_user_with_nologin()')
        try:
            self.logging.debug(
                'Creating regular user with no_login shell'
                'with uri %s' % self.uri_users)
            username = 'fake_fvt_user_nologin'
            ip_json = {'name': username,
                       'password': 'fake_password', 'profile': 'regularuser',
                       'group': 'dummy_group', 'no_login': True}
            resp = self.session.request_post_json(
                self.uri_users, body=ip_json, expected_status_values=[201])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                found = False
                users = self.session.request_get_json(
                    self.uri_users, expected_status_values=[200])
                for user in users:
                    if user['name'] == username:
                        self.validator.validate_json(
                            user, self.default_schema)
                        found = True
                        break
                if not found:
                    self.fail('Failed to create regularuser with nologin shell')
            else:
                self.fail('Received empty response for create regularuser'
                          ' with no_login shell using data %s' % ip_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t005s_create_user_with_nologin()')

    def test_t006s_get_nologin_user(self):
        """
        method to test GET, for regularuser with nologin shell
        """
        self.logging.info(
            '-->TestUsers.test_t006s_get_nologin_user()')
        try:
            # using the username created in previous test.
            # test case numbering ensures that this test case is executed
            # after test_t005s_create_user_with_nologin()
            user_uri = self.uri_users + '/fake_fvt_user_nologin'
            self.logging.debug(
                'Retrieve detailed information of regularuser with '
                'nologin shell using uri %s' % user_uri)
            resp = self.session.request_get_json(
                user_uri, expected_status_values=[200])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                if resp['profile'] != 'regularuser':
                    self.fail('Retrieved user profile is not "reguleruser"')
            else:
                self.fail('Received empty response for GET regularuser '
                          'with nologin shell using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t006s_get_nologin_user()')

    def test_t007s_create_virt_user(self):
        """
        method to create virtuser
        """
        self.logging.info(
            '-->TestUsers.test_t007s_create_virt_user()')
        try:
            self.logging.debug(
                'Creating virtuser using uri %s' % self.uri_users)
            username = 'fake_fvt_virtuser'
            ip_json = {'name': username, 'password': 'fake_password',
                       'profile': 'virtuser', 'group': ''}
            resp = self.session.request_post_json(
                self.uri_users, body=ip_json, expected_status_values=[201])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                found = False
                users = self.session.request_get_json(
                    self.uri_users, expected_status_values=[200])
                for user in users:
                    if user['name'] == username:
                        self.validator.validate_json(
                            user, self.default_schema)
                        found = True
                        break
                if not found:
                    self.fail('Failed to create virtuser')
            else:
                self.fail('Received empty response for create virtuser'
                          ' using data %s' % ip_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t007s_create_virt_user()')

    def test_t008s_get_virtuser(self):
        """
        method to test GET, for virtuser
        """
        self.logging.info(
            '-->TestUsers.test_t008s_get_virtuser()')
        try:
            # using the username created in previous test.
            # test case numbering ensures that this test case is executed
            # after test_t007s_create_virt_user()
            user_uri = self.uri_users + '/fake_fvt_virtuser'
            self.logging.debug(
                'Retrieve detailed information of virtuser '
                'using uri %s' % user_uri)
            resp = self.session.request_get_json(
                user_uri, expected_status_values=[200])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                if resp['profile'] != 'virtuser':
                    self.fail('Retrieved user profile is not "virtuser"')
            else:
                self.fail('Received empty response for GET on virtuser '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t008s_get_virtuser()')

    def test_t009s_create_admin_user(self):
        """
        method to create admin user
        """
        self.logging.info(
            '-->TestUsers.test_t009s_create_admin_user()')
        try:
            self.logging.debug(
                'Creating admin user using uri %s' % self.uri_users)
            username = 'fake_fvt_admin'
            ip_json = {'name': username, 'password': 'fake_password',
                       'profile': 'admin', 'group': ''}
            resp = self.session.request_post_json(
                self.uri_users, body=ip_json, expected_status_values=[201])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                found = False
                users = self.session.request_get_json(
                    self.uri_users, expected_status_values=[200])
                for user in users:
                    if user['name'] == username:
                        self.validator.validate_json(
                            user, self.default_schema)
                        found = True
                        break
                if not found:
                    self.fail('Failed to create admin user')
            else:
                self.fail('Received empty response for creating admin user'
                          ' using data %s' % ip_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t009s_create_admin_user()')

    def test_t010s_get_admin_user(self):
        """
        method to test GET, for admin user
        """
        self.logging.info(
            '-->TestUsers.test_t010s_get_admin_user()')
        try:
            # using the username created in previous test.
            # test case numbering ensures that this test case is executed
            # after test_t009s_create_admin_user()
            user_uri = self.uri_users + '/fake_fvt_admin'
            self.logging.debug(
                'Retrieve detailed information of admin user '
                'using uri %s' % user_uri)
            resp = self.session.request_get_json(
                user_uri, expected_status_values=[200])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug(
                    'validating json %s against default json schema '
                    'of user %s' % (resp, self.default_schema))
                self.validator.validate_json(resp, self.default_schema)
                if resp['profile'] != 'admin':
                    self.fail('Retrieved user profile is not "admin"')
            else:
                self.fail('Received empty response for GET on admin user '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t010s_get_admin_user()')

    def test_t011s_delete_regularuser(self):
        """
        method to test DELETE, for regular user with login shell
        """
        self.logging.info(
            '-->TestUsers.test_t011s_delete_regularuser()')
        try:
            # using the username created in
            # test_t003s_create_user_with_default()
            # test case numbering ensures that this test case is executed
            # after test_t003s_create_user_with_default()
            user_uri = self.uri_users + '/fake_fvt_user'
            self.logging.debug(
                'Deleting regular user with log in shell '
                'using uri %s' % user_uri)
            resp = self.session.request_delete(
                user_uri, expected_status_values=[204])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug('successfully deleted user using uri %s'
                                   % user_uri)
            else:
                self.fail('Received empty response for deleting regular user '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t011s_delete_regularuser()')

    def test_t012s_delete_regularuser_nologin(self):
        """
        method to test DELETE, for regular user with nologin shell
        """
        self.logging.info(
            '-->TestUsers.test_t012s_delete_regularuser_nologin()')
        try:
            # using the username created in
            # test_t005s_create_user_with_nologin()
            # test case numbering ensures that this test case is executed
            # after test_t005s_create_user_with_nologin()
            user_uri = self.uri_users + '/fake_fvt_user_nologin'
            self.logging.debug(
                'Deleting regular user with nologin shell '
                'using uri %s' % user_uri)
            resp = self.session.request_delete(
                user_uri, expected_status_values=[204])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug('successfully deleted user using uri %s'
                                   % user_uri)
            else:
                self.fail('Received empty response for deleting regular user '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t012s_delete_regularuser_nologin()')

    def test_t013s_delete_virtuser(self):
        """
        method to test DELETE, for virtuser
        """
        self.logging.info(
            '-->TestUsers.test_t013s_delete_virtuser()')
        try:
            # using the username created in
            # test_t007s_create_virt_user()
            # test case numbering ensures that this test case is executed
            # after test_t007s_create_virt_user()
            user_uri = self.uri_users + '/fake_fvt_virtuser'
            self.logging.debug(
                'Deleting virtuser using uri %s' % user_uri)
            resp = self.session.request_delete(
                user_uri, expected_status_values=[204])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug('successfully deleted user using uri %s'
                                   % user_uri)
            else:
                self.fail('Received empty response for deleting virtuser '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t013s_delete_virtuser()')

    def test_t014s_delete_adminuser(self):
        """
        method to test DELETE, for admin user
        """
        self.logging.info(
            '-->TestUsers.test_t014s_delete_adminuser()')
        try:
            # using the username created in
            # test_t009s_create_admin_user()
            # test case numbering ensures that this test case is executed
            # after test_t009s_create_admin_user()
            user_uri = self.uri_users + '/fake_fvt_admin'
            self.logging.debug(
                'Deleting admin user using uri %s' % user_uri)
            resp = self.session.request_delete(
                user_uri, expected_status_values=[204])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug('successfully deleted user using uri %s'
                                   % user_uri)
            else:
                self.fail('Received empty response for deleting admin user '
                          'using uri %s' % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t014s_delete_adminuser()')

    def test_t015f_delete_nonexisting_user(self):
        """
        method to test CREATE, negative test case for non-existing user
        """
        self.logging.info(
            '-->TestUsers.test_t015f_delete_nonexisting_user()')
        try:
            user_uri = self.uri_users + '/fake_non_exist_fvtuser'
            self.logging.debug(
                'Negative test case to delete non-existing user '
                'using uri %s' % user_uri)
            resp = self.session.request_delete(
                user_uri, expected_status_values=[404])
            self.logging.debug('Response received: %s' % resp)
            self.logging.debug('As expected received 404 for  uri %s'
                                   % user_uri)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t015f_delete_nonexisting_user()')

    def test_t016f_create_invalid_profile(self):
        """
        method to test CREATE, negative test case with invalid profile
        """
        self.logging.info(
            '-->TestUsers.test_t016f_create_invalid_profile()')
        try:
            self.logging.debug(
                'Negative test case to test create user with invalid profile'
                ', with uri %s' % self.uri_users)
            username = 'user_inv_profile'
            ip_json = {'name': username, 'password': 'fake_password',
                       'profile': 'invalid_profile', 'group': ''}
            # note: only allowed values for profile are regularuser, virtuser
            # and admin
            resp = self.session.request_post_json(
                self.uri_users, body=ip_json, expected_status_values=[400])
            if resp:
                self.logging.debug('Response received: %s' % resp)
                self.logging.debug('As expected, received 400')
            else:
                self.fail('Received empty response, instead of 400 for create'
                          ' user with invalid profile. i/p : %s' % ip_json)
        except APIRequestError as error:
            self.logging.error(error.__str__())
            raise Exception(error)
        finally:
            self.logging.info(
                '<--TestUsers.test_t016f_create_invalid_profile()')
