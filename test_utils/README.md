## Getting to know the cli_test_runner testcase classes...
Example using ipython (python CLI/shell):

# Output from the console...
```
(labmix_venv) mclark@delldude: [labmix… main|…47] # ipython
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from test_utils.example_test import ExampleTestSuite

In [2]: test = ExampleTestSuite(gw_cpe='192.168.69.1', ping_addr='192.168.69.222')
[03-31 23:23:04][INFO][ExampleTestSuite]: 
              TEST CASE INFO             
 +------------------+------------------+ 
 | NAME             | ExampleTestSuite | 
 | TEST LIST        | []               | 
 | ENVIRONMENT FILE | None             | 
 +------------------+------------------+ 

[03-31 23:23:04][INFO][ExampleTestSuite]: 
+------------------+--------------------------------+
| TEST ARGS        | VALUE                          |
+------------------+--------------------------------+
| configsections   | ['ExampleTestSuite', 'global'] |
| cpe_type         | smartos                        |
| dry_run          | False                          |
| environment_file | None                           |
| fake_arg         |                                |
| gw_cpe           | 192.168.69.1                   |
| log_file         | None                           |
| log_file_level   | DEBUG                          |
| log_level        | DEBUG                          |
| no_clean         | False                          |
| password         | None                           |
| ping_addr        | 192.168.69.222                 |
| ping_count       | 3                              |
| ssh_user         | admin                          |
| test_list        | None                           |
| test_regex       | None                           |
+------------------+--------------------------------+


In [3]: test.run()
...
...
-------------------------------------------------------------------------------------------------------------------
 ----------------------------------------------------------------------------------------------------------------- 
   TEST RESULTS FOR "ExampleTestSuite"                                                                             
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | PASSED                                                                                       |   
   | TEST NAME  | test1_example                                                                                |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test1_example()                                                                              |   
   | OUTPUT:    | None                                                                                         |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | PASSED                                                                                       |   
   | TEST NAME  | test2_example                                                                                |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test2_example()                                                                              |   
   | OUTPUT:    | None                                                                                         |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | FAILED                                                                                       |   
   | TEST NAME  | test3_example                                                                                |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test3_example()                                                                              |   
   | OUTPUT:    | ERROR:(Exception("Failure demonstrating a test failure"))                                    |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | NOT_RUN                                                                                      |   
   | TEST NAME  | test4_skip_example                                                                           |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test4_skip_example()                                                                         |   
   | OUTPUT:    | NOT_RUN (test4_skip_example:'Demonstrating a skipped test')                                  |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | FAILED                                                                                       |   
   | TEST NAME  | test5_ssh_gw                                                                                 |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test5_ssh_gw()                                                                               |   
   | OUTPUT:    | ERROR:(Exception("Missing --gw-cpe and --password args/values?"))                            |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | FAILED                                                                                       |   
   | TEST NAME  | test6_ping_from_gw_cpe                                                                       |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | test6_ping_from_gw_cpe()                                                                     |   
   | OUTPUT:    | ERROR:(Exception("We dont have a gw_cpe ssh object to test ping with?"))                     |   
 ----------------------------------------------------------------------------------------------------------------- 
   | RESULT:    | PASSED                                                                                       |   
   | TEST NAME  | clean_method                                                                                 |   
   | TIME:      | 0                                                                                            |   
   | TEST ARGS: | clean_method()                                                                               |   
   | OUTPUT:    | None                                                                                         |   
 ----------------------------------------------------------------------------------------------------------------- 
                                                                                                                   
                                                                                                                   
   LATEST RESULTS:                                                                                                 
   -----------------------------------------------                                                                 
     TOTAL   FAILED   NOT_RUN   PASSED   ELAPSED                                                                   
   -----------------------------------------------                                                                 
       7       3         1        3         0                                                                      
   -----------------------------------------------                                                                 
                                                                                                                   
                                                                                                                   
 ----------------------------------------------------------------------------------------------------------------- 
-------------------------------------------------------------------------------------------------------------------

passed:3 failed:3 not_run:1 total:7
```


