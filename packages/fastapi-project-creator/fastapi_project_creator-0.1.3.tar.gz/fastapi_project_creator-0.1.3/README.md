# FastAPI Generator

A simple CLI tool to generate FastAPI project structure with best practices, ready-to-use configuration, and organized folder structure.

## Installation

```bash
# Install from PyPI
pip install fastapi-project-creator

# Or install directly from GitHub
pip install git+https://github.com/raihanhd12/fastapi-project-creator.git
```

## Usage

```bash
# Create a new FastAPI project
create-fastapi-app my-project-name
```

This will generate a complete FastAPI project structure with the following features:

- Organized directory structure following best practices
- Pre-configured API router setup with controllers and services
- Database connection with SQLAlchemy
- Environment variable configuration with host and port settings
- Ready-to-use project structure with proper entry point

## Project Structure

```
my-project-name/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── api.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── base_controller.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── base_service.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Development

To contribute to this project:

1. Clone the repository

```bash
git clone https://github.com/raihanhd12/fastapi-project-creator.git
cd fastapi-project-creator
```

2. Install in development mode

```bash
pip install -e .
```

3. Make your changes and test them with

```bash
create-fastapi-app test-project
```

## License

MIT