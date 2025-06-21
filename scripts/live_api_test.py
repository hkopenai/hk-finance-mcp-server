import sys
import os
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"live_api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the project root to the path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from hkopenai.hk_finance_mcp_server.tool_business_reg import fetch_business_returns_data
    from hkopenai.hk_finance_mcp_server.tool_credit_card import fetch_credit_card_data
    from hkopenai.hk_finance_mcp_server.tool_coin_cart import fetch_coin_cart_schedule
    from hkopenai.hk_finance_mcp_server.tool_hkma_tender import fetch_tender_invitations
    from hkopenai.hk_finance_mcp_server.tool_neg_resident_mortgage import fetch_neg_equity_data
except ImportError as e:
    logger.error(f"Failed to import tool modules: {e}")
    sys.exit(1)

def test_business_reg():
    """Test fetching business registration data."""
    logger.info("Testing Business Registration Data Fetch...")
    try:
        # Fetch data with default parameters
        data = fetch_business_returns_data()
        logger.info(f"Successfully fetched Business Registration data. Sample: {data[:200]}...")
        assert True
    except Exception as e:
        logger.error(f"Error fetching Business Registration data: {e}")
        assert False, f"Error fetching Business Registration data: {e}"

def test_credit_card():
    """Test fetching credit card data."""
    logger.info("Testing Credit Card Data Fetch...")
    try:
        # Fetch data with a specific time range (recent one for test)
        data = fetch_credit_card_data(start_year=2023, start_month=1, end_year=2023, end_month=12)
        logger.info(f"Successfully fetched Credit Card data. Sample: {data[:200]}...")
        assert True
    except Exception as e:
        logger.error(f"Error fetching Credit Card data: {e}")
        assert False, f"Error fetching Credit Card data: {e}"

def test_coin_cart():
    """Test fetching coin cart schedule data."""
    logger.info("Testing Coin Cart Schedule Data Fetch...")
    try:
        data = fetch_coin_cart_schedule()
        logger.info(f"Successfully fetched Coin Cart data. Sample: {str(data)[:200]}...")
        assert True
    except Exception as e:
        logger.error(f"Error fetching Coin Cart data: {e}")
        assert False, f"Error fetching Coin Cart data: {e}"

def test_hkma_tender():
    """Test fetching HKMA tender data."""
    logger.info("Testing HKMA Tender Data Fetch...")
    try:
        # Fetch data with pagination
        data = fetch_tender_invitations(pagesize=10, offset=0)
        logger.info(f"Successfully fetched HKMA Tender data. Sample: {data[:200]}...")
        assert True
    except Exception as e:
        logger.error(f"Error fetching HKMA Tender data: {e}")
        assert False, f"Error fetching HKMA Tender data: {e}"

def test_neg_resident_mortgage():
    """Test fetching negative equity resident mortgage data."""
    logger.info("Testing Negative Equity Resident Mortgage Data Fetch...")
    try:
        # Fetch data for a recent time range
        data = fetch_neg_equity_data(start_year=2023, start_month=1, end_year=2023, end_month=12)
        logger.info(f"Successfully fetched Negative Equity Mortgage data. Sample: {data[:200]}...")
        assert True
    except Exception as e:
        logger.error(f"Error fetching Negative Equity Mortgage data: {e}")
        assert False, f"Error fetching Negative Equity Mortgage data: {e}"

def main():
    """Execute live API tests for all financial tool modules."""
    logger.info("Starting Live API Verification for HK Finance MCP Server Tools")
    results = {}
    
    test_functions = {
        "Business Registration": test_business_reg,
        "Credit Card Data": test_credit_card,
        "Coin Cart Schedule": test_coin_cart,
        "HKMA Tender": test_hkma_tender,
        "Negative Equity Mortgage": test_neg_resident_mortgage
    }
    
    for tool, test_func in test_functions.items():
        try:
            test_func()
            results[tool] = True
        except AssertionError as e:
            logger.error(f"Test failed for {tool}: {e}")
            results[tool] = False
    
    # Summary of results
    logger.info("Live API Test Summary:")
    for tool, success in results.items():
        status = "SUCCESS" if success else "FAILURE"
        logger.info(f"  - {tool}: {status}")
    
    logger.info("Live API Verification Completed")

if __name__ == "__main__":
    main()
