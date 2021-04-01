from lab_utils.net_utils.sshconnection import SshConnection
from test_utils.cli_test_runner import CliTestRunner
import sys

class LabmixInstallTests(CliTestRunner):
    def test1_imports_worked(self):
        self.log.debug("You made it, install looks good!")

    def clean_method(self):
        self.log.debug("You made it, install looks good!")

if __name__ == "__main__":

    test = LabmixInstallTests()
    test.args.no_clean = True
    result = test.run()
    sys.exit(result)
