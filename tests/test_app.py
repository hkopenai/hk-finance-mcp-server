import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_weather_mcp_server.app import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_weather_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_weather_mcp_server.app.tool_weather')
    def test_create_mcp_server(self, mock_tool_weather, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
        # Track decorator calls and capture decorated function
        decorator_calls = []
        decorated_func = None
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                nonlocal decorated_func
                decorated_func = f
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_server.tool.call_args = None  # Initialize call_args
        mock_fastmcp.return_value = mock_server
        mock_tool_weather.get_current_weather.return_value = {'test': 'data'}

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tool was decorated
        self.assertIsNotNone(decorated_func)
        
        # Test the actual decorated function
        result = decorated_func(region="test")
        mock_tool_weather.get_current_weather.assert_called_once_with("test")
        
        # Verify tool description was passed to decorator
        self.assertEqual(len(decorator_calls), 1)
        self.assertIsNotNone(decorator_calls[0][1]['description'])

if __name__ == "__main__":
    unittest.main()