## Sample test 'sample_testsuite.py' and it's output.



File: example_test.py

```
from test_utils.cli_test_runner import CliTestRunner, SkipTestException
from lab_utils.net_utils.sshconnection import SshConnection
import copy

# Usage: python example_test.py -h

##################################################################################################
# Create the testcase (TestRunner) object                                                                     #
##################################################################################################
class ExampleTestSuite(CliTestRunner):

    #####################################################################################
    # Example of how to edit, add, remove the pre-baked cli arguments provided in the base
    # CliTestRunner class...
    #####################################################################################

    # this can be set to {} to delete all, or any subset of the _DEFAULT_CLI_ARGS can be used
    # see ./example_test.py -h for all the cli args 
    _DEFAULT_CLI_ARGS = copy.copy(CliTestRunner._DEFAULT_CLI_ARGS)

    _DEFAULT_CLI_ARGS['gateway'] = {
        'args': ['--fake-arg'],
        'kwargs': {'help': 'This is a fake string argument',
                   'default': "",
                   'type': str}}

    _DEFAULT_CLI_ARGS['ping'] = {
        'args': ['--ping-addr'],
        'kwargs': {'help': 'Remote address to ping',
                   'default': "",
                   'type': str}}

    _DEFAULT_CLI_ARGS['ping_count'] = {
        'args': ['--ping-count'],
        'kwargs': {'help': 'Number of pings to send',
                   'default': 3,
                   'type': int}}

    #####################################################################################
    # Create the test methods...
    #####################################################################################

    def test1_example(self):
        """
        Attempts to set some stuff on this test suite object
        """
        self.log.debug('Assigning self.stuff="123"')
        setattr(self, 'stuff', '123')


    def test2_example(self):
        """
        Sample to show how tests can read from previous test values to determine state
        """
        if hasattr(self, 'stuff'):
            self.log.debug('Got stuff:{0}'.format(self.stuff))
        else:
            raise Exception('No stuff')

    def test3_example(self):
        """
        Sample to show what a failure looks like
        """
        raise Exception('Failure demonstrating a test failure')

    def test4_skip_example(self):
        """
        Sample to show how to show how a test can skip itself.
        """
        self.log.warning('Lets skip this test')
        raise SkipTestException('Demonstrating a skipped test')

    def test5_ssh_gw(self):
        """
        Sample test to show how cli args can be used by ssh'ing into a remote addr
        """
        if not self.args.gw_cpe or not self.args.password:
            raise Exception('Missing --gw-cpe and --password args/values?')
        gw_cpe = SshConnection(self.args.gw_cpe, username='root',
                            password=self.args.password, verbose=True, timeout=5)
        self.log.debug('Issuing uptime command on gw_cpe...')
        gw_cpe.sys('uptime', code=0, verbose=True)
        self.log.debug('Setting self.gw_cpe to new ssh obj')
        setattr(self, 'gw_cpe', gw_cpe)

    def test6_ping_from_gw_cpe(self):
        """
        Sample test, ping a remote addr from the gw_cpe using the
        provided --ping-addr and --ping-count values
        """
        if not self.args.ping_addr:
            raise SkipTestException('--ping-addr was not provided, skipping this test')
        if not hasattr(self, 'gw_cpe') or not self.gw_cpe:
            raise Exception('We dont have a gw_cpe ssh object to test ping with?')
        timeout = 1.5 * self.args.ping_count
        expected_exit_code = 0
        self.gw_cpe.sys('ping -c {0} {1}'.format(self.args.ping_count, self.args.ping_addr),
                        timeout=timeout, verbose=True, code=expected_exit_code)




    def clean_method(self):
        """
         This method should be implemented per Test Class. This method will be called by default
         during the test run method(s). 'no_clean_on_exit' set by cli '--no-clean' will prevent
         this default method from being called.
        """
        self.log.debug('Cleaning up after ourselves...')
        if hasattr(self, 'gw_cpe'):
            self.gw_cpe.close()


if __name__ == "__main__":

    test = ExampleTestSuite()
    result = test.run()
    exit(result)
```





## Running the test from the cli with provided parameters   ...

