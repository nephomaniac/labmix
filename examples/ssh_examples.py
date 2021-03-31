#!/usr/bin/env python3

# Intended to show examples of the SshConnection Class
# Usage ./ssh_examples.py -i 172.20.4.123 -p pass123


# import the SshConnection and LabLogger classes...
from lab_utils.net_utils.sshconnection import SshConnection
from lab_utils.log_utils.lablogger import LabLogger
import argparse

#Get some cli args first...
parser = argparse.ArgumentParser(
    description='Sample to show ssh usage...',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Set a default hub addr, this can be the WAN or LAN addr
parser.add_argument('-i','--hubip', default=None, 
        help='Provide the wan or lan IP of the hub to connect to', required=True)
parser.add_argument('-p','--password', default=None, help='Provide hub ssh password', required=True)
parser.add_argument('-u','--user', default='root', help='Provide ssh username')


args = parser.parse_args()
hubip = args.hubip 
hubpass = args.password
hubuser = args.user


#Create a logging instance...
log = LabLogger('EXAMPLE_SCRIPT')



# Create ssh connection objects...
# Example ssh to an RG's WAN addr...
log.debug('Creating an ssh session to my hub:{0}'.format(hubip))
hub = SshConnection(hubip, password=hubpass, username=hubuser, verbose=True)

# Run a command to get the mac
hub.mac = hub.sys('uci get network.wan.macaddr')[0]
# '00:23:6A:C0:5C:30'
log.debug('Got the hubs mac:{0}'.format(hub.mac))


# Run a remote command to discover all the addresses of the SATs behind this HUB...
all_sat_addrs = hub.sys("cat /tmp/mesh/topology.json | jq -r '.Hosts | map(select(.Role == \"SAT\")) | .[0].Address'", code=0)
# By default the sys(listformat=True) so lines are returned in an array. If a raw buffer is returned you may need
# to trim return/newline chars. etc
# ['192.168.69.201', '192.168.69.101']
log.debug('Got Sats:{0}'.format(",".join(all_sat_addrs)))


# Create ssh connection objects to private addresses using the HUB as an ssh bastion proxy...
sats = []
for sat_addr in all_sat_addrs:
    log.debug('Creating ssh connection to sat:{0}'.format(sat_addr))
    # Assume the sats use the same password as the hub here...
    new_sat = SshConnection(sat_addr, password=hub.password, proxy=hub.host, proxy_password=hub.password, verbose=True)
    # Run a command on one of the SATs to get it's mac
    new_sat.mac = new_sat.sys('uci get network.wan.macaddr')[0]
    # '3C:90:66:F8:BE:80'
    sats.append(new_sat)


fake_img_name = 'smartos_fake.img'
# Download a file (ie /etc/hosts) from the hub, rename it to pretend it's a firmware image..
hub.scp.get(remote_path='/etc/hosts/', local_path=fake_img_name)

# Upload software to all the sats (this is better done with threads/sub processes, see remote_commands.py example)
rg_path = '/tmp/{0}'.format(fake_img_name)
rgs = sats
rgs.append(hub)
try:
    for rg in rgs:
        rg.scp.put(fake_img_name, rg_path)
    for rg in rgs:
        # Run a command with verbose to show per IP logging...
        out = rg.sys('echo "Hello from {0}"; ls {1}'.format(rg.mac, rg_path), code=0, verbose=1)
        # Fake fail the next time around...
        log.debug('Command on host:{0} succeeded with output:\n{1}\n'.format(rg.host, "\n".join(out)))
        rg_path += "_bad_file"
        log.warning('Setting up the next one to fail...!')
except Exception as E:
    log.critical('Command failed on rg:{0}:{1},\n err:{2}'.format(rg.host, rg.mac, E))
    raise E



