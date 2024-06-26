![Scheme](icon.jpg)

### INSTALL 
```
See the 'install_helper.sh script for installing these libs and environment. 
```
### Validating an installation
Try running the test.py script to do a basic validation that the libs, and virtual env have been 
installed correctly...

source <virt env name>/bin/activate
python test.py 
Example:
```
mclark@delldude: [labmix… main|…47] # source labmix_venv/bin/activate

(labmix_venv) mclark@delldude: [labmix… main|…47] # python test.py 
[04-01 13:21:20][INFO][LabmixInstallTests]: 
               TEST CASE INFO              
 +------------------+--------------------+ 
 | NAME             | LabmixInstallTests | 
 | TEST LIST        | []                 | 
 | ENVIRONMENT FILE | None               | 
 +------------------+--------------------+ 

[04-01 13:21:20][INFO][LabmixInstallTests]: 
+------------------+----------------------------------+
| TEST ARGS        | VALUE                            |
+------------------+----------------------------------+
| configsections   | ['LabmixInstallTests', 'global'] |
| cpe_type         | smartos                          |
| dry_run          | False                            |
| environment_file | None                             |
| gw_cpe           | None                             |
| log_file         | None                             |
| log_file_level   | DEBUG                            |
| log_level        | DEBUG                            |
| no_clean         | False                            |
| password         | None                             |
| ssh_user         | root                             |
| test_list        | None                             |
| test_regex       | None                             |
+------------------+----------------------------------+

[04-01 13:21:20][DEBUG][LabmixInstallTests]: Creating TestUnit: "test1_imports_worked" with args:
[04-01 13:21:20][DEBUG][LabmixInstallTests]: Attempting to populate testunit:test1_imports_worked, with testcase.args...
[04-01 13:21:20][DEBUG][LabmixInstallTests]: Testunit keyword args:{}
[04-01 13:21:20][DEBUG][LabmixInstallTests]: Got method args:('self',)
[04-01 13:21:20][DEBUG][LabmixInstallTests]: test unit total args:{}
[04-01 13:21:20][INFO][test1_imports_worked]: 
---------------------------------------------------------------------------------------------------------------
 +-----------------------------------------------------------------------------------------------------------+ 
 | STARTING TESTUNIT: test1_imports_worked                                                                   | 
 | METHOD:test1_imports_worked, TEST DESCRIPTION:                                                            | 
 | None                                                                                                      | 
 | End on Failure:False                                                                                      | 
 | Passing ARGS:""                                                                                           | 
 | Running test method: "test1_imports_worked()"                                                             | 
 +-----------------------------------------------------------------------------------------------------------+ 
---------------------------------------------------------------------------------------------------------------

[04-01 13:21:20][DEBUG][test1_imports_worked]: You made it, install looks good!
[04-01 13:21:20][INFO][test1_imports_worked]: 
----------------------------------------------------------------------------------------------------------------
                               - SUCCESS -  TEST:"test1_imports_worked" COMPLETE                                
----------------------------------------------------------------------------------------------------------------

[04-01 13:21:20][DEBUG][LabmixInstallTests]: 
LATEST RESULTS:                                
-----------------------------------------------
  TOTAL   FAILED   NOT_RUN   PASSED   ELAPSED  
-----------------------------------------------
    1       0         0        1         0     
-----------------------------------------------

[04-01 13:21:20][DEBUG][LabmixInstallTests]: Printing pre-cleanup results:
[04-01 13:21:20][INFO][LabmixInstallTests]: Test list results for testcase:LabmixInstallTests

passed:1 failed:0 not_run:0 total:1

```

## Note: If missing modules/imports fail. Check python versions and paths to make sure things are lined up 
Example of python executables and paths not lining up everywhere notice 3.8 vs 3.9...
```
(lab_venv) mattclark@Matts-MacBook-Pro:~/python_workspace/labmix$ python
Python 3.9.2 (v3.9.2:1a79785e3e, Feb 19 2021, 09:06:10) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

(lab_venv) mclark@ace: [labmix… main|✚1…49] # ipython
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.
(lab_venv) mattclark@Matts-MacBook-Pro:~/python_workspace/labmix$ which python
/Users/mattclark/python_workspace/labmix/lab_venv/bin/python

(lab_venv) mattclark@Matts-MacBook-Pro:~/python_workspace/labmix$ which ipython
/Users/mattclark/python_workspace/labmix/lab_venv/bin/ipython
```
Make sure your python and ipython executable are running from the same 'python' as your
venv. Make sure the paths are using your venv libs/ dir... 

Example where my venv is 'lab_venv'...
(lab_venv) mclark@ace: [lab_venv… main ↓·10|…50] # ls lib/python3.8/site-packages

/home/mclark/python_stuff/labmix/lab_venv/lib/python3.8/site-package


Now check sys.path from python and then ipython. Example...
```
(lab_venv) mclark@ace: [lab_venv… main ↓·10|…50] # which ipython
/home/mclark/python_stuff/labmix/lab_venv/bin/ipython
(lab_venv) mclark@ace: [lab_venv… main ↓·10|…50] # ipython
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import sys

In [2]: sys.path
Out[2]: 
['/home/mclark/python_stuff/labmix/lab_venv/bin',
 '/usr/lib/python38.zip',
 '/usr/lib/python3.8',
 '/usr/lib/python3.8/lib-dynload',
 '',
 '/home/mclark/python_stuff/labmix/lab_venv/lib/python3.8/site-packages',
 '/home/mclark/python_stuff/labmix/lab_venv/lib/python3.8/site-packages/labmix-1.0.0-py3.8.egg',
 ...
 ...
 '/home/mclark/.ipython']
```

If you path is incorrect, you can try to rm -rf your venv and start the steps above over by recreateing a venv. 
...and/or...
Try adjust the path in the venv/bin/activate bash script...


```
#store the old path
OLD_PYTHONPATH="$PYTHONPATH
export PYTHONPATH="</fullpath/my_venv/lib/pythonXYZ/site...>,$PYTHONPATH"

#in the deactivate()function restore your old path...
[ -n $OLD_PYTHONPATH ] && export export PYTHONPATH="$OLD_PYTHONPATH
```



## Test the install with ipython
### Use tab complete to see options within the libs
```
In [1]: from lab_utils.<tab tab>
                        file_utils   net_utils   
                        log_utils    system_utils
```

### Use tab complete to see options within an obj...
```
In [2]: cpe = SshConnection('10.30.0.10', password='pass123')
In [3]: cpe.<tab tab>
  banner_timeout               cmd_not_executed_code        debug()                      get_proxy_transport()         
  close()                      cmd_timeout_err_code         debug_connect                get_ssh_connection()          
  close_sftp()                 connection                   enable_ipv6_dns              host                         >
  cmd()                        create_http_fwd_connection() find_keys                    http_fwd_request()            
```
### Use '?' to get additional info on a function or method...
```
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
```

### see Examples dir for additional usage examples. 
