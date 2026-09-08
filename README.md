# Hunter.io API Client

Python-клиент для Hunter.io API v2 с resource-based архитектурой, типизацией, сервисным слоем и JSON-backed storage.

Проект выполнен с учётом требований к качеству кода: `mypy`, `flake8`, `isort` и конфигурации в `setup.cfg`.

## Architecture

Проект разделён на несколько уровней ответственности:

```text
HunterClient
    │
    ├── EmailEndpoint
    │     └── verify()
    │
    ├── DomainEndpoint
    │     └── search()
    │
    └── shared HTTP layer
          ├── authentication
          ├── requests.Session
          ├── timeouts
          └── HTTP error handling

HunterService
    │
    ├── HunterClient
    └── DataStorage

DataStorage
    │
    └── results.json
```

### Почему resource-based architecture

API endpoints группируются по ресурсам, а не помещаются в один большой `HunterClient`.

Например:

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
└── campaigns
    ├── list()
    └── get()
```

При добавлении новых endpoints существующие классы не превращаются в большой монолитный клиент.

Каждый ресурс может иметь собственный endpoint-класс, используя общий HTTP transport.

## Project Structure

```text
hunter-test-task/
├── hunter_client/
│   ├── __init__.py
│   ├── client.py
│   ├── http/
│   │   └── transport.py
│   ├── resources/
│   │   ├── email.py
│   │   └── domain.py
│   ├── dto/
│   │   └── ...
│   ├── service.py
│   └── storage.py
├── tests/
│   └── ...
├── main.py
├── setup.cfg
├── requirements.txt
├── .gitignore
└── README.md
```

## Implemented endpoints

### Email Verifier

```python
client.email.verify("user@example.com")
```

Verifies an email address using Hunter's Email Verifier API.

### Domain Search

```python
client.domain.search("stripe.com", limit=10)
```

Searches for email addresses associated with a domain.

## Service Layer

`HunterService` coordinates API calls and persistence.

Example:

```python
service.verify_and_save_email("user@example.com")
service.search_and_save_domain("stripe.com", limit=10)
```

The service layer:

1. Calls the required API resource through `HunterClient`.
2. Receives the API response.
3. Converts the response into the required application representation.
4. Persists the result using `DataStorage`.

API communication and persistence are therefore kept separate from application-level operations.

## Storage

`DataStorage` provides simple CRUD operations backed by a local JSON file.

Supported operations:

```text
create()
read()
update()
delete()
```

Default storage file:

```text
results.json
```

The storage implementation can be replaced independently from the API client.

## Requirements

* Python 3.8+
* Hunter.io API key

## Installation

Clone the repository:

```bash
git clone https://github.com/DDarkVoid/hunter-test-task.git
cd hunter-test-task
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
HUNTER_API_KEY=your_api_key
```

Never commit `.env` or your API key to the repository.

## Running

Run the example application:

```bash
python main.py
```

The example demonstrates:

* email verification;
* domain search;
* persistence of API results.

## Code Quality

The project uses `setup.cfg` as the central configuration for static analysis and formatting tools.

### mypy

Run:

```bash
mypy .
```

The configuration enables strict checks such as:

* `disallow_untyped_defs`;
* `strict_optional`;
* `strict_equality`;
* `warn_unreachable`;
* `warn_unused_ignores`.

Expected result:

```text
Success: no issues found
```

### flake8

Run:

```bash
flake8 .
```

Expected result:

```text
0
```

### isort

Check import ordering:

```bash
isort --check-only .
```

To automatically fix imports:

```bash
isort .
```

## Development checks

Before submitting changes, run:

```bash
isort --check-only .
flake8 .
mypy .
```

All checks should pass without errors.

## Design Principles

The project follows several simple principles:

### Single Responsibility

Each layer has a specific responsibility:

```text
HTTP transport
      ↓
API resources
      ↓
Service layer
      ↓
Storage
```

### Dependency separation

The service layer does not implement HTTP communication directly, and the API client does not manage application persistence.

### Extensibility

New API resources can be added without expanding `HunterClient` into a large class.

For example:

```text
resources/
├── email.py
├── domain.py
├── leads.py
├── campaigns.py
└── account.py
```

This approach is intended to remain maintainable as the number of API endpoints grows.

## Testing

Tests should cover the main application boundaries:

* HTTP transport;
* API resources;
* service layer;
* storage CRUD operations.

Run tests with:

```bash
pytest
```

## Security

API credentials must be supplied through environment variables.

Do not commit:

```text
.env
*.key
*.secret
```

or any other credentials to the repository.

## License

This project was created as a test assignment.
