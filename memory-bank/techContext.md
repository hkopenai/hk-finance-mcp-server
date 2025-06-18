# Tech Context

## Technologies Used
- **Python**: The primary programming language for the HK Finance MCP Server, chosen for its robust support in web development, data processing, and API interactions, which are essential for handling financial data.
- **MCP Framework**: The Model Context Protocol framework, specifically using the FastMCP library, is used to structure the server, enabling standardized tool and resource exposure for integration with other MCP systems.
- **HTTP Libraries**: Standard library `urllib.request` for making API calls to external financial data sources in Hong Kong, such as IRD CSV files and HKMA JSON APIs.
- **Testing Frameworks**: The `unittest` framework for unit testing to ensure the reliability of financial data tools, with mocking via `unittest.mock` for simulating external API responses.
- **Documentation Tools**: Markdown for project documentation within the Memory Bank, ensuring accessible and consistent documentation.

## Development Setup
- **Version Control**: Git is used for version control, with a `.gitignore` file to manage files excluded from tracking.
- **Dependency Management**: Managed through `pyproject.toml`, which likely uses tools like Poetry or similar for Python dependency handling.
- **IDE Support**: VSCode is utilized for development, providing integration with Git, Python extensions, and Markdown preview for Memory Bank files.

## Technical Constraints
- **Data Source Availability**: Dependent on the availability and reliability of external financial data APIs or sources specific to Hong Kong, which may have rate limits or require authentication.
- **MCP Compliance**: Must adhere to MCP specifications for tool schemas and communication protocols, limiting flexibility in how tools are exposed or interact with clients.
- **Security Requirements**: Financial data handling necessitates strict security measures, including encryption and secure API interactions, to protect sensitive information.
- **Performance**: Needs to handle potentially high volumes of requests for financial data without significant latency, requiring optimization of data retrieval and processing.

## Dependencies
- **Internal Dependencies**: The project structure indicates dependencies between core server modules (`app.py`) and individual tool modules (e.g., `tool_business_reg.py`, `tool_credit_card.py`, `tool_hkma_tender.py`), managed within the `hkopenai/hk_finance_mcp_server` directory.
- **External Libraries**: Includes standard Python libraries like `urllib.request` for HTTP requests and `json` for parsing API responses. Testing is supported by `unittest` and `unittest.mock`. Additional dependencies are specified in `pyproject.toml`, likely managed by a tool like Poetry, potentially including Pydantic for input schema validation.
- **MCP Server Tools**: Relies on the broader MCP ecosystem for client interactions, requiring compatibility with MCP server libraries like FastMCP for Python, ensuring proper tool registration and request handling.

## Tool Usage Patterns
- **MCP Tool Execution**: Tools are executed via MCP calls, with each tool module (`tool_*.py`) defining specific input schemas using Pydantic fields (e.g., optional date filters for `tool_credit_card.py`, pagination for `tool_hkma_tender.py`) and returning structured JSON-compatible data as per MCP standards.
- **Testing Practices**: Each tool has corresponding test files in the `tests/` directory (e.g., `test_tool_business_reg.py`, `test_tool_credit_card.py`), following a pattern of comprehensive unit testing with `unittest`. Tests cover data fetching, filtering logic, and error handling using mocked API responses.
- **Documentation Updates**: Memory Bank files are updated following significant changes or user requests, using Markdown to maintain a clear record of project context and decisions.
- **File Management**: File operations (reading, writing, searching) are conducted using provided tools, ensuring that paths are correctly specified relative to the working directory.

## Revision History
- **Initial Draft**: June 18, 2025 - Creation of the tech context document to outline the technologies, setup, and constraints for the HK Finance MCP Server.
- **Update 1**: June 18, 2025 - Updated technologies used to reflect actual codebase libraries (`urllib.request` instead of `requests`, `unittest` instead of `pytest`), refined dependencies with specific library usage, and detailed tool usage patterns with input schema and testing specifics.
