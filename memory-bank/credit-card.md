# Credit Card Data Tool Documentation

## Overview
The Credit Card Data Tool is a component of the HK Finance MCP Server designed to fetch and process credit card statistics in Hong Kong. This tool provides valuable insights into credit card usage and trends, which are essential for financial analysis and market research in Hong Kong.

## Purpose
This tool addresses the need for comprehensive data on credit card activities in Hong Kong. It enables users to:
- Retrieve quarterly statistics on credit card transactions and outstanding balances.
- Filter data by specific year and quarter ranges.
- Analyze trends in credit card usage, spending patterns, and debt levels.

## Key Features
- **Data Retrieval**: Automatically fetches JSON data from the Hong Kong Monetary Authority (HKMA) open data portal.
- **Data Parsing**: Converts JSON data into a structured format for easy access and analysis.
- **Filtering**: Allows users to specify a range of dates (year/quarter) to narrow down the data returned.
- **Error Handling**: Includes robust mechanisms to handle invalid data formats, network issues, and API downtimes.

## Integration Details
- **API Source**: The tool integrates with the HKMA Open Data API, specifically targeting the credit card statistics endpoint (e.g., `https://api.hkma.gov.hk/public/banking/credit-card-lending`).
- **Data Format**: The API returns data in JSON format, which includes fields such as date, number of credit cards, transaction volumes, and outstanding amounts.
- **Dependencies**: Utilizes Python's `json` module for parsing and `requests` library for HTTP requests to fetch data.

## Usage
To use this tool via the MCP Server, invoke the `get_credit_card_data` function with optional parameters for start and end year/quarter:
```json
{
  "start_year": 2018,
  "start_quarter": 1,
  "end_year": 2023,
  "end_quarter": 4
}
```
- If no parameters are provided, it defaults to fetching data for the last 8 quarters.
- The response includes a JSON array of quarterly credit card statistics within the specified range.

## Limitations
- **Data Availability**: Dependent on the HKMA's data update frequency and availability.
- **Rate Limits**: Subject to any rate limiting imposed by the HKMA API, though not explicitly documented.
- **Historical Data**: Limited to the range of data provided by the HKMA, which may not cover very old records.

## Error Handling and Edge Cases
- **Invalid JSON Data**: The tool checks for malformed JSON responses and raises an exception with a descriptive message.
- **Network Failures**: Implements error reporting for connection issues to ensure users are informed of data retrieval problems.
- **Boundary Conditions**: Handles edge cases for date filters, such as invalid year/quarter inputs or ranges that exceed available data.

## Future Enhancements
- Implement caching to reduce load on the HKMA API for frequently requested data ranges.
- Add support for more granular data filtering, such as by card type or issuer if the API expands to include such details.
- Enhance error messages with more specific diagnostic information for troubleshooting.

## Related Documentation
- See `systemPatterns.md` for architectural patterns related to API integration in the HK Finance MCP Server.
- Refer to `techContext.md` for details on the Python libraries and MCP framework used for this tool.
