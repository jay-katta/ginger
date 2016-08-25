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

import ConfigParser
import os
import time
import subprocess


def readconfig(session, configfile, section, key):
    session.logging.info(
        '-->utils.readconfig(): configfile:%s, section:%s, key:%s' % (configfile, section, key))

    if configfile:
        try:
            session.logging.info('Reading configuration file %s' % configfile)
            params = ConfigParser.ConfigParser()
            params.read(configfile)
        except Exception as e:
            session.logging.error("Failed to read config file %s. Error: %s" % (configfile, e.__str__()))
            session.logging.info('<-- utils.readconfig()')
            return
        if params.has_section(section):
            if params.has_option(section, key):
                value = params.get(section, key)
                session.logging.info('<-- utils.readconfig()')
                return value
            else:
                session.logging.error("Option %s is not avaliable in Section %s of config file %s" % (key, section, configfile))
        else:
            session.logging.error("Section %s is not available in the config file %s" % (section, configfile))
    else:
        session.logging.error('Configuration file required')

    session.logging.info('<-- utils.readconfig()')


def wait_task_status_change(session, task_id, task_uri='/plugins/gingers390x/tasks/', task_final_status='finished',
                            task_current_status='running'):
    """
    Wait till task changed its status from task current status
    :param session: session for logging into restful api of the kimchi
    :param task_id: Task Id for which status need to be checked
    :param task_final_status: Final expected status of task
    :param task_current_status: Current status of task
    :return:task_resp: Get response of task id, if task status is other than task_final_status or task_current_status, Raise exception
    """
    session.logging.info(
        '-->utils.wait_task_status_change(): task_id:%s |task_uri:%s |task_final_status:%s |task_current_status:%s'
        %(str(task_id), task_uri, task_final_status, task_current_status))
    counter = 0

    while True:
        if counter > 10:
            raise Exception('Task status change timed out for task id: %s' % str(task_id))

        counter += 1

        task_resp = session.request_get_json(
            task_uri + '/' + task_id)
        task_status = task_resp["status"]
        if task_status == task_current_status:
            time.sleep(2)
            continue
        elif task_status == task_final_status:
            break
        else:
            raise Exception('Task status does not changed to %s. Task Response:%s', task_final_status, task_resp)

    session.logging.debug('task_resp:%s', task_resp)
    session.logging.info('<--utils.wait_task_status_change()')
    return task_resp


