# Business Registration Data Tool Documentation

## Overview
The Business Registration Data Tool is a component of the HK Finance MCP Server designed to fetch and process business registration statistics from the Hong Kong Inland Revenue Department (IRD). This tool provides insights into business registration trends, which are critical for financial analysis and policy-making in Hong Kong.

## Purpose
This tool addresses the need for accurate, up-to-date business registration data in Hong Kong. It enables users to:
- Retrieve monthly statistics on business registrations.
- Filter data by specific year and month ranges.
- Analyze trends in business incorporations and closures.

## Key Features
- **Data Retrieval**: Automatically fetches CSV data from the IRD's official open data portal.
- **Data Parsing**: Converts raw CSV data into a structured JSON format for easier consumption.
- **Filtering**: Allows users to specify a range of dates (year/month) to narrow down the data returned.
- **Error Handling**: Includes robust mechanisms to handle invalid data formats, network issues, and API downtimes.

## Integration Details
- **API Source**: The tool integrates with the IRD Open Data API, specifically targeting the business registration statistics endpoint (e.g., `https://www.ird.gov.hk/dat/esbr/csv/e_sbr_all.csv`).
- **Data Format**: The API returns data in CSV format, which the tool parses into a list of records with fields such as date, number of registrations, and type of business.
- **Dependencies**: Utilizes Python's `csv` module for parsing and `requests` library for HTTP requests to fetch data.

## Usage
To use this tool via the MCP Server, invoke the `get_business_reg_data` function with optional parameters for start and end year/month:
```json
{
  "start_year": 2020,
  "start_month": 1,
  "end_year": 2023,
  "end_month": 12
}
```
- If no parameters are provided, it defaults to fetching data for the last 12 months.
- The response includes a JSON array of monthly business registration statistics within the specified range.

## Limitations
- **Data Availability**: Dependent on the IRD's data update frequency and availability.
- **Rate Limits**: Subject to any rate limiting imposed by the IRD API, though not explicitly documented.
- **Historical Data**: Limited to the range of data provided by the IRD, which may not cover very old records.

## Error Handling and Edge Cases
- **Invalid CSV Data**: The tool checks for malformed CSV responses and raises an exception with a descriptive message.
- **Network Failures**: Implements retry logic or error reporting for connection issues.
- **Boundary Conditions**: Handles edge cases for date filters, such as invalid year/month inputs or ranges that exceed available data.

## Future Enhancements
- Implement caching to reduce load on the IRD API for frequently requested data ranges.
- Add support for more granular data filtering, such as by business type or sector if the API expands to include such details.
- Enhance error messages with more specific diagnostic information for troubleshooting.

## Related Documentation
- See `systemPatterns.md` for architectural patterns related to API integration in the HK Finance MCP Server.
- Refer to `techContext.md` for details on the Python libraries and MCP framework used for this tool.
