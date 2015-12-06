

import logging
import os
import sys
import unittest


# Folder of the app to tests.
APP_DIR = os.path.join(os.path.dirname(__file__), 'app')
# Folder where test will be search.
TEST_DIR = os.path.join(os.path.dirname(__file__), 'tests')


##########################################################
# WARNING! GAE SDK folder needs to be on the PYTHONPATH. #
##########################################################
def fix_path():
    """
    Fix system path to import all GAE and app files during tests.
    """
    # Warning! GAE SDK folder needs to be on the PYTHONPATH.
    import dev_appserver

    # Fix the sys.path to include GAE extra paths.
    dev_appserver.fix_sys_path()

    # Adds app dir to the path.
    sys.path = [APP_DIR] + sys.path

    # This import adds libraries in libs to the path.
    import main

fix_path()
#######################################################
# Now we can import everything... ok, 'everything' ;) #
#######################################################

import webtest

from google.appengine.ext import testbed

import main


class AppEngineTestBase(unittest.TestCase):
    """
    Base class for AppEngine tests.
    """

    def setUp(self):
        # Create and activate Testbed to moock AppEngine APIs.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # TODO: mock services with self.testbed.init_X_stub()
        # Create app for testing handlers.
        self.testapp = webtest.TestApp(main.app)
        # Not showing logging.
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        self.testbed.deactivate()


def runAllTests():
    """
    Run all tests.
    """
    loader = unittest.TestLoader()
    test_suite = loader.discover(TEST_DIR, pattern='*')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    exit_code = not result.wasSuccessful()
    sys.exit(exit_code)


# If it's the main file we run all the tests under 'tests' module.
if __name__ == '__main__':
    runAllTests()
