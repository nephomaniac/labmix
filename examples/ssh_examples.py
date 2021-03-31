#!/usr/bin/env python3

# import the SshConnection and LabLogger classes...
from lab_utils.net_utils.sshconnection import SshConnection
from lab_utils.log_utils.lablogger import LabLogger
import argparse
#Get some cli args first...
parser = argparse.ArgumentParser(
    description='Sample to show ssh usage...',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Set a default hub addr, this can be the WAN or LAN addr
hubip='192.168.1.1'
parser.add_argument('-i', '--hubip', default=hubip,
                        help='Provide the wan or lan IP of the hub to connect to')

args = parser.parse_args()
hubip = args.hub_ip or hubip


#Create a logging instance...
log = LabLogger('SSH_EXAMPLE')



# Create ssh connection objects...
# Example ssh to an RG's WAN addr...
log.debug('Creating an ssh session to my hub:{0}'.format(hubip))
hub = SshConnection(hubip, password='hub_pass')

# Run a command to get the mac
hub.mac = hub.sys('uci get network.wan.macaddr')[0]
# '00:23:6A:C0:5C:30'
log.debug('Got the hubs mac:{0}'.format(hub.mac))

# Run a remote command to the addresses of all the SATs...
all_sat_addrs = hub.sys("cat /tmp/mesh/topology.json | jq -r '.Hosts | map(select(.Role == \"SAT\")) | .[0].Address'", code=0)
# By default the sys(listformat=True) so lines are returned in an array. If a raw buffer is returned you may need
# to trim return/newline chars. etc
# ['192.168.69.201', '192.168.69.101']
log.debug('Got Sats:{0}'.format(",".join(all_sat_addrs)))


# Create ssh connection objects to private addresses using the HUB as an ssh bastion proxy...
sats = []
for sat_addr in all_sat_addrs:
    log.debug('Creating ssh connection to sat:{0}'.format(sat_addr))
    new_sat = SshConnection(sat_addr, password='sat_pass', proxy=hub.host, proxy_password=hub.password)
    # Run a command on one of the SATs to get it's mac
    new_sat.mac = new_sat.sys('uci get network.wan.macaddr')[0]
    # '3C:90:66:F8:BE:80'
    sats.append(new_sat)


img = 'smartos.img'
# Download a file (ie /etc/hosts) from the hub, rename it to pretend it's a firmware image..
hub.scp.get('/etc/hosts', img)

# Upload software to all the sats (this is better done with threads/sub processes, see remote_commands.py example)
# Do a fake upgrade...
rg_path = 'tmp/{0}'.format(img)
try:
    for sat in sats:
        sat.scp.put(img, rg_path)
    for sat in sats:
        out = sat.sys('echo "I could be upgrading to this {0}"'.format(rg_path), code=0)
        log.debug('Upgrade succeeded with output:{0}'.format("\n".join(out)))
        #sat.sys('sysupgrade {0}'.format(rg_path), code=0)
except Exception as E:
    log.critical('Failed to upgrade sat:{0}:{1}, err:{2}'.format(sat.host, sat.mac, E))
    raise E



