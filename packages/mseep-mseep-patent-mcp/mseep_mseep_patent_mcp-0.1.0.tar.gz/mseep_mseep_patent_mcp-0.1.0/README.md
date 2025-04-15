# RapidAPI MCP Server

This repository contains an implementation of an MCP Server for interfacing with the RapidAPI Global Patent API and storing patent data in a SQLite database.

## Features

- RapidAPI Global Patent API integration
- MCP Server implementation for handling patent requests
- SQLite database integration for patent data storage
- Advanced patent scoring system (pscore, cscore, lscore, tscore)
- Rate limiting and error handling

## Installation

### Using Conda (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/myownipgit/RapidAPI-MCP.git
cd RapidAPI-MCP
```

2. Create and activate conda environment:
```bash
# Create environment from yml file
conda env create -f environment.yml

# Activate environment
conda activate rapidapi-mcp
```

Alternatively, you can create the environment manually:
```bash
# Create new environment with Python 3.11
conda create -n rapidapi-mcp python=3.11

# Activate environment
conda activate rapidapi-mcp

# Install required packages
conda install -c conda-forge requests aiohttp python-dotenv pytest
pip install rapidapi-connect
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

1. Initialize the MCP Server:
```python
from patent_mcp.server import MCPPatentServer

mcp_server = MCPPatentServer()
```

2. Handle patent search requests:
```python
search_request = {
    'command': 'search',
    'params': {
        'query': 'quantum computing',
        'date_range': '2004-2024',
        'page': 1,
        'per_page': 100
    }
}

results = await mcp_server.handle_patent_request(search_request)
```

## Testing

To run the tests, activate your conda environment and run:
```bash
# Run the connection test
python tests/test_connection.py

# Run all tests with pytest
python -m pytest tests/
```

## Project Structure

- `patent_mcp/` - Main package directory
  - `client.py` - RapidAPI client implementation
  - `server.py` - MCP Server implementation
  - `database.py` - SQLite database operations
  - `scoring.py` - Patent scoring system
  - `__init__.py` - Package initialization
- `docs/` - Documentation
  - `SCORING.md` - Detailed scoring methodology
- `examples/` - Example scripts
- `tests/` - Unit tests

## Requirements

- Python 3.11 or higher
- Required packages are listed in `environment.yml`

## Scoring System

The system implements a comprehensive patent scoring methodology:

- Patent Score (pscore): Overall patent strength
- Citation Score (cscore): Citation impact analysis
- Legal Score (lscore): Legal status evaluation
- Technology Score (tscore): Technical complexity assessment

See [SCORING.md](docs/SCORING.md) for detailed information.

## Configuration

The server uses the following environment variables:
- `RAPIDAPI_KEY`: Your RapidAPI API key
- `DB_PATH`: Path to SQLite database (optional, defaults to `./patents.db`)
- Additional configuration options in `.env`

## Rate Limits

The RapidAPI service has the following limits:
- 1000 requests per day
- 500000 hard limit

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details