<p align="center">
  <img src="brand/logo.png" width="128" height="128">
</p>

# Zaturn: Your Co-Pilot For Data Analytics & BI

https://github.com/user-attachments/assets/d42dc433-e5ec-4b3e-bef0-5cfc097396ab

Zaturn is an open source, AI-powered data analysis/BI tool that can connect to your data sources, run SQL queries on it, and give you useful insights. Think of it like vibe data analysis, in the spirit of vibe coding. Currently Zaturn is available as an MCP (Model Context Protocol) Server that can be integrated into your favorite MCP Client (Claude, Cursor, etc.) A full fledged notebook interface is on the roadmap.

## Features:

### Multiple Data Sources 
Zaturn can currently connect to the following data sources: 
- SQL Databases: PostgreSQL, SQLite, DuckDB, MySQL
- Files: CSV, Parquet

Connectors for more data sources are being added.

### Visualizations
In addition to providing tabular and textual summaries, Zaturn can also generate the following image visualizations

- Scatter and Line Plots
- Histograms
- Strip and Box Plots
- Bar Plots

> NOTE: The visuals will be shown only if your MCP client supports image rendering (e.g. Claude Desktop)
> 
> If you MCP client does not support images (e.g. Cursor) add the `--noimg` argument in the MCP config. Then the plots will be stored as files and the file location will be returned. You can view the plots with your file browser.

More visualization capabilities are being added.


## How Does Zaturn Work?

The naivest way to have an LLM analyze your data is to upload a dataset with a prompt. But that won't get you far, because AI has context window limitations, and it can only go through a few thousand rows at the best. Also, LLM's are not great at doing math.

Using an MCP like Zaturn will keep your data where it is, and enable AI to draft and run SQL queries on the data. The LLM now processes only the queries and results instead of your entire dataset.

## Installation & Setup
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

2. Install Zaturn with uv:
```bash
$ uv tool install zaturn
```

3. Add to MCP config, with data sources:
```json
"mcpServers": {
  "zaturn": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/downloaded/folder",
      "mcp_server.py",
      "mysql+pymysql://username:password@host:3306/dbname",
      "postgresql://username:password@host:port/dbname",
      "sqlite:////full/path/to/sample_dbs/northwind.db",
      "/full/path/to/sample_dbs/titanic.parquet",
      "/full/path/to/sample_dbs/ny_aq.csv",
      "/full/path/to/sample_dbs/duckdb_sample.duckdb"
    ]
  },
}
```

If your MCP client does not support images, add the `--noimg` flag after `mcp_server.py`:
```json
...
      "mcp_server.py",
      "--noimg",
      "mysql+pymysql://username:password@host:3306/dbname",
...
```


4. Set a system prompt if your LLM/IDE allows you to:
```
You are a helpful data analysis assistant. Use only the tool provided data sources to process user inputs. Do not use external sources or your own knowledge base.
```

5. Ask a question and watch the magic:
```
User: List the top 5 customers by revenue for Northwind
AI: 
[04/08/25 15:16:47] INFO     Processing request of type ListToolsRequest                                     server.py:534
[04/08/25 15:16:51] INFO     Processing request of type CallToolRequest                                      server.py:534
[04/08/25 15:16:53] INFO     Processing request of type CallToolRequest                                      server.py:534
[04/08/25 15:16:55] INFO     Processing request of type CallToolRequest                                      server.py:534
The top 5 customers by revenue for Northwind are:

1. B's Beverages with a revenue of $6,154,115.34
2. Hungry Coyote Import Store** with a revenue of $5,698,023.67
3. Rancho grande with a revenue of $5,559,110.08
4. Gourmet Lanchonetes with a revenue of $5,552,597.90
5. Ana Trujillo Emparedados y helados with a revenue of $5,534,356.6
```

## Roadmap

- Support for more data source types
- More data visualizations
- Predictive analysis and forecasting, e.g.:
```
Based on the revenue of the last 3 months, forecast next month's revenue.
```
- Generate Presentations & PDFs
```
Manager: 
  I need a presentation to show the boss. Can you do it by EOD?
Analyst: 
  EOD?! Are you still in the 2010s? 
  I can get it done right now. Actually, you can do it right now.
  You know what? The boss can do it right now.
```
- A native notebook interface 

If you have any specific requirements please feel free to raise an issue.


## Example Dataset Credits

THe [pokemon dataset compiled by Sarah Taha and PokéAPI](https://www.kaggle.com/datasets/sarahtaha/1025-pokemon) has been included under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
