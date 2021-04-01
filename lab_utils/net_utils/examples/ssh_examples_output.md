### Example showing verbose logging prefixed by each node as well as the primary script for filtering in a pipeline later...
```
~/python_workspace/labmix/examples$ python ssh_examples.py -i 192.168.69.1 -p ninja

[2021-03-31 12:10:12,833][DEBUG][EXAMPLE_SCRIPT]: Creating an ssh session to my hub:192.168.69.1
[2021-03-31 12:10:12,833][DEBUG][192.168.69.1]: SSH connection has hostname:192.168.69.1 user:root password:n***a
[2021-03-31 12:10:12,962][DEBUG][192.168.69.1]: SSH connection attempt(1 of 2), host:'root@192.168.69.1', using ipv4:192.168.69.1, thru proxy:'None'
[2021-03-31 12:10:12,987][DEBUG][192.168.69.1]: SSH - Connected to 192.168.69.1
[2021-03-31 12:10:13,050][DEBUG][EXAMPLE_SCRIPT]: Got the hubs mac:00:23:6A:C0:5C:30
[2021-03-31 12:10:13,130][DEBUG][EXAMPLE_SCRIPT]: Got Sats:192.168.69.201
[2021-03-31 12:10:13,130][DEBUG][EXAMPLE_SCRIPT]: Creating ssh connection to sat:192.168.69.201
[2021-03-31 12:10:13,130][DEBUG][192.168.69.201]: SSH connection has hostname:192.168.69.201 user:root password:n***a
[2021-03-31 12:10:13,130][DEBUG][192.168.69.201]: SSH proxy has hostname:192.168.69.1 user:root password:n***a
PRoxy connect using password:ninja username:root
[2021-03-31 12:10:13,473][DEBUG][192.168.69.201]: SSH connection attempt(1 of 2), host:'root@192.168.69.201', using ipv4:192.168.69.201, thru proxy:'192.168.69.1'
[2021-03-31 12:10:13,507][DEBUG][192.168.69.201]: SSH - Connected to 192.168.69.201 via proxy host:192.168.69.1:22
[2021-03-31 12:10:13,879][DEBUG][192.168.69.201]: [root@192.168.69.201]# echo "Hello from 3C:90:66:F8:BE:80"; ls /tmp/smartos_fake.img
[2021-03-31 12:10:13,961][DEBUG][192.168.69.201]: 
b'Hello from 3C:90:66:F8:BE:80\r\n\x1b[0;0m/tmp/smartos_fake.img\x1b[m\r\n'
[2021-03-31 12:10:13,962][DEBUG][192.168.69.201]: done with exec
[2021-03-31 12:10:13,962][DEBUG][EXAMPLE_SCRIPT]: Command on host:192.168.69.201 succeeded with output:
Hello from 3C:90:66:F8:BE:80
/tmp/smartos_fake.img

[2021-03-31 12:12:34,302][WARNING][EXAMPLE_SCRIPT]: Setting up the next one to fail...!

[2021-03-31 12:10:13,962][DEBUG][192.168.69.1]: [root@192.168.69.1]# echo "Hello from 00:23:6A:C0:5C:30"; ls /tmp/smartos_fake.img_bad_file
[2021-03-31 12:10:14,025][DEBUG][192.168.69.1]: 
b'Hello from 00:23:6A:C0:5C:30\r\nls: /tmp/smartos_fake.img_bad_file: No such file or directory\r\n'
[2021-03-31 12:10:14,025][DEBUG][192.168.69.1]: done with exec
[2021-03-31 12:10:14,025][DEBUG][192.168.69.1]: ['Hello from 00:23:6A:C0:5C:30', 'ls: /tmp/smartos_fake.img_bad_file: No such file or directory']
[2021-03-31 12:10:14,025][CRITICAL][EXAMPLE_SCRIPT]: Command failed on rg:192.168.69.1:00:23:6A:C0:5C:30,
 err:'Cmd:echo "Hello from 00:23:6A:C0:5C:30"; ls /tmp/smartos_fake.img_bad_file failed with status code:1, output:[\'Hello from 00:23:6A:C0:5C:30\', \'ls: /tmp/smartos_fake.img_bad_file: No such file or directory\']'
Traceback (most recent call last):
  File "/Users/mattclark/python_workspace/labmix/examples/ssh_examples.py", line 86, in <module>
    raise E
  File "/Users/mattclark/python_workspace/labmix/examples/ssh_examples.py", line 79, in <module>
    out = rg.sys('echo "Hello from {0}"; ls {1}'.format(rg.mac, rg_path), code=0, verbose=1)
  File "/Users/mattclark/python_workspace/labmix/lab_venv/lib/python3.9/site-packages/labmix-1.0.0-py3.9.egg/lab_utils/net_utils/sshconnection.py", line 427, in sys
    raise CommandExitCodeException('Cmd:' + str(cmd) + ' failed with status code:' +
lab_utils.net_utils.sshconnection.CommandExitCodeException: 
'Cmd:echo "Hello from 00:23:6A:C0:5C:30"; 
ls /tmp/smartos_fake.img_bad_file failed with status code:1, 
output:[\'Hello from 00:23:6A:C0:5C:30\', \'ls: /tmp/smartos_fake.img_bad_file: No such file or directory\']'
```