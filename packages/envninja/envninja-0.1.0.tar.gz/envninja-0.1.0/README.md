# EnvNinja - Environment Variable Management for Python

EnvNinja is a lightweight Python library for managing environment variables in a secure, structured, and automated manner. It provides an easy way to load, validate, and type-check environment variables, along with autogenerating `.env.example` files for easier collaboration in development teams. With support for automatic type casting and secret management, it’s a great tool for production-ready environments.

## Features

- **Type Safety**: Automatically cast environment variables to their correct types (int, bool, str, etc.).
- **Validation**: Ensure required environment variables are set and have the correct types.
- **Secret Detection**: Automatically flag sensitive information (like passwords, API tokens, etc.) and append emoji indicators for clarity.
- **`.env.example` Generation**: Auto-generate `.env.example` files with useful comments and emoji indicators for sensitive fields.
- **Docker Integration**: Generate `.env.example` for your Docker setups automatically.
- **Autocompletion**: For easy access to environment variables as properties (`config.PORT`).

## Installation

You can install EnvNinja via pip:

```bash
pip install envninja
