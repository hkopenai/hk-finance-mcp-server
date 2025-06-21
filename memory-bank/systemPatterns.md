# System Patterns

## System Architecture
The HK Finance MCP Server is designed as a Model Context Protocol (MCP) server, focusing on providing financial data and services specific to Hong Kong. The architecture follows a modular structure to facilitate the integration of various financial tools within the MCP ecosystem:
- **Core Server Module**: Handles the primary MCP server functionality using the FastMCP library, managing tool registration, request routing, and response handling through functions defined in 'server.py'.
- **Tool Modules**: Individual modules for each financial data tool:
  - **Business Registration (`tool_business_reg.py`)**: Fetches and processes business return data from IRD Hong Kong CSV files, with filtering by year and month.
  - **Credit Card Information (`tool_credit_card.py`)**: Retrieves credit card lending survey data and loss reporting hotlines from HKMA APIs, with quarterly data filtering.
  - **Coin Cart Schedule (`tool_coin_cart.py`)**: Fetches coin cart schedule data from HKMA API, providing location and timing details without filtering options.
  - **HKMA Tender (`tool_hkma_tender.py`)**: Handles tender invitations and notices from HKMA API, supporting pagination and date range filtering.
  - **Negative Resident Mortgage (`tool_neg_resident_mortgage.py`)**: Fetches negative equity mortgage statistics from HKMA API, with quarterly data filtering by year and month.
  Each module encapsulates specific data fetching and processing logic, allowing for independent development and updates.
- **Data Access Layer**: Abstracts the data retrieval mechanisms, interfacing with external APIs or data sources (e.g., IRD Hong Kong CSV files, HKMA JSON APIs) to fetch financial information using standard Python libraries like `urllib.request`.
- **Integration Layer**: Ensures compatibility with MCP standards, enabling seamless communication with other MCP servers and clients through standardized tool definitions and input schemas using Pydantic for validation.

## Key Technical Decisions
- **Modular Design**: Opted for a modular approach to tool development to enhance maintainability and scalability. Each financial tool is encapsulated in its own module, reducing interdependencies.
- **Python Implementation**: Chose Python as the primary programming language due to its extensive library support for web development, data processing, and API interactions, which are crucial for financial data handling.
- **MCP Compliance**: Ensured that the server adheres to MCP specifications for tool and resource exposure, facilitating integration with other systems in the MCP ecosystem.
- **Testing Framework**: Incorporated a robust unit testing suite using the `unittest` framework to validate tool functionality and data accuracy, critical for financial applications where errors can have significant consequences. Tests cover data fetching, filtering, and error handling with mocked external dependencies.

## Design Patterns in Use
- **Factory Pattern**: Used for creating tool instances dynamically based on user requests, allowing the server to instantiate the appropriate financial tool without hardcoding dependencies.
- **Singleton Pattern**: Applied to the core server configuration to ensure a single point of access to server-wide settings and resources.
- **Adapter Pattern**: Employed in the data access layer to standardize interactions with diverse external financial data sources, converting their responses into a uniform format for internal processing.
- **Observer Pattern**: Considered for future implementation to notify subscribed clients of updates to financial data, enhancing real-time data delivery capabilities.

## Component Relationships
- **Server to Tools**: The core server module in 'server.py' acts as the entry point, delegating requests to specific tool modules (e.g., `tool_business_reg.py`, `tool_credit_card.py`, `tool_hkma_tender.py`) based on the MCP tool name specified in the request.
- **Tools to Data Access**: Each tool module interacts with the data access layer to retrieve or process financial data, ensuring separation of concerns between business logic (e.g., data filtering by date ranges, formatting quarterly data) and data fetching.
- **Data Access to External Sources**: The data access layer connects to external APIs or data sources (e.g., public CSV files from IRD for business data, JSON APIs from HKMA for credit card, coin cart, tender, and mortgage data), handling request formatting and response parsing without additional authentication in most cases.
- **Integration Layer**: Wraps the entire system, providing the MCP interface that clients interact with, ensuring that all communications conform to MCP protocols through tool decorators and schema definitions.

