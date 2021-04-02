#!/usr/bin/env python3

from lab_utils.net_utils.sshconnection import SshConnection

ip='192.168.1.1'
cpe = SshConnection(ip, password='yourpassword')
# The two main command interfaces are cmd() and sys().
#     cmd() returns a dict with details of the command's execution
#     sys() returns the commands output in either an array of lines or single buffer.
out = cpe.cmd('echo "Hello from host:{0}"'.format(cpe.host), verbose=True)

# print(out)
# {'cmd': 'echo "Hello from host:192.168.69.1"',
#  'output': 'Hello from host:192.168.69.1\r\n',
#  'status': 0,
#  'cbfired': False,
#  'elapsed': 0}


# Raise a command failure exception by providing the expected exit code of the command...
cpe.sys('echo "This cmd will fail"; ls no_file_here', code=0, verbose=True)
# Raise a command timeout exception by providing a timeout...
cpe.sys('echo "This cmd will timeout"; sleep 10', code=0, verbose=True, timeout=2)
