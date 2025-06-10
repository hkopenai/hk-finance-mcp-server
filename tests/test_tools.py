import unittest
from tests.test_tool_business_reg import TestBusinessReturns
from tests.test_tool_credit_card import TestCreditCardLending
from tests.test_tool_neg_resident_mortgage import TestNegativeEquityMortgage

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestBusinessReturns))
    suite.addTests(loader.loadTestsFromTestCase(TestNegativeEquityMortgage))
    suite.addTests(loader.loadTestsFromTestCase(TestCreditCardLending))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
