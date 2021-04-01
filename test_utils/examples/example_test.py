from test_utils.cli_test_runner import CliTestRunner, SkipTestException
from lab_utils.net_utils.sshconnection import SshConnection
import copy
import sys

# Usage: python example_test.py -h

##################################################################################################
# Create the testcase (TestRunner) object                                                                     #
##################################################################################################
class ExampleTestSuite(CliTestRunner):

    #####################################################################################
    # Example of how to edit, add, remove the pre-baked cli arguments provided in the base
    # CliTestRunner class...
    #####################################################################################

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
    # By Default any method prefixed with 'test' is added and run by alpha_numeric order
    # 
    # However, any method be added to a test run list despite the methods name. 
    # newlist = [] 
    # newlist.append(self.create_testunit_from_method(
    #        self.some_method_not_starting_with_test, eof=True))
    #
    # Note: each testunits can specifiy whether the test suite should continue or exit by 
    # setting it's individual eof (end on failure) flag. eof can also be provided during 
    # run() to apply to all testsunits. 
    #
    # Then can be run by:
    #  <your_cli_test_runner_class>.run(testlist=newlist)
    #
    # When a test is run from the cli, --test-list can provide a comma delimited set 
    # test names to run which will also over write the default test list. 
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


#########################################################################################
# Specify what to do if called from the command line 
# (ie vs being sourced as a class from another file)
#########################################################################################

if __name__ == "__main__":
    
    # Create an instance of our testsuite class
    # this will provide all the cli -arg and --kwarg params handling for the user input
    test = ExampleTestSuite()
    
    ### Now Run the test suite, see cli_test_runner's run() method defintion and docstring
    # for more details. 
    # basic options for run(): testlist=None, eof=False, clean_on_exit=None, 
    #                          test_regex=None, printresults=True, force_dry_run=False
    result = test.run()
    
    #Always exit with the proper return code 
    sys.exit(result)
