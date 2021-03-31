### INSTALL 
 sudo apt install python3-pip
 sudo apt-get install python3-venv
 pip3 install ipython

 python3 -m venv lab_venv
 source lab_venv/bin/activate
 python3 setup.py install

### Test the install with ipython
(lab_venv) mclark@ace: [labmix… main|✚1…49] # ipython
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

### Use tab complete to see options within the libs
In [1]: from lab_utils.<tab tab>
                        file_utils   net_utils   
                        log_utils    system_utils

In [2]: cpe = SshConnection('10.30.0.10', password='pass123')

### Use tab complete to see options within an obj...
In [3]: cpe.<tab tab>
  banner_timeout               cmd_not_executed_code        debug()                      get_proxy_transport()         
  close()                      cmd_timeout_err_code         debug_connect                get_ssh_connection()          
  close_sftp()                 connection                   enable_ipv6_dns              host                         >
  cmd()                        create_http_fwd_connection() find_keys                    http_fwd_request()            

### Use '?' to get additional info on a function or method...
 In [3]: cpe.cmd?

    ['status'] - The exitcode of the command. Note in the case a call back fires, this
                 exitcode is unreliable.
    ['cbfired']  - Boolean to indicate whether or not the provided callback fired
                  (ie returned False)
    ['elapsed'] - Time elapsed waiting for command loop to end.
Arguments:
:param cmd: - mandatory - string representing the command to be run  against the
              remote ssh session
:param verbose: - optional - will default to global setting, can be set per cmd() as
                  well here
:param timeout: - optional - integer used to timeout the overall cmd() operation in
                  case of remote blocking
:param listformat: - optional - boolean, if set returns output as list of lines, else a
                     single buffer/string
:param cb: - optional - callback, method that can be used to handle output as it's rx'd
            instead of waiting for the cmd to finish and return buffer.
            Called like: cb(ssh_cmd_out_buffer, *cbargs)
            Must accept string buffer, and return an integer to be used as cmd status.
            Must return type 'sshconnection.SshCbReturn'
            If cb returns stop, recv loop will end, and channel will be closed.
            if cb settimer is > 0, timer timeout will be adjusted for this time
            if cb statuscode is != -1 cmd status will return with this value
            if cb nextargs is set, the next time cb is called these args will be passed
            instead of cbargs
:param cbargs: - optional - list of arguments to be appended to output buffer and
                 passed to cb
:param get_pty: Request a pseudo-terminal from the server.
:param invoke_shell: Request a shell session on this channel
:param enable_debug: - optional - boolean, if set will use self.debug() to print
                       additional messages during cmd()
:param check_alive - optional - bool, If true will check if the transport is alive,
                     and re-establish it if not before attempting to send the command.
File:      ~/python_stuff/labmix/lab_utils/net_utils/sshconnection.py
Type:      method


### see Examples dir for additional usage examples. 