## Critical Implementation Paths
- **Request Handling Flow**: Client request → MCP Integration Layer → Core Server Module (`server.py`) → Specific Tool Module (e.g., `tool_business_reg.py`) → Data Access Layer → External Data Source (e.g., IRD CSV, HKMA API) → Reverse path for response delivery with formatted data.
- **Tool Registration**: During server startup, each tool is registered with the core server in 'server.py' using `@mcp.tool` decorators, providing metadata about the tools (e.g., input schemas with Pydantic fields, descriptions) to be exposed via MCP.
- **Error Handling**: Implemented across all layers to catch and log errors, ensuring that failures in data retrieval or processing are communicated back to the client in a standardized MCP error format, though specific implementations vary by tool.
- **Security Measures**: Currently, minimal security measures are evident in the data access layer as most data sources are public; future updates may integrate authentication and data encryption to protect sensitive financial information during transmission if non-public sources are added.

## SWOT Analysis
- **Strengths**:
  - **Modular Architecture**: The separation of concerns with distinct tool modules enhances maintainability and scalability, allowing independent updates to financial data tools.
  - **Robust Unit Testing**: Comprehensive test coverage for each tool module using `unittest` and mocking ensures reliability in data processing and filtering, critical for financial data accuracy.
  - **MCP Compliance**: Adherence to MCP standards facilitates seamless integration with other systems, increasing the server's utility in broader ecosystems.
  - **Python Ecosystem**: Leveraging Python's extensive libraries simplifies interactions with diverse data sources (CSV, JSON APIs), speeding up development.
- **Weaknesses**:
  - **Minimal Security Measures**: Current reliance on public data sources without robust authentication or encryption could pose risks if sensitive data sources are integrated in the future.
  - **Limited Error Handling Specificity**: While error handling exists, it varies by tool, potentially leading to inconsistent user experiences during failures.
  - **Incomplete Documentation**: Although core documentation is in place, detailed technical and tool-specific documentation is still needed for full transparency.
- **Opportunities**:
  - **Expansion of Data Sources**: Potential to integrate additional Hong Kong financial data sources or non-public APIs, enhancing the server's scope and value.
  - **Security Enhancements**: Implementing advanced security protocols (e.g., OAuth, data encryption) could prepare the server for handling sensitive data, broadening its applicability.
  - **Real-Time Data Updates**: Adopting patterns like the Observer Pattern for real-time notifications could improve user experience in dynamic financial environments.
  - **User Feedback Integration**: Developing mechanisms for user feedback on tool performance could guide iterative improvements and feature prioritization.
- **Threats**:
  - **Data Source Reliability**: Dependence on external public APIs or data files (e.g., IRD, HKMA) risks service disruption if these sources change formats, become unavailable, or impose rate limits.
  - **Scalability Challenges**: Increased user demand or data volume could strain current architecture if not optimized for high traffic, impacting performance.
  - **Regulatory Compliance**: Evolving financial data regulations in Hong Kong may require significant updates to ensure compliance, especially if handling personal or sensitive data.
  - **Competitive Landscape**: Other financial data platforms or MCP servers could offer similar or superior services, reducing the project's unique value proposition if not continuously innovated.

## Revision History
- **Initial Draft**: June 18, 2025 - Creation of the system patterns document to outline the architecture and design decisions for the HK Finance MCP Server.
- **Update 1**: June 18, 2025 - Refined content with specific implementation details after reviewing codebase, focusing on tool modules, data access methods, and MCP integration specifics.
- **Update 2**: June 18, 2025 - Added details on unit testing framework and included a SWOT analysis to evaluate strengths, weaknesses, opportunities, and threats of the system architecture.
- **Update 3**: June 18, 2025 - Expanded tool module descriptions in system architecture and component relationships with detailed functionality for credit card, coin cart, and negative resident mortgage tools after completing codebase analysis.
