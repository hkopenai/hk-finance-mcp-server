# Licensed Banks Historical Data Tool Documentation

## Overview
The Licensed Banks Historical Data Tool is a component of the HK Finance MCP Server designed to fetch and process historical data about licensed banks, bank branches, and bank offices in Hong Kong from 1954-2002. This tool provides access to comprehensive historical banking data from the Hong Kong Academy of Finance (AOF) API.

## Purpose
This tool addresses the need for historical banking data analysis in Hong Kong. It enables users to:
- Retrieve historical data on licensed banks, branches, and offices from 1954-2002
- Filter data by specific time periods and data types
- Analyze long-term trends in Hong Kong's banking sector development
- Support research and analysis of Hong Kong's financial history

## Key Features
- **Historical Data Retrieval**: Fetches data from the Hong Kong Academy of Finance (AOF) API covering 48 years of banking history
- **Flexible Filtering**: Allows filtering by year range and data type (licensed banks, branches, offices, or all)
- **Multi-language Support**: Supports English, Traditional Chinese, and Simplified Chinese output
- **Comprehensive Coverage**: Includes data on licensed banks, bank branches, bank offices, and total branches and offices
- **Error Handling**: Includes robust error handling for API failures and data validation

## Data Source
- **API Source**: Hong Kong Academy of Finance (AOF) API
- **Dataset**: Numbers of Licensed Banks, Bank Branches, and Bank Offices in Hong Kong (1954-2002)
- **Data Dictionary**: Available at https://www.aof.org.hk/docs/default-source/hkimr/hong-kong-economic-history-database/hkimr-lic-bank-branches-and-offices_swagger.json
- **Reference**: https://www.aof.org.hk/research/HKIMR/publications-and-research/hong-kong-economic-history-database

## Data Fields
The tool provides access to the following data fields:
- **year**: The year of the data record (1954-2002)
- **licensed_banks**: Number of licensed banks in Hong Kong
- **bank_branches**: Number of bank branches
- **bank_offices**: Number of bank offices
- **total_branches_and_offices**: Total number of branches and offices
- **notes**: Additional notes or comments about the data

## Usage
To use this tool via the MCP Server, invoke the `get_licensed_banks_historical_data` function with optional parameters:

```json
{
  "start_year": 1980,
  "end_year": 2000,
  "data_type": "licensed_banks",
  "lang": "en"
}
```

## Parameters
- **start_year** (optional): Start year for filtering data (1954-2002)
- **end_year** (optional): End year for filtering data (1954-2002)
- **data_type** (optional): Type of data to retrieve:
  - "licensed_banks": Only licensed banks count
  - "bank_branches": Only bank branches count
  - "bank_offices": Only bank offices count
  - "all": All data types (default)
- **lang** (optional): Language for output (en, tc, sc) - default: "en"

## Integration Details
- **API Endpoint**: https://www.aof.org.hk/api/v1/hkimr/lic-bank-branches-and-offices
- **Data Format**: JSON response with historical banking statistics
- **Dependencies**: Utilizes hkopenai_common.json_utils for data fetching
- **Timeout**: 30 seconds for API requests

## Use Cases
- **Historical Analysis**: Study the evolution of Hong Kong's banking sector over time
- **Research**: Academic and policy research on Hong Kong's financial development
- **Trend Analysis**: Identify patterns in banking sector growth and consolidation
- **Comparative Studies**: Compare banking sector development across different time periods 