# Hong Kong Finance Data MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-finance-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to finance related data in Hong Kong through a FastMCP interface.

## Features

1. Monthly statistics on the number of new and active business registrations in Hong Kong
2. Quarterly statistics on residential mortgage loans in negative equity in Hong Kong
3. Credit card lending survey results in Hong Kong
4. Coin cart schedule in Hong Kong
5. Get list of hotlines for reporting loss of credit card from Hong Kong banks
6. Get information of Tender Invitation and Notice of Award of Contracts from Hong Kong Monetary Authority
7. Daily figures of Hong Kong Interbank Interest Rates (HIBOR)
8. Information on Automated Teller Machines (ATMs) of retail banks in Hong Kong
9. Monthly statistics on stamp duty collected from transfer of Hong Kong stock (both listed and unlisted)
10. Information on bank branch locations of retail banks in Hong Kong
11. Information on fraudulent bank websites and phishing scams reported to HKMA

## Examples

* What is the number of new business registered in Hong Kong 2024?
* What is the negative loan situation in Hong Kong Q1 2025 compare with Q1 2024?
* Write a commentary about the latest residential mortgage loans in negative equity in Hong Kong
* How is current Hong Kong economy by referencing credit lending data and residential mortgage loans in negative equity?
* What are the recent trends in HIBOR rates over the past month?
* Where can I find ATMs in Yuen Long district that support HKD and RMB currencies?
* Can you list the recent fraudulent bank websites reported to HKMA?

Assume chart tool is available:

* Plot a line chart showing trend and number of new business registered each month from Jan to Dec in Hong Kong 2024.
![](https://raw.githubusercontent.com/hkopenai/hk-finance-mcp-server/refs/heads/main/assets/line_chart.png)

## Data Source

* Hong Kong Monetary Authority
  - Bank Branch Locator: [HKMA DataGovHK Page](https://data.gov.hk/en-data/dataset/hk-hkma-bankatm-banks-branch-locator)
  - Fraudulent Bank Websites and Phishing Scams: [HKMA DataGovHK Page](https://data.gov.hk/en-data/dataset/hk-hkma-banksvf-fraudulent-bank-scams)
  - Credit Card Lending Survey Results: [HKMA DataGovHK Page](https://data.gov.hk/en-data/dataset/hk-hkma-t03-t0308credit-card-lending-survey)
* Hong Kong Inland Revenue Department
  - Stamp Duty Statistics: [IRD DataGovHK Page](https://www.ird.gov.hk/eng/dat/dat_gov.htm)

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### Running Options

- Default stdio mode: `python server.py`
- SSE mode (port 8000): `python server.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-finance": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hkopenai.hk-finance-mcp-server"
    ]
  }
}
```

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```
