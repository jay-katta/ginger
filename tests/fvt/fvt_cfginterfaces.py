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
    create_bond_data = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "S003", "TYPE": "Bond", "BONDINFO": {
                        "SLAVES": ["S003slave1", "S003slave2"],
                        "BONDING_MASTER": "yes",
                        "BONDING_OPTS": {"mode": "balance-rr",
                                         "downdelay": "5", "updelay":
                                                 "7", "mimon": "8",
                                             "arp_interval": "9"}
                            }}
        }

    create_vlan_data = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "S004", "TYPE": "Vlan",
                       "VLANINFO": {"VLAN": "yes", "VLANID": "9",
                                    "PHYSDEV": "S004"}}
        }

    bond_with_noslaves = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBondnoSlaves", "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": [], "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    bond_with_invalid_opts = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBondnoSlaves",
                       "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": ["eth0", "eth1"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    bond_without_basicinfo = {
        "IPV4_INFO": {"IPV4INIT": "yes", "BOOTPROTO": "none",
                      "DEFROUTE": "yes",
                      "DNSAddresses": ["10.10.10.1", "10.10.10.2"],
                      "PEERDNS": "yes",
                      "PEERROUTES": "yes",
                      "IPV4Addresses": [{
                          "IPADDR": "10.10.10.10",
                          "NETMASK": "255.255.255.0",
                          "GATEWAY": "10.10.10.10"}],
                      "ROUTES": [{
                          "NETMASK": "24",
                          "GATEWAY": "10.10.10.123",
                          "ADDRESS": "10.10.10.10"}]},
        }

    cfg_without_ipv4init = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBond", "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": ["eth0", "eth1"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}},
        "IPV4_INFO": {"BOOTPROTO": "none", "DEFROUTE": "yes",
                      "DNSAddresses": ["10.10.10.1", "10.10.10.2"],
                      "PEERDNS": "yes", "PEERROUTES": "yes",
                      "IPV4Addresses": [{
                           "IPADDR": "10.10.10.10",
                           "NETMASK": "255.255.255.0",
                           "GATEWAY": "10.10.10.10"}],
                      "ROUTES": [{
                          "NETMASK": "24",
                          "GATEWAY": "10.10.10.123",
                          "ADDRESS": "10.10.10.10"}]}
        }

    cfg_without_type = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBondnoSlaves"}
        }

    create_bond_without_info = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBond", "TYPE": "Bond"}
        }

    create_bond_without_device = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": ["eth1", "eth2"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    create_bond_invalid_master_info = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBond", "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": [],
                                    "BONDING_MASTER": "okay",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    create_bond_without_master = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBond", "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": [],
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    create_bond_invalid_mode = {
        "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1", "ZONE": "FedoraServer",
                       "DEVICE": "ethFvtBond", "TYPE": "Bond",
                       "BONDINFO": {"SLAVES": ["eth0", "eth1"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "round",
                                                     "downdelay": "5",
                                                     "updelay": "7",
                                                     "mimon": "8",
                                                     "arp_interval": "9"}}}
        }

    @classmethod
    def setUpClass(cls):
        super(TestCfginterfaces, cls).setUpClass()
        cls.logging = cls.session.logging

    def _s001_list_allcfginterfaces(self):
            """
             List all cfginterface details
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s001_list_allcfginterfaces() ')
            try:
                self.logging.debug('Retrieve a details list of all defined '
                                   'interfaces')
                resp_json = self.session.request_get_json(
                    TestCfginterfaces.uri_cfginterfaces)
                self.logging.debug('Interfaces found : %s' % resp_json)
                if resp_json is not None:
                    for cfg_json in resp_json:
                        self.logging.debug('Cfginterfaces : %s' % cfg_json)
                        # self.validator.validate_json(repo_json,
                        # Repository.default_schema)
                else:
                    self.logging.debug('No interfaces found : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s001_list_allcfginterfaces() ')

    def test_s002_get_cfginterface_details(self):
            """
             Display cfginterface details
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s002_get_cfginterface_details() ')
            try:
                self.logging.debug('Retrieve detailed information of an '
                                   'interface')
                uri_lo = \
                    TestCfginterfaces.uri_cfginterfaces + \
                    os.sep + TestCfginterfaces.loopback
                resp_json = self.session.request_get_json(uri_lo)
                self.logging.debug('Loopback interface details : %s' %
                                   resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s002_get_cfginterface_details()')

    def test_s003_createbond(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s003_createbond() ')
            ifcfg_slave1 = "/etc/sysconfig/network-scripts/ifcfg-S003slave1"
            s1 = open(ifcfg_slave1, 'w')
            s1.write("DEVICE=S003slave1\n")
            s1.write("NAME=S003slave1\n")
            s1.write("TYPE=Ethernet\n")
            s1.close()
            ifcfg_slave2 = "/etc/sysconfig/network-scripts/ifcfg-S003slave2"
            s2 = open(ifcfg_slave2, 'w')
            s2.write("DEVICE=S003slave2\n")
            s2.write("NAME=S003slave2\n")
            s2.write("TYPE=Ethernet\n")
            s2.close()
            try:
                self.logging.debug('Create an interface of type Bond')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_data,
                    expected_status_values=[201])
                self.logging.debug('Bond details : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_slave1)
                os.remove(ifcfg_slave2)
                os.remove("/etc/sysconfig/network-scripts/ifcfg-S003")
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s003_createbond()')

    def test_s004_createvlan(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s004_createvlan() ')
            ifcfg_master = "/etc/sysconfig/network-scripts/ifcfg-S004"
            s1 = open(ifcfg_master, 'w')
            s1.write("DEVICE=S004\n")
            s1.write("NAME=S004\n")
            s1.write("TYPE=Ethernet\n")
            s1.close()
            try:
                self.logging.debug('Create an interface of type Vlan')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_vlan_data,
                    expected_status_values=[201])
                self.logging.debug('Vlan details : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_master)
                os.remove("/etc/sysconfig/network-scripts/ifcfg-vlan0009")
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s004_createvlan()')

    def test_s005_bond_with_noslaves(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s005_bond_with_noslaves() ')
            try:
                self.logging.debug('Create an interface of type Bond')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.bond_with_noslaves,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s005_bond_with_noslaves()')

    def test_s006_bond_with_invalid_opt(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s006_bond_with_invalid_opt() ')
            try:
                self.logging.debug('Create an interface of type Bond')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.bond_with_invalid_opts,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s006_bond_with_invalid_opt()')

    def test_s007_bond_without_basicinfo(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s007_bond_without_basicinfo() ')
            try:
                self.logging.debug('Create an interface of type Bond')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.bond_without_basicinfo,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s007_bond_without_basicinfo()')

    def test_s008_bond_without_ipv4init(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s008_bond_without_ipv4init() ')
            try:
                self.logging.debug('Create an interface of type Bond')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.cfg_without_ipv4init,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s008_bond_without_ipv4init()')

    def test_s009_cfg_without_type(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s009_cfg_without_type() ')
            try:
                self.logging.debug('Create an interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.cfg_without_type,
                    expected_status_values=[400])
                self.logging.debug('Interface creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s009_cfg_without_type()')

    def test_s010_create_bond_without_info(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s010_create_bond_without_info() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_without_info,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s010_create_bond_without_info()')

    def test_s011_create_bond_without_device(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s011_create_bond_without_device() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_without_device,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s011_create_bond_without_device()')

    def test_s012_create_bond_invalid_master(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s012_create_bond_invalid_master() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_invalid_master_info,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s012_create_bond_invalid_master()')

    def test_s013_create_bond_without_master(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s013_create_bond_without_master() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_without_master,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s013_create_bond_without_master()')

    def test_s014_create_bond_invalid_mode(self):
            """
            Create an interface of type bond
            """
            self.logging.info('--> TestCfginterfaces.'
                              'test_s014_create_bond_without_master() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    TestCfginterfaces.create_bond_invalid_mode,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s014_create_bond_without_master()')

    def test_s015_create_bond_invalid_downdelay(self):
            """
            Create an interface of type bond
            """
            create_bond_invalid_downdely = {
                "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer", "DEVICE": "ethFvtBond",
                               "TYPE": "Bond",
                               "BONDINFO": {"SLAVES": ["eth0", "eth1"],
                                            "BONDING_MASTER": "yes",
                                            "BONDING_OPTS":
                                                {"mode": "balance-rr",
                                                 "downdelay": "Five",
                                                 "updelay": "7",
                                                 "mimon": "8",
                                                 "arp_interval": "9"}}}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s015_create_bond_invalid_downdelay() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    create_bond_invalid_downdely,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s015_create_bond_invalid_downdelay()')

    def test_s016_create_bond_invalid_updelay(self):
            """
            Create an interface of type bond
            """
            create_bond_invalid_updely = {
                "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer", "DEVICE": "ethFvtBond",
                               "TYPE": "Bond",
                               "BONDINFO": {"SLAVES": ["eth0", "eth1"],
                                            "BONDING_MASTER": "yes",
                                            "BONDING_OPTS":
                                                {"mode": "balance-rr",
                                                 "downdelay": "5",
                                                 "updelay": "One",
                                                 "mimon": "8",
                                                 "arp_interval": "9"}}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s016_create_bond_invalid_updelay() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    create_bond_invalid_updely,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s016_create_bond_invalid_updelay()')

    def test_s017_create_bond_invalid_mimon(self):
            """
            Create an interface of type bond
            """
            create_bond_invalid_mimon = {
                "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer",
                               "DEVICE": "ethFvtBond",
                               "TYPE": "Bond",
                               "BONDINFO":
                                   {"SLAVES": ["eth0", "eth1"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "1",
                                                     "mimon": "two",
                                                     "arp_interval": "9"}}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s017_create_bond_invalid_mimon() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    create_bond_invalid_mimon,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s017_create_bond_invalid_mimon()')

    def test_se018_create_bond_invalid_arp(self):
            """
            Create an interface of type bond
            """
            create_bond_invalid_arp = {
                "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer", "DEVICE": "ethFvtBond",
                               "TYPE": "Bond",
                               "BONDINFO":
                                   {"SLAVES": ["eth0", "eth1"],
                                    "BONDING_MASTER": "yes",
                                    "BONDING_OPTS": {"mode": "balance-rr",
                                                     "downdelay": "5",
                                                     "updelay": "1",
                                                     "mimon": "2",
                                                     "arp_interval": "two"}}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_se018_create_bond_invalid_arp() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    create_bond_invalid_arp,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_se018_create_bond_invalid_arp()')

    def test_se019_create_bond_no_slavekey(self):
            """
            Create an interface of type bond
            """
            create_bond_no_slavekey = {
                "BASIC_INFO": {"ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer",
                               "DEVICE": "ethFvtBond",
                               "TYPE": "Bond",
                               "BONDINFO": {"BONDING_MASTER": "yes"}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_se019_create_bond_no_slavekey() ')
            try:
                self.logging.debug('Create an Bond interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces,
                    create_bond_no_slavekey,
                    expected_status_values=[400])
                self.logging.debug('Bond creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_se019_create_bond_no_slavekey()')

    # def _s020_create_vlan(self):
    #         """
    #         Create an interface of type bond
    #         """
    #         create_vlan = {
    #         "BASIC_INFO": {"NAME": "eth0.1",
    #             "ONBOOT": "yes",
    #             "MTU": "1",
    #             "ZONE": "FedoraServer",
    #             "DEVICE": "eth0.1",
    #             "TYPE": "Vlan",
    #             "VLANINFO": {"VLAN" : "yes",
    #                         "VLANID": "99",
    #                         "PHYSDEV": "eth0"}
    #             }
    #         }
    #         self.logging.info('--> TestCfginterfaces.'
    #                           'test_s020_create_vlan() ')
    #         try:
    #             self.logging.debug('Create an Vlan interface')
    #             resp_json = self.session.request_post_json(
    #                 TestCfginterfaces.uri_cfginterfaces, create_vlan,
    #                 expected_status_values=[201])
    #             self.logging.debug('Vlan interface details are : '
    #                                '%s' %(resp_json))
    #         except APIRequestError as error:
    #             self.logging.error(error.__str__())
    #         finally:
    #             self.logging.info('<-- TestCfginterfaces.'
    #                               'test_s020_create_vlan()')

    def test_s021_vlan_without_info(self):
            """
            Create an interface of type bond
            """
            vlan_without_info = {
                "BASIC_INFO": {"NAME": "eth0.1",  "ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer", "DEVICE": "eth0.1",
                               "TYPE": "Vlan"}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s021_vlan_without_info() ')
            try:
                self.logging.debug('Create an Vlan interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces, vlan_without_info,
                    expected_status_values=[400])
                self.logging.debug('Vlan creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s021_vlan_without_info()')

    def test_s022_vlan_without_phydev(self):
            """
            Create an interface of type bond
            """
            vlan_without_phydev = {
                "BASIC_INFO": {"NAME": "eth0.1", "ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer",
                               "DEVICE": "eth0.1",
                               "TYPE": "Vlan",
                               "VLANINFO": {"VLAN": "yes", "VLANID": "99"}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s022_vlan_without_phydev() ')
            try:
                self.logging.debug('Create an Vlan interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces, vlan_without_phydev,
                    expected_status_values=[400])
                self.logging.debug('Vlan creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s022_vlan_without_phydev()')

    def test_s023_vlan_without_vlanid(self):
            """
            Create an interface of type bond
            """
            vlan_without_vlanid = {
                "BASIC_INFO": {"NAME": "eth0.1", "ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer",
                               "DEVICE": "eth0.1",
                               "TYPE": "Vlan",
                               "VLANINFO": {"VLAN": "yes", "PHYSDEV": "eth0"}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s023_vlan_without_vlanid() ')
            try:
                self.logging.debug('Create an Vlan interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces, vlan_without_vlanid,
                    expected_status_values=[400])
                self.logging.debug('Vlan creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s023_vlan_without_vlanid()')

    def test_s024_vlan_invalid_vlanid(self):
            """
            Create an interface of type bond
            """
            vlan_invalid_id = {
                "BASIC_INFO": {"NAME": "eth0.1", "ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer", "DEVICE": "eth0.1",
                               "TYPE": "Vlan",
                               "VLANINFO": {"VLAN": "yes",
                                            "VLANID": "9999",
                                            "PHYSDEV": "eth0"}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s024_vlan_invalid_vlanid() ')
            try:
                self.logging.debug('Create an Vlan interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces, vlan_invalid_id,
                    expected_status_values=[400])
                self.logging.debug('Vlan creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s024_vlan_invalid_vlanid()')

    def test_s025_vlan_invalid_vlankey(self):
            """
            Create an interface of type vlan with invalid vlankey
            """
            vlan_invalid_key = {
                "BASIC_INFO": {"NAME": "eth0.1", "ONBOOT": "yes", "MTU": "1",
                               "ZONE": "FedoraServer",
                               "DEVICE": "eth0.1",
                               "TYPE": "Vlan",
                               "VLANINFO": {"VLAN": "Okay",
                                            "VLANID": "99",
                                            "PHYSDEV": "eth0"}}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s025_vlan_invalid_vlankey() ')
            try:
                self.logging.debug('Create an Vlan interface')
                resp_json = self.session.request_post_json(
                    TestCfginterfaces.uri_cfginterfaces, vlan_invalid_key,
                    expected_status_values=[400])
                self.logging.debug('Vlan creation failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s025_vlan_invalid_vlankey()')

    def test_s026_update_ipv6_autoconf(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S026"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S026\n")
            f.write("NAME=S026\n")
            f.close()
            update_ipv6 = {
                "BASIC_INFO": {"DEVICE": "S026"},
                "IPV6_INFO":
                    {"IPV6INIT": "yes",
                     "IPV6_AUTOCONF": "yes",
                     "IPV6_DEFROUTE": "yes",
                     "DNSAddresses": ["fe80::120b:a9ff:fe00:4de1",
                                      "fe80::120b:a9ff:fe00:4de2"],
                     "IPV6_PEERDNS": "yes",
                     "IPV6_PEERROUTES": "yes"}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s026_update_ipv6_autoconf() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S026", update_ipv6,
                    expected_status_values=[200])
                self.logging.debug('After updating IPV6, interface '
                                   'details are : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s026_update_ipv6_autoconf()')

    def test_s027_update_ipv6_dhcp(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S027"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S027\n")
            f.write("NAME=S027\n")
            f.close()
            update_ipv6_dhcp = {
                "BASIC_INFO": {"DEVICE": "S027"},
                "IPV6_INFO": {"IPV6INIT": "yes",
                              "IPV6_AUTOCONF": "no",
                              "DHCPV6C": "yes",
                              "IPV6_DEFROUTE": "yes",
                              "DNSAddresses": ["fe80::120b:a9ff:fe00:4de1",
                                               "fe80::120b:a9ff:fe00:4de2"],
                              "IPV6_PEERDNS": "yes",
                              "IPV6_PEERROUTES": "yes"}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s027_update_ipv6_dhcp() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S027",
                    update_ipv6_dhcp,
                    expected_status_values=[200])
                self.logging.debug('After updating IPV6, interface '
                                   'details are : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s027_update_ipv6_dhcp()')

    def test_s028_update_ipv6_manual(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S028"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S028\n")
            f.write("NAME=S028\n")
            f.close()
            update_ipv6_manual = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO":
                    {"IPV6INIT": "yes",
                     "IPV6_AUTOCONF": "no",
                     "IPV6_DEFROUTE": "yes",
                     "DNSAddresses": ["fe80::120b:a9ff:fe00:4de1",
                                      "fe80::120b:a9ff:fe00:4de2"],
                     "IPV6_PEERDNS": "yes",
                     "IPV6_PEERROUTES": "yes"}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s028_update_ipv6_manual() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S028",
                    update_ipv6_manual,
                    expected_status_values=[500])
                self.logging.debug('Updating an interface failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_S028_update_ipv6_manual()')

    def test_s029_update_ipv6_manual_invalidip(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S029"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S029\n")
            f.write("NAME=S029\n")
            f.close()
            update_ipv6_manual_invalidip = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO":
                    {"IPV6INIT": "yes",
                     "IPV6_AUTOCONF": "no",
                     "IPV6_DEFROUTE": "yes",
                     "DNSAddresses": ["fe80::120b:a9ff:fe00:4de1",
                                      "fe80::120b:a9ff:fe00:4de2"],
                     "IPV6_PEERDNS": "yes",
                     "IPV6_PEERROUTES": "yes",
                     "IPV6Addresses":
                         [{"PREFIX": "64",
                           "IPADDR": "fe80::221:ccff:fe72:d02e"},
                          {"PREFIX": "24",
                           "IPADDR": "fe80::221:ccff:fe72:d02ef"}]}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s029_update_ipv6_manual_invalidip() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S029",
                    update_ipv6_manual_invalidip,
                    expected_status_values=[400])
                self.logging.debug('Updating an interface failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s029_update_ipv6_manual_invalidip()')

    def test_s030_update_ipv6_manual_validip(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S030"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S030\n")
            f.write("NAME=S030\n")
            f.close()
            update_ipv6_manual_validip = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO":
                    {"IPV6INIT": "yes",
                     "IPV6_AUTOCONF": "no",
                     "IPV6_DEFROUTE": "yes",
                     "DNSAddresses": ["fe80::120b:a9ff:fe00:4de1",
                                      "fe80::120b:a9ff:fe00:4de2"],
                     "IPV6_PEERDNS": "yes",
                     "IPV6_PEERROUTES": "yes",
                     "IPV6Addresses":
                         [{"PREFIX": "64",
                           "IPADDR": "fe80::221:ccff:fe72:d02e"},
                          {"PREFIX": "24",
                           "IPADDR": "fe80::221:ccff:fe72:d02f"}]}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s030_update_ipv6_manual_validip() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S030",
                    update_ipv6_manual_validip,
                    expected_status_values=[200])
                self.logging.debug('After Updating, an interface details are '
                                   'to : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s030_update_ipv6_manual_validip()')

    def test_s031_update_ipv6_manual_missingprefix(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S031"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S031\n")
            f.write("NAME=S031\n")
            f.close()
            update_ipv6_manual_missingprefix = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO": {"IPV6INIT": "yes", "IPV6_AUTOCONF": "no",
                              "IPV6Addresses": [{
                                  "IPADDR": "fe80::221:ccff:fe72:d02e"}]}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s031_update_ipv6_manual_missingprefix() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S031",
                    update_ipv6_manual_missingprefix,
                    expected_status_values=[500])
                self.logging.debug('Updating an interface failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s031_update_'
                                  'ipv6_manual_missingprefix()')

    def test_s032_update_ipv6_manual_modemissing(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S032"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S032\n")
            f.write("NAME=S032\n")
            f.close()
            update_ipv6_manual_modemissing = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO": {"IPV6INIT": "yes", "IPV6_AUTOCONF": "no",
                              "IPV6Addresses": [{"PREFIX": "24"}]}
            }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s032_update_ipv6_manual_modemissing() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S032",
                    update_ipv6_manual_modemissing,
                    expected_status_values=[500])
                self.logging.debug('Updating an interface failed due to : '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- '
                                  'TestCfginterfaces.'
                                  'test_s032_update_'
                                  'ipv6_manual_modemissing()')

    def test_s033_update_ipv6_default_gateway(self):
            """
            Update IPV6 information on an interface
            """
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S033"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S033\n")
            f.write("NAME=S033\n")
            f.close()
            update_ipv6_default_gateway = {
                "BASIC_INFO": {"DEVICE": "eth0"},
                "IPV6_INFO": {"IPV6INIT": "yes", "IPV6_AUTOCONF": "no",
                              "IPV6Addresses":
                                  [{"PREFIX": "64",
                                    "IPADDR": "fe80::221:ccff:fe72:d02e"},
                                   {"PREFIX": "24",
                                    "IPADDR": "fe80::221:ccff:fe72:d02f"}],
                              "IPV6_DEFAULTGW": "fe80::221:ccff:fe72:d026"}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s033_update_ipv6_default_gateway() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S033",
                    update_ipv6_default_gateway,
                    expected_status_values=[200])
                self.logging.debug('After Updating, an interface details are '
                                   'to : %s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s033_update_ipv6_default_gateway()')

    def test_s034_ipv4_routes_option1(self):
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S034"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S034\n")
            f.write("NAME=S034\n")
            f.close()
            routes_file = "/etc/sysconfig/network-scripts/route-S034"
            r = open(routes_file, 'w')
            r.write("10.10.10.10/24 via 10.10.10.123\n")
            r.close()
            self.logging.info('--> TestCfginterfaces.'
                              'test_s034_ipv4_routes_option1() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_get_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S034",
                    expected_status_values=[200])
                self.logging.debug('Interface details are: '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                os.remove(routes_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s034_ipv4_routes_option1()')

    def test_s035_ipv4_routes_option2(self):
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S035"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S035\n")
            f.write("NAME=S035\n")
            f.close()
            routes_file = "/etc/sysconfig/network-scripts/route-S035"
            r = open(routes_file, 'w')
            r.write("ADDRESS0=10.10.10.11\n")
            r.write("NETMASK0=255.255.254.0\n")
            r.write("GATEWAY0=101.10.10.10\n")
            r.write("METRIC0=2\n")
            r.close()
            self.logging.info('--> TestCfginterfaces.'
                              'test_s035_ipv4_routes_option2() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_get_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S035",
                    expected_status_values=[200])
                self.logging.debug('Interface details are: '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                os.remove(routes_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s035_ipv4_routes_option2()')

    def test_s036_ipv6_routes_option1(self):
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S036"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S036\n")
            f.write("NAME=S036\n")
            f.close()
            routes_file = "/etc/sysconfig/network-scripts/route6-S036"
            r = open(routes_file, 'w')
            r.write("fe80::120b:a9ff:fe00:4de6/64 via "
                    "fe80::120b:a9ff:fe00:4de5 metric 1 \n")
            r.close()
            self.logging.info('--> TestCfginterfaces.'
                              'test_s036_ipv6_routes_option1() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_get_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S036",
                    expected_status_values=[200])
                self.logging.debug('Interface details are: '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                os.remove(routes_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s036_ipv6_routes_option1()')

    def test_s037_update_ipv4_routes_option1(self):
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S037"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S037\n")
            f.write("NAME=S037\n")
            f.close()
            routes_file = "/etc/sysconfig/network-scripts/route-S037"
            ipv4_routes = {
                "BASIC_INFO": {"NAME": "S037", "DEVICE": "S037"},
                "IPV4_INFO": {"IPV4INIT": "yes", "BOOTPROTO": "none",
                              "ROUTES": [{"METRIC": "2",
                                          "NETMASK": "255.255.254.0",
                                          "GATEWAY": "101.10.10.10",
                                          "ADDRESS": "10.10.10.11"},
                                         {"NETMASK": "255.255.254.0",
                                          "GATEWAY": "101.10.10.10",
                                          "ADDRESS": "10.10.10.13"}]}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s037_update_ipv4_routes_option1() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S037",
                    ipv4_routes,
                    expected_status_values=[200])
                self.logging.debug('Interface details are: '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                os.remove(routes_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s037_update_ipv4_routes_option1()')

    def test_s038_update_ipv6_routes_option1(self):
            ifcfg_file = "/etc/sysconfig/network-scripts/ifcfg-S038"
            f = open(ifcfg_file, 'w')
            f.write("DEVICE=S038\n")
            f.write("NAME=S038\n")
            f.close()
            routes_file = "/etc/sysconfig/network-scripts/route6-S038"
            ipv6_routes = {
                "BASIC_INFO": {"NAME": "S038", "DEVICE": "S038"},
                "IPV6_INFO": {"IPV6INIT": "yes", "IPV6_AUTOCONF": "yes",
                              "ROUTES":
                                  [{"METRIC": "1", "NETMASK": "64",
                                    "GATEWAY": "fe80::120b:a9ff:fe00:4de5",
                                    "ADDRESS": "fe80::120b:a9ff:fe00:4de6"}],
                              "IPV6_DEFAULTGW": "fe80::221:ccff:fe72:d026"}
                }
            self.logging.info('--> TestCfginterfaces.'
                              'test_s038_update_ipv6_routes_option1() ')
            try:
                self.logging.debug('Update IPv6 for an interface')
                resp_json = self.session.request_put_json(
                    TestCfginterfaces.uri_cfginterfaces + "/S038",
                    ipv6_routes,
                    expected_status_values=[200])
                self.logging.debug('Interface details are: '
                                   '%s' % resp_json)
            except APIRequestError as error:
                self.logging.error(error.__str__())
            finally:
                os.remove(ifcfg_file)
                os.remove(routes_file)
                self.logging.info('<-- TestCfginterfaces.'
                                  'test_s038_update_ipv6_routes_option1()')
