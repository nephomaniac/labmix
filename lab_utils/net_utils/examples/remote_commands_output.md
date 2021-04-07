Example shows concurrent execution of commands against a list of IP addresses with individual logging, and status. 

~/python_workspace/labmix/examples$ python remote_commands.py -i 192.168.69.1,192.168.69.201 -c 'uci get network.wan.macaddr && ping -c1 192.168.69.1 ' -p ninja
```
[2021-03-31 11:47:25,676][DEBUG][RemoteCmds]: Thread: 0, in Q loop...
[2021-03-31 11:47:25,677][DEBUG][RemoteCmds]: Connecting to new host:192.168.69.1
[2021-03-31 11:47:25,677][DEBUG][192.168.69.1]: SSH connection has hostname:192.168.69.1 user:root password:n***a
[2021-03-31 11:47:25,677][DEBUG][192.168.69.1]: ssh_connect args:
hostname:192.168.69.1
username:root
password:ninja
keypath:None
proxy_username:root
proxy_passwordNone
proxy_keypathNone
timeout:5
retry:1
[2021-03-31 11:47:25,677][DEBUG][192.168.69.1]: IPV6 DNS lookup disabled, do IPV4 resolution and pass IP to connect()
[2021-03-31 11:47:25,677][DEBUG][RemoteCmds]: Thread: 1, in Q loop...
[2021-03-31 11:47:25,677][DEBUG][RemoteCmds]: Connecting to new host:192.168.69.201
[2021-03-31 11:47:25,677][DEBUG][192.168.69.201]: SSH connection has hostname:192.168.69.201 user:root password:n***a
[2021-03-31 11:47:25,677][DEBUG][192.168.69.201]: ssh_connect args:
hostname:192.168.69.201
username:root
password:ninja
keypath:None
proxy_username:root
proxy_passwordNone
proxy_keypathNone
timeout:5
retry:1
[2021-03-31 11:47:25,678][DEBUG][192.168.69.201]: IPV6 DNS lookup disabled, do IPV4 resolution and pass IP to connect()
[2021-03-31 11:47:25,678][DEBUG][RemoteCmds]: Threads started now waiting for join
[2021-03-31 11:47:25,810][DEBUG][192.168.69.1]: SSH connection attempt(1 of 2), host:'root@192.168.69.1', using ipv4:192.168.69.1, thru proxy:'None'
[2021-03-31 11:47:25,810][DEBUG][192.168.69.1]: Using username:root and password:n***a
[2021-03-31 11:47:25,832][DEBUG][192.168.69.1]: SSH - Connected to 192.168.69.1
[2021-03-31 11:47:25,833][DEBUG][192.168.69.1]: host: 192.168.69.1 running command:uci get network.wan.macaddr && echo ping -c1 192.168.69.1  
[2021-03-31 11:47:25,833][DEBUG][192.168.69.1]: [root@192.168.69.1]# uci get network.wan.macaddr && echo ping -c1 192.168.69.1 
[2021-03-31 11:47:25,864][DEBUG][192.168.69.201]: SSH connection attempt(1 of 2), host:'root@192.168.69.201', using ipv4:192.168.69.201, thru proxy:'None'
[2021-03-31 11:47:25,864][DEBUG][192.168.69.201]: Using username:root and password:n***a
[2021-03-31 11:47:25,896][DEBUG][192.168.69.1]: 
b'00:23:6A:C0:5C:30\r\nping -c1 192.168.69.1\r\n'
[2021-03-31 11:47:25,897][DEBUG][192.168.69.1]: done with exec
[2021-03-31 11:47:25,897][DEBUG][192.168.69.1]: Done with host: 192.168.69.1
[2021-03-31 11:47:25,897][DEBUG][192.168.69.1]: Closing ssh to host: 192.168.69.1
[2021-03-31 11:47:25,897][DEBUG][192.168.69.1]: Closed ssh to host: 192.168.69.1
[2021-03-31 11:47:25,897][DEBUG][RemoteCmds]: Finished task in thread:0
[2021-03-31 11:47:25,897][DEBUG][RemoteCmds]: Thread: 0, in Q loop...
[2021-03-31 11:47:25,906][DEBUG][192.168.69.201]: SSH - Connected to 192.168.69.201
[2021-03-31 11:47:25,907][DEBUG][192.168.69.201]: host: 192.168.69.201 running command:uci get network.wan.macaddr && echo ping -c1 192.168.69.1  
[2021-03-31 11:47:25,907][DEBUG][192.168.69.201]: [root@192.168.69.201]# uci get network.wan.macaddr && echo ping -c1 192.168.69.1 
[2021-03-31 11:47:25,997][DEBUG][192.168.69.201]: 
b'3C:90:66:F8:BE:80\r\nping -c1 192.168.69.1\r\n'
[2021-03-31 11:47:25,997][DEBUG][192.168.69.201]: done with exec
[2021-03-31 11:47:25,997][DEBUG][192.168.69.201]: Done with host: 192.168.69.201
[2021-03-31 11:47:25,997][DEBUG][192.168.69.201]: Closing ssh to host: 192.168.69.201
[2021-03-31 11:47:25,997][DEBUG][192.168.69.201]: Closed ssh to host: 192.168.69.201
[2021-03-31 11:47:25,998][DEBUG][RemoteCmds]: Finished task in thread:1
[2021-03-31 11:47:25,998][DEBUG][RemoteCmds]: Thread: 1, in Q loop...
[2021-03-31 11:47:25,998][DEBUG][RemoteCmds]: Done with join
[2021-03-31 11:47:26,403][DEBUG][RemoteCmds]: Finished task in thread:0
[2021-03-31 11:47:26,403][DEBUG][RemoteCmds]: 0: Done with thread
[2021-03-31 11:47:26,501][DEBUG][RemoteCmds]: Finished task in thread:1
[2021-03-31 11:47:26,501][DEBUG][RemoteCmds]: 1: Done with thread
[2021-03-31 11:47:26,598][DEBUG][RemoteCmds]: Got terminal width: 140

+--------------+---+----+------------------------------------------------------------------------------------------------------------+
+--------------+---+----+------------------------------------------------------------------------------------------------------------+
|HOST          |RES|TIME|OUTPUT                                                                                                      |
+--------------+---+----+------------------------------------------------------------------------------------------------------------+
|192.168.69.1  |0  |0   |00:23:6A:C0:5C:30                                                                                           |
|              |   |    |PING 192.168.69.1 (192.168.69.1) 56(84) bytes of data.                                                      |
|              |   |    |64 bytes from 192.168.69.1: icmp_req=1 ttl=64 time=0.371 ms                                                 |
|              |   |    |--- 192.168.69.1 ping statistics ---                                                                        |
|              |   |    |1 packets transmitted, 1 received, 0% packet loss, time 0ms                                                 |
|              |   |    |rtt min/avg/max/mdev = 0.371/0.371/0.371/0.000 ms                                                           |
|              |   |    |                                                                                                            |
+--------------+---+----+------------------------------------------------------------------------------------------------------------+
|192.168.69.201|0  |0   |3C:90:66:F8:BE:80                                                                                           |
|              |   |    |PING 192.168.69.1 (192.168.69.1) 56(84) bytes of data.                                                      |
|              |   |    |64 bytes from 192.168.69.1: icmp_req=1 ttl=64 time=2.39 ms                                                  |
|              |   |    |--- 192.168.69.1 ping statistics ---                                                                        |
|              |   |    |1 packets transmitted, 1 received, 0% packet loss, time 0ms                                                 |
|              |   |    |rtt min/avg/max/mdev = 2.391/2.391/2.391/0.000 ms                                                           |
|              |   |    |                                                                                                            |
+--------------+---+----+------------------------------------------------------------------------------------------------------------+

```