import unittest
import os

class TestExampleLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_example_live_test(self):
        """
        This is an example live test. Replace this with actual live test logic.
        """
        self.assertTrue(True, "Example live test passed.")

if __name__ == "__main__":
    unittest.main()
