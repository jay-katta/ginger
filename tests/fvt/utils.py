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
import time


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

