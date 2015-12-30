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

class TestFilesystems(TestBase):
    default_schema = {"type": "object",
                      "properties": {"use%": {"type": "string"},
                                     "used": {"type": "string"},
                                     "mounted_on": {"type": "string"},
                                     "avail": {"type": "string"},
                                     "filesystem": {"type": "string"},
                                     "type": {"type": "string"},
                                     "size": {"type": "string"}
                                     }
                      }
    uri_filesystems = '/plugins/ginger/filesystems'

    def test_f001_fs_mount_with_type_missing(self):
        """
        Mount filesystem with type missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_fs_mount_with_type_missing()')
            blkdev = utils.readconfig(self, 'config', 'FILESYSTEM', 'blk_dev')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'mount_point')
            fs_data = {'blk_dev' : blkdev, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems,body=fs_data,expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_fs_mount_with_type_missing()')

    def test_f002_mount_with_invalid_type(self):
        """
        Mount filesystem with invalid type. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_mount_with_invalid_type()')
            blkdev = utils.readconfig(self, 'config', 'FILESYSTEM', 'blk_dev')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'mount_point')
            fs_data = {'type' : 'invalid', 'blk_dev' : blkdev, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_mount_with_invalid_type()')

    def test_f003_local_mount_without_blkdev(self):
        """
        Mount local filesystem with block device missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_local_mount_without_blkdev()')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'mount_point')
            fs_data = {'type' : 'local', 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_local_mount_without_blkdev()')

    def test_f004_local_mount_without_mountpoint(self):
        """
        Mount local filesystem with mountpoint missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_local_mount_without_mountpoint()')
            blkdev = utils.readconfig(self, 'config', 'FILESYSTEM', 'blk_dev')
            fs_data = {'type' : 'local', 'blk_dev' : blkdev}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_local_mount_without_mountpoint()')

    def test_f005_nfs_mount_without_server(self):
        """
        Mount NFS filesystem with server missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_nfs_mount_without_server()')
            share = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_share')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_mntpt')
            fs_data = {'type' : 'nfs', 'share' : share, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_nfs_mount_without_server()')

    def test_f006_nfs_mount_without_share(self):
        """
        Mount NFS filesystem with share missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_nfs_mount_without_share()')
            server = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_server')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_mntpt')
            fs_data = {'type' : 'nfs', 'server' : server, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_nfs_mount_without_share()')

    def test_f007_nfs_mount_without_mountpoint(self):
        """
        Mount NFS filesystem with mountpoint missing. Fails with 400.
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_nfs_mount_without_mountpoint()')
            server = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_server')
            share = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_share')
            fs_data = {'type' : 'nfs', 'server' : server, 'share' : share}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[400])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_nfs_mount_without_mountpoint()')

    def test_s001_local_mount(self):
        """
        Mount local filesystem
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_local_mount()')
            blkdev = utils.readconfig(self, 'config', 'FILESYSTEM', 'blk_dev')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'mount_point')
            fs_data = {'type' : 'local', 'blk_dev' : blkdev, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[201])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_local_mount()')

    def test_s002_nfs_mount(self):
        """
        Mount NFS filesystem
        :return:
        """
        try:
            self.logging.info('--> TestFilesystems.test_nfs_mount()')
            server = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_server')
            share = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_share')
            mountpt = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_mntpt')
            fs_data = {'type' : 'nfs', 'server' : server, 'share' : share, 'mount_point' : mountpt}
            self.session.request_post(uri=self.uri_filesystems, body=fs_data, expected_status_values=[201])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_nfs_mount()')

    def test_s003_list_fs(self):
        try:
            self.logging.info('--> TestFilesystems.test_list_fs()')
            resp_fs = self.session.request_get_json(self.uri_filesystems,[200])
            if resp_fs != []:
                for resp in resp_fs:
                    self.validator.validate_json(resp, self.default_schema)
            else:
                self.logging.debug('No filesystems found on the machine')
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_list_fs()')

    def test_s004_get_single_fs(self):
        mnt_pt = '%2Fdev'
        try:
            self.logging.info('--> TestFilesystems.test_get_single_fs()')
            resp_fs = self.session.request_get_json(self.uri_filesystems + '/' + mnt_pt,[200])
            self.validator.validate_json(resp_fs, self.default_schema)
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_get_single_fs()')

    def test_s005_unmount_fs(self):
        """
        Unmount filesystem
        :return:
        """
        mnt_pt = utils.readconfig(self, 'config', 'FILESYSTEM', 'mount_point')
        mnt_pt = mnt_pt.replace("/", "%2F")
        nfs_mnt = utils.readconfig(self, 'config', 'FILESYSTEM', 'nfs_mntpt')
        nfs_mnt = nfs_mnt.replace("/", "%2F")
        try:
            self.logging.info('--> TestFilesystems.test_unmount_fs()')
            self.session.request_delete(self.uri_filesystems + '/' + mnt_pt, [204])
            self.session.request_delete(self.uri_filesystems + '/' + nfs_mnt, [204])
        except Exception, err:
            self.logging.error(str(err))
            raise Exception(str(err))
        finally:
            self.logging.info('<-- TestFilesystems.test_unmount_fs()')


