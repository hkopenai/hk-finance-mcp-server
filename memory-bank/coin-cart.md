# Coin Cart Data Tool Documentation

## Overview
The Coin Cart Data Tool is a component of the HK Finance MCP Server designed to fetch and process data related to coin cart collection schedules in Hong Kong. This tool provides essential information for financial institutions and businesses that rely on coin collection services provided by the Hong Kong Monetary Authority (HKMA).

## Purpose
This tool addresses the need for accurate scheduling and location data for coin cart services in Hong Kong. It enables users to:
- Retrieve current and upcoming coin cart collection schedules.
- Access location details and operational hours for coin collection points.
- Plan logistics around coin collection based on real-time data.

## Key Features
- **Data Retrieval**: Automatically fetches JSON data from the HKMA's open data portal.
- **Data Parsing**: Processes JSON data into a structured format for easy access and analysis.
- **Real-Time Updates**: Ensures the data reflects the latest schedules published by the HKMA.
- **Error Handling**: Includes mechanisms to handle data format issues, network interruptions, and API downtimes.

## Integration Details
- **API Source**: The tool integrates with the HKMA Open Data API, specifically targeting the coin cart schedule endpoint (e.g., `https://api.hkma.gov.hk/public/coin-cart-schedule`).
- **Data Format**: The API returns data in JSON format, which includes fields such as date, location, time, and status of coin cart services.
- **Dependencies**: Utilizes Python's `json` module for parsing and `requests` library for HTTP requests to fetch data.

## Usage
To use this tool via the MCP Server, invoke the `get_coin_cart_data` function without parameters as it fetches the latest available data:
```json
{}
```
- The response includes a JSON array of coin cart schedules with details on dates, locations, and operational times.

## Limitations
- **Data Availability**: Dependent on the HKMA's data update frequency and availability.
- **Rate Limits**: Subject to any rate limiting imposed by the HKMA API, though not explicitly documented.
- **Geographical Scope**: Limited to coin cart services within Hong Kong as provided by the HKMA.

## Error Handling and Edge Cases
- **Invalid JSON Data**: The tool checks for malformed JSON responses and raises an exception with a descriptive message.
- **Network Failures**: Implements error reporting for connection issues to ensure users are informed of data retrieval problems.
- **Empty Data**: Handles scenarios where no data is returned, providing appropriate feedback to the user.

## Future Enhancements
- Implement filtering options to allow users to retrieve schedules for specific locations or date ranges.
- Add notification features to alert users of schedule changes or new coin cart deployments.
- Enhance data visualization options for easier interpretation of schedules and locations.

## Related Documentation
- See `systemPatterns.md` for architectural patterns related to API integration in the HK Finance MCP Server.
- Refer to `techContext.md` for details on the Python libraries and MCP framework used for this tool.
