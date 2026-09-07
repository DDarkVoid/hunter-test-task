# Hunter.io API Client & Service Layer

A small Python project that integrates with the Hunter.io API v2, provides a JSON-backed CRUD storage, and connects both through a service layer.

## Architecture

The API client uses a resource-based architecture so it can be extended without turning `HunterClient` into a large monolithic class.

```text
HunterClient
├── email
│   └── EmailEndpoint
│       └── verify()
├── domain
│   └── DomainEndpoint
│       └── search()
└── shared HTTP layer
    ├── API authentication
    ├── requests.Session
    ├── timeouts
    └── HTTP error handling

HunterService
├── calls HunterClient
└── saves API results to DataStorage

DataStorage
└── in-memory storage synchronized with results.json
```

### Scaling to 100+ endpoints

Endpoints are grouped by API resource instead of being added directly to one large client class.

For example:

```text
HunterClient
├── email
│   ├── verify()
│   └── find()
├── domain
│   ├── search()
│   └── count()
├── leads
│   ├── list()
│   ├── create()
│   └── delete()
├── campaigns
│   ├── list()
│   └── get()
└── account
    └── info()
```

Each resource can be implemented as a separate endpoint class while reusing the same HTTP functionality from `HunterClient`.

This keeps responsibilities separated and allows the client to grow without accumulating hundreds of unrelated methods in a single class.

## Project Structure

```text
hunter_project/
├── hunter_client.py   # Hunter.io API client and resource endpoints
├── storage.py         # JSON-backed CRUD storage
├── service.py         # Service layer
├── main.py            # Application entry point and usage example
├── setup.cfg          # mypy, flake8 and isort configuration
├── requirements.txt   # Project dependencies
├── .gitignore
└── README.md
```

## Implemented API Endpoints

### Email Verifier

```python
client.email.verify("user@example.com")
```

Uses Hunter's Email Verifier endpoint.

### Domain Search

```python
client.domain.search("stripe.com", limit=10)
```

Uses Hunter's Domain Search endpoint.

## Data Storage

`DataStorage` provides CRUD operations and synchronizes its in-memory data with a local JSON file.

Available methods:

```text
create()
read()
update()
delete()
```

The default application storage file is:

```text
results.json
```

## Service Layer

`HunterService` coordinates API requests and persistence.

Available operations:

```python
service.verify_and_save_email("user@example.com")
service.search_and_save_domain("stripe.com", limit=10)
```

The service layer:

1. Calls the appropriate Hunter API endpoint through `HunterClient`.
2. Receives the API response.
3. Creates or updates the corresponding record in `DataStorage`.

## Requirements

- Python 3.8+
- Hunter.io API key

## Installation

Clone the repository:

```bash
git clone https://github.com/DDarkVoid/hunter-test-task.git
cd hunter-test-task
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
HUNTER_API_KEY=your_actual_api_key
```

Do not commit `.env` or your API key to the repository.

## Running

Run the example application:

```bash
python main.py
```

The example performs:

- email verification;
- domain search;
- saving the returned results to `results.json`.

## Code Quality

The project is configured for static type checking and linting.

Run mypy:

```bash
mypy .
```

Run flake8:

```bash
flake8 .
```

Run isort check:

```bash
isort --check-only .
```

The project is configured according to the provided `setup.cfg`, with Django-specific configuration removed because this project does not use Django.

## Design Principles

The project follows a simple separation of responsibilities:

```text
API communication
       ↓
HunterClient / Endpoint resources
       ↓
HunterService
       ↓
DataStorage
       ↓
results.json
```

This makes the main components independent and easier to extend or test.
