#!/usr/bin/env python3
from lab_utils.net_utils.sshconnection import SshConnection
from lab_utils.log_utils.lablogger import LabLogger

ip_file = 'file_with_list_of_ips.txt'
firmware_path = '/somepath/file_with_firmware.img'

log = LabLogger('Upgrade_test')
with open(ip_file) as fh:
    sat_ips = fh.readlines()
for ip in sat_ips:
    try:
        sat = SshConnection(ip, password='yourpassword')
        sat.scp.put(firmware_path)
        sat.sys('sysupgrade ' + firmware_path, code=0, verbose=True)
        log.debug('Successful upgrade of RG with ip:' + ip)
    except Exception as Err:
        log.critical('FailedUpgrade of RG with IP' + ip +", err:" + str(Err))