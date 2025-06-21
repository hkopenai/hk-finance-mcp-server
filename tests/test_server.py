import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server.server import create_mcp_server
from hkopenai.hk_finance_mcp_server.tool_business_reg import get_business_stats

def create_tool_decorator(expected_name, decorated_func_container):
    """Create a tool decorator that only matches functions with the expected name.
    
    Args:
        expected_name: The function name to match
        decorated_func_container: List to store the matched function
    """
    def tool_decorator(description=None):
        def decorator(f):
            if f.__name__ == expected_name:
                decorated_func_container.append(f)
            return f
        return decorator
    return tool_decorator

class TestApp(unittest.TestCase):

    
    @patch('hkopenai.hk_finance_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_finance_mcp_server.app.tool_business_reg')
    def test_create_mcp_server(self, tool_business_reg, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
        # Track decorator calls and capture decorated function
        decorated_func = []
        
        tool_decorator = create_tool_decorator('get_business_stats', decorated_func)
            
        mock_server.tool = tool_decorator
        mock_server.tool.call_args = None  # Initialize call_args
        mock_fastmcp.return_value = mock_server
        tool_business_reg.get_business_stats.return_value = {'test': 'data'}

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tool was decorated
        self.assertIsNotNone(decorated_func)
        
        # Test the actual decorated function
        result = decorated_func[0]()
        tool_business_reg.get_business_stats.assert_called_once_with(None, None, None, None)
        

if __name__ == "__main__":
    unittest.main()
