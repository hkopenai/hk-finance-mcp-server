# Negative Equity Mortgage Data Tool Documentation

## Overview
The Negative Equity Mortgage Data Tool is a component of the HK Finance MCP Server designed to fetch and process data related to residential mortgage loans in negative equity in Hong Kong. This tool provides critical insights into housing market risks and financial stability, which are essential for economic analysis and policy-making in Hong Kong.

## Purpose
This tool addresses the need for detailed information on negative equity mortgages in Hong Kong. It enables users to:
- Retrieve quarterly statistics on residential mortgage loans in negative equity.
- Filter data by specific year and quarter ranges.
- Analyze trends in negative equity situations to assess housing market health and financial risk.

## Key Features
- **Data Retrieval**: Automatically fetches JSON data from the Hong Kong Monetary Authority (HKMA) open data portal.
- **Data Parsing**: Converts JSON data into a structured format for easy access and analysis.
- **Filtering**: Allows users to specify a range of dates (year/quarter) to narrow down the data returned.
- **Error Handling**: Includes robust mechanisms to handle invalid data formats, network issues, and API downtimes.

## Integration Details
- **API Source**: The tool integrates with the HKMA Open Data API, specifically targeting the negative equity mortgage statistics endpoint (e.g., `https://api.hkma.gov.hk/public/banking/residential-mortgage-loans-negative-equity`).
- **Data Format**: The API returns data in JSON format, which includes fields such as date, number of loans in negative equity, and total value of such loans.
- **Dependencies**: Utilizes Python's `json` module for parsing and `requests` library for HTTP requests to fetch data.

## Usage
To use this tool via the MCP Server, invoke the `get_negative_equity_mortgage_data` function with optional parameters for start and end year/quarter:
```json
{
  "start_year": 2015,
  "start_quarter": 1,
  "end_year": 2023,
  "end_quarter": 4
}
```
- If no parameters are provided, it defaults to fetching data for the last 8 quarters.
- The response includes a JSON array of quarterly negative equity mortgage statistics within the specified range.

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
- Add support for more granular data analysis, such as by property type or region if the API expands to include such details.
- Enhance error messages with more specific diagnostic information for troubleshooting.

## Related Documentation
- See `systemPatterns.md` for architectural patterns related to API integration in the HK Finance MCP Server.
- Refer to `techContext.md` for details on the Python libraries and MCP framework used for this tool.