Run any cli_test_runner object with -h or --help to see all the available params...
```
(labmix_venv) mclark@delldude: [test_utils… main|…47] # python example_test.py  -h

usage: ExampleTestSuite [-h] [--password PASSWORD] [--cpe-type CPE_TYPE] [--gw-cpe GW_CPE] [--log-level LOG_LEVEL] [--ssh-user SSH_USER]
                        [--log-file LOG_FILE] [--log-file-level LOG_FILE_LEVEL] [--test-list TEST_LIST] [--test-regex TEST_REGEX]
                        [--environment-file ENVIRONMENT_FILE] [--dry-run [DRY_RUN]] [--no-clean] [--fake-arg FAKE_ARG]
                        [--ping-addr PING_ADDR] [--ping-count PING_COUNT]

CLI TEST RUNNER

optional arguments:
  -h, --help            show this help message and exit
  --password PASSWORD   Password to use for machine root ssh access
  --cpe-type CPE_TYPE   CPE Type to use in this test
  --gw-cpe GW_CPE       Address of the CPE acting as the gateway or hub
  --log-level LOG_LEVEL
                        log level for stdout logging
  --ssh-user SSH_USER   ssh user name to use with the gateway cpe
  --log-file LOG_FILE   file path to log to (in addition to stdout
  --log-file-level LOG_FILE_LEVEL
                        log level to use when logging to '--log-file'
  --test-list TEST_LIST
                        comma or space delimited list of test names to run
  --test-regex TEST_REGEX
                        regex to use when creating the list of local test methods to run.Will use this regex in a search of the method
                        name
  --environment-file ENVIRONMENT_FILE
                        Environment file that describes test topology
  --dry-run [DRY_RUN]   Prints test runlist info and exit. Default is json to stdout, see below for formats and location options. A higher
                        log level can also be provided to quiet down any other outputArgument format: json/yaml/labtest:filepathExample#:
                        json:/tmp/testinfo.json
  --no-clean            Flag, if provided will not run the clean method on exit
  --fake-arg FAKE_ARG   This is a fake string argument
  --ping-addr PING_ADDR
                        Remote address to ping
  --ping-count PING_COUNT
                        Number of pings to send
```

To run from the cli:
./example_test.py --gw-cpe '192.168.1.1' --password 'n****' --ping-addr '192.168.69.222'


## Use ipython or python shells to tab complete and '?' attributes and class methods of a cli_test_runner object...

```
(labmix_venv) mclark@delldude: [labmix… main|…47] # ipython
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from test_utils.cli_test_runner import CliTestRunner

In [2]: blanktest = CliTestRunner()
[04-01 08:14:10][INFO][CliTestRunner]: 
            TEST CASE INFO            
 +------------------+---------------+ 
 | NAME             | CliTestRunner | 
 | TEST LIST        | []            | 
 | ENVIRONMENT FILE | None          | 
 +------------------+---------------+ 

[04-01 08:14:10][INFO][CliTestRunner]: 
+------------------+-----------------------------+
| TEST ARGS        | VALUE                       |
+------------------+-----------------------------+
| configsections   | ['CliTestRunner', 'global'] |
| cpe_type         | smartos                     |
| dry_run          | False                       |
| environment_file | None                        |
| gw_cpe           | None                        |
| log_file         | None                        |
| log_file_level   | DEBUG                       |
| log_level        | DEBUG                       |
| no_clean         | False                       |
| password         | None                        |
| ssh_user         | admin                       |
| test_list        | None                        |
| test_regex       | None                        |
+------------------+-----------------------------+


In [3]: blanktest.
                    add_arg()                           create_testunit_by_name()           dump_test_info_labtest()            endsuccess()                        get_default_userhome_config()        
                    args                                create_testunit_from_method()       dump_test_info_yaml()               format_testunit_method_arg_values() get_meth_arg_names()                 
                    clean_method()                      do_with_args()                      endfailure()                        get_arg()                           get_method_fcode()                  >
                    config_file                         dump_test_info_json()               endnotrun()                         get_args()                          get_pretty_args()            
```