def enable_eckd(busid):
    """
    Enable the passed eckd device
    :param busid: bus-id of the eckd to be enabled
    """
    en_out = subprocess.Popen(["chccwdev", "-e", busid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = en_out.communicate()
    if en_out.returncode != 0:
        raise Exception('Failed to enable the eckd device: ', err)


def format_eckd(devpath):
    """
    Format the passed eckd device to be used
    as a block device
    :param devpath: path of the eckd device
    """
    fmt_out = subprocess.Popen(["dasdfmt", "-b", "4096", "-y", devpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = fmt_out.communicate()
    if fmt_out.returncode != 0:
        raise Exception('Failed to format the eckd device: ', err)

def fetch_dasd_dev(busid):
    """

    :param busid:
    :return:
    """
    lsdasd = subprocess.Popen(["lsdasd", "-l", busid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = lsdasd.communicate()
    if lsdasd.returncode != 0:
        raise Exception, err
    devname = out.splitlines()[0].split('/')[1]
    devname = '/dev/'+ devname
    return devname

def partition_eckd(dev):
    """
    Create 20M partition on the given eckd device
    :param dev: device path of the eckd device
    """
    part_str = '\nn\n \n' + '+20M' + '\n' + 'w\n'
    p1_out = subprocess.Popen(["echo", "-e", "\'", part_str, "\'"],
                              stdout=subprocess.PIPE)
    p2_out = subprocess.Popen(["fdasd", dev], stdin=p1_out.stdout,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p1_out.stdout.close()
    out, err = p2_out.communicate()
    if p2_out.returncode != 0:
        raise Exception('Failed to partition the dasd device: ', err)

def format_part_with_fs(part_path, fstype):
    """
    Format the given partition with specified filesystem
    :param part_path: device path of the partition
    :param fstype: filesystem type
    """
    print "path: ", part_path
    print "fstype: ", fstype
    force_flag = '-F'
    if fstype == 'xfs':
        force_flag = '-f'
    fmt_fs = subprocess.Popen(["mkfs", "-t", fstype, force_flag, part_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = fmt_fs.communicate()
    if fmt_fs.returncode != 0:
        raise Exception('Failed to format filesystem: ', err)

def create_mount_point(fs_mount_point):
    """
    Create mount point if it doesnt exist
    :param fs_mount_point: mount point to be created
    """
    if not os.path.exists(fs_mount_point):
        os.mkdir(fs_mount_point)

def nfs_setup(nfs_share_path, nfs_mount_pt):
    """
    Setup nfs server and create share path
    and mount point if it doesnt exist
    :param nfs_share_path: nfs share to be shared
    :param nfs_mount_pt: mount point
    """
    if not os.path.exists(nfs_share_path):
        if not os.path.exists("/var/ftp"):
            os.mkdir("/var/ftp")
            os.mkdir(nfs_share_path)
        else:
            os.mkdir(nfs_share_path)

    is_exported = False
    with open("/etc/exports") as fo:
        lines = fo.readlines()
    for i in lines:
        path = i.split()[0]
        if path == nfs_share_path:
            is_exported = True

    if not is_exported:
        with open("/etc/exports", "a+") as fo:
            fo.write(nfs_share_path + " " + "*(rw,sync)")

    nfs_out = subprocess.Popen(["service", "nfs-server", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = nfs_out.communicate()
    if nfs_out.returncode != 0:
        raise Exception, err

    if not os.path.exists(nfs_mount_pt):
        os.mkdir(nfs_mount_pt)

def delete_dir(path):
    if os.path.exists(path):
        os.rmdir(path)

def del_eckd_partition(devname, part_num='1'):
    """
    Delete the created partition
    :param devname: device path of the eckd device
    """
    part_str = '\nd\n' + part_num + '\n' + 'w\n'
    p1_out = subprocess.Popen(["echo", "-e", "\'", part_str, "\'"],
                              stdout=subprocess.PIPE)
    p2_out = subprocess.Popen(["fdasd", devname], stdin=p1_out.stdout,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p1_out.stdout.close()
    out, err = p2_out.communicate()
    if p2_out.returncode != 0:
        raise Exception('Failed to delete eckd partition: ', err)

def create_pv(part):
    """
    Create a PV on the specified partition
    :param part: device path of the partition
    """
    pv_out = subprocess.Popen(["pvcreate", "-f", part], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = pv_out.communicate()
    if pv_out.returncode != 0:
        raise Exception('Failed to create pv: ', err)

def create_vg(vgname, pvpath):
    """
    Create a VG from the pv path provided
    :param vgname:Name of the VG to be created
    :param pvpath:device path of the pv
    """
    vg_out = subprocess.Popen(["vgcreate", vgname, pvpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = vg_out.communicate()
    if vg_out.returncode != 0:
        raise Exception('Failed to create vg: ', err)

def delete_vg(vgname):
    """
    Delete a VG
    :param vgname: name of the VG to be deleted
    """
    del_vg = subprocess.Popen(["vgremove", vgname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = del_vg.communicate()
    if del_vg.returncode != 0:
        raise Exception('Failed to delete vg: ', err)

def delete_pv(part):
    """
    Delete a pv
    :param part:device path of the pv
    """
    del_pv = subprocess.Popen(["pvremove", part], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = del_pv.communicate()
    if del_pv.returncode != 0:
        raise Exception('Failed to remove pv: ', err)

def add_lun(adapter, port, lun_id):
    """
    Add a LUN to system
    :param adapter: HBA adapter id
    :param port: Remote port wwpn
    :param lun_id: Id of the given LUN
    """

    port_dir = '/sys/bus/ccw/drivers/zfcp/' + adapter + '/' + port + '/'
    lun_dir = port_dir + lun_id

    if os.path.exists(lun_dir):
        # LUN already present on the system, nothing to add.
        return
    else:
        try:
            with open(port_dir + 'unit_add', "w") as txt_file:
                txt_file.write(lun_id)
        except Exception as e:
            raise Exception("Failed to add lun", {'err': e.message})

def remove_lun(adapter, port, lun_id):
    """
    Add a LUN to system
    :param adapter: HBA adapter id
    :param port: Remote port wwpn
    :param lun_id: Id of the given LUN
    """

    port_dir = '/sys/bus/ccw/drivers/zfcp/' + adapter + '/' + port + '/'
    lun_dir = port_dir + lun_id

    if not os.path.exists(lun_dir):
        # LUN already removed.
        return
    else:
        try:
            with open(port_dir + 'unit_remove', "w") as txt_file:
                txt_file.write(lun_id)
        except Exception as e:
            raise Exception("Failed to remove lun", {'err': e.message})
