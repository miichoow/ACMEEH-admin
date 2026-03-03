# acmeeh-admin

[![Tests](https://github.com/miichoow/ACMEEH-admin/actions/workflows/test.yml/badge.svg)](https://github.com/miichoow/ACMEEH-admin/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/acmeeh-admin)](https://pypi.org/project/acmeeh-admin/)
[![Python versions](https://img.shields.io/pypi/pyversions/acmeeh-admin)](https://pypi.org/project/acmeeh-admin/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/miichoow/ACMEEH-admin/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/miichoow/ACMEEH-admin/branch/main/graph/badge.svg)](https://codecov.io/gh/miichoow/ACMEEH-admin)
[![Code Style](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Python client library and CLI for the **[ACMEEH](https://github.com/miichoow/ACMEEH) Admin API**.

[ACMEEH](https://github.com/miichoow/ACMEEH) is a production-ready ACME server (RFC 8555) for internal PKI management, supporting pluggable CA backends, HTTP-01/DNS-01/TLS-ALPN-01 challenges, EAB, CSR profiles, CRL generation, and certificate lifecycle hooks. This package provides both a **Python client** and a **CLI** for its token-authenticated Admin REST API.

- **Library**: Programmatic access via `AcmeehAdminClient`
- **CLI**: `acmeeh-admin` command-line tool for operators and scripts

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Python Library](#python-library)
  - [Public API](#public-api)
  - [Quick Start](#quick-start)
  - [Constructor](#constructor)
  - [Authentication](#authentication)
  - [Resource Reference](#resource-reference)
  - [Error Handling](#error-handling)
  - [Pagination](#pagination)
  - [Thread Safety](#thread-safety)
  - [Synchronous Only](#synchronous-only)
  - [Connection Pooling and Proxies](#connection-pooling-and-proxies)
  - [Retries](#retries)
- [CLI](#cli)
  - [Global Options](#global-options)
  - [Configuration](#configuration)
  - [Authentication (CLI)](#authentication-1)
  - [Command Reference](#command-reference)
  - [Output Formats](#output-formats)
  - [CLI Output Messages](#cli-output-messages)
  - [Exit Codes](#exit-codes)
  - [CLI Examples](#cli-examples)
- [REST API Endpoints](#rest-api-endpoints)
- [Architecture](#architecture)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.10+
- A running [ACMEEH](https://github.com/miichoow/ACMEEH) server with the admin module enabled

## Installation

```bash
pip install acmeeh-admin
```

Or install from source:

```bash
git clone <repo-url>
cd acmeeh-admin
pip install .
```

For development (includes pytest and responses):

```bash
pip install -e ".[dev]"
```

## Dependencies

| Package    | Version      | Purpose       |
|------------|--------------|---------------|
| `requests` | >= 2.28, < 3 | HTTP client   |
| `click`    | >= 8.1, < 9  | CLI framework |

---

## Python Library

### Public API

The package exports the following symbols from `acmeeh_admin`:

```python
from acmeeh_admin import (
    AcmeehAdminClient,          # Main client class
    AcmeehAdminError,           # Base exception for HTTP 4xx/5xx
    AcmeehAuthenticationError,  # 401/403 errors
    AcmeehConnectionError,      # Unreachable server / timeout
    __version__,                # Package version string (e.g. "0.1.0")
)
```

### Quick Start

```python
from acmeeh_admin import AcmeehAdminClient

# Authenticate with an existing token
client = AcmeehAdminClient("https://acme.internal", token="your-bearer-token")

# Or authenticate interactively
client = AcmeehAdminClient("https://acme.internal")
client.login("admin", "password")

# Use the API
users = client.users.list()
cert = client.certificates.get_by_serial("01:AB:CD:EF")

# Clean up
client.logout()
```

### Constructor

```python
AcmeehAdminClient(
    base_url: str,
    *,
    token: str | None = None,      # Bearer token for authentication
    verify_ssl: bool = True,        # Set False for self-signed certs
    timeout: int = 30,              # Request timeout in seconds
    api_prefix: str = "/api",       # Admin API path prefix
)
```

### Authentication

| Method                             | Description                                                                                                   |
|------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `client.login(username, password)` | Authenticate and store the token for subsequent requests. Returns the login response dict (includes `token`). |
| `client.logout()`                  | Revoke the current token and clear it from the session. Returns the server response dict.                     |
| `client.token`                     | Property to get/set the bearer token directly.                                                                |

### Resource Reference

The client exposes the following resource objects, each mapping to a group of Admin API endpoints.

#### `client.users` — Admin User Management

| Method                                            | Description                                                            |
|---------------------------------------------------|------------------------------------------------------------------------|
| `list() -> list[dict]`                            | List all admin users.                                                  |
| `create(username, email, role="auditor") -> dict` | Create a new admin user. Response includes the generated password.     |
| `get(user_id) -> dict`                            | Get a specific admin user by ID.                                       |
| `update(user_id, **kwargs) -> dict`               | Update an admin user. Accepts `enabled` (bool) and `role` (str).       |
| `delete(user_id) -> None`                         | Delete an admin user.                                                  |
| `me() -> dict`                                    | Get the current (authenticated) user's profile.                        |
| `reset_password() -> dict`                        | Reset the current user's password. Response includes the new password. |

#### `client.audit` — Audit Log

| Method                                                                | Description                                                                    |
|-----------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `list(*, limit, cursor, action, user_id, since, until) -> list[dict]` | Fetch a single page of audit log entries. All parameters are optional filters. |
| `list_all(*, limit, **filters) -> list[dict]`                         | Fetch all pages and return a flat list. Accepts the same filters as `list()` except `cursor`. |
| `export(*, action, user_id, since, until) -> list[dict]`              | Export audit log as parsed NDJSON entries (streamed).                          |

#### `client.eab` — External Account Binding (EAB) Credentials

| Method                                                  | Description                                                         |
|---------------------------------------------------------|---------------------------------------------------------------------|
| `list() -> list[dict]`                                  | List all EAB credentials.                                           |
| `create(kid, label="") -> dict`                         | Create an EAB credential. Response includes the generated HMAC key. |
| `get(cred_id) -> dict`                                  | Get a specific EAB credential by ID.                                |
| `revoke(cred_id) -> dict`                               | Revoke an EAB credential.                                           |
| `add_identifier(eab_id, identifier_id) -> None`         | Link an allowed identifier to a credential.                         |
| `remove_identifier(eab_id, identifier_id) -> None`      | Unlink an allowed identifier from a credential.                     |
| `list_identifiers(eab_id) -> list[dict]`                | List allowed identifiers linked to a credential.                    |
| `assign_csr_profile(eab_id, profile_id) -> None`        | Assign a CSR profile to a credential.                               |
| `unassign_csr_profile(eab_id, profile_id) -> None`      | Remove the CSR profile assignment from a credential.                |
| `get_csr_profile(eab_id) -> dict \| None`               | Get the CSR profile assigned to a credential. Returns `None` if no profile is assigned. |

#### `client.identifiers` — Allowed Identifier Management

| Method                                              | Description                                                              |
|-----------------------------------------------------|--------------------------------------------------------------------------|
| `list() -> list[dict]`                              | List all allowed identifiers.                                            |
| `create(identifier_type, value) -> dict`            | Create a new allowed identifier. `identifier_type` is `"dns"` or `"ip"`. |
| `get(identifier_id) -> dict`                        | Get an allowed identifier with its associated accounts.                  |
| `delete(identifier_id) -> None`                     | Delete an allowed identifier.                                            |
| `add_account(identifier_id, account_id) -> None`    | Associate an identifier with an ACME account.                            |
| `remove_account(identifier_id, account_id) -> None` | Remove an identifier-account association.                                |
| `list_for_account(account_id) -> list[dict]`        | List allowed identifiers for a specific ACME account.                    |

#### `client.profiles` — CSR Profile Management

| Method                                                           | Description                                                          |
|------------------------------------------------------------------|----------------------------------------------------------------------|
| `list() -> list[dict]`                                           | List all CSR profiles.                                               |
| `create(name, profile_data, description="") -> dict`             | Create a new CSR profile. `profile_data` is a dict of profile rules. |
| `get(profile_id) -> dict`                                        | Get a specific CSR profile with associated accounts.                 |
| `update(profile_id, name, profile_data, description="") -> dict` | Update a CSR profile (full replacement).                             |
| `delete(profile_id) -> None`                                     | Delete a CSR profile.                                                |
| `validate(profile_id, csr_b64) -> dict`                          | Dry-run validate a base64-encoded CSR against a profile.             |
| `assign_account(profile_id, account_id) -> None`                 | Assign a CSR profile to an ACME account.                             |
| `unassign_account(profile_id, account_id) -> None`               | Remove a profile-account assignment.                                 |
| `get_for_account(account_id) -> dict \| None`                    | Get the CSR profile assigned to an ACME account. Returns `None` if no profile is assigned. |

#### `client.certificates` — Certificate Operations

| Method                                                    | Description                                                                                                                    |
|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `search(**filters) -> list[dict]`                         | Search certificates. Filters: `account_id`, `serial`, `fingerprint`, `status`, `domain`, `expiring_before`, `limit`, `offset`. |
| `get_by_serial(serial) -> dict`                           | Get a certificate by serial number.                                                                                            |
| `get_by_fingerprint(fingerprint) -> dict`                 | Get a certificate by SHA-256 fingerprint (hex).                                                                                |
| `bulk_revoke(filter, reason=None, dry_run=False) -> dict` | Revoke multiple certificates matching a filter. `filter` is a dict with keys such as `domain`, `account_id`, `serial_numbers`, etc. `reason` is an RFC 5280 revocation reason code (e.g., 4 = superseded). |

> **Note:** The `fingerprint` filter is available in the library via `client.certificates.search(fingerprint="...")` but is not exposed as a CLI option. For fingerprint lookups in the CLI, use `certificates get-by-fingerprint <SHA256_HEX>` instead.

#### `client.notifications` — Notification Management

| Method                                         | Description                                                |
|------------------------------------------------|------------------------------------------------------------|
| `list(*, status, limit, offset) -> list[dict]` | List notifications with optional filters. All parameters are optional. |
| `retry() -> dict`                              | Retry all failed notifications. Returns `{"retried": count}`.         |
| `purge(days=30) -> dict`                       | Purge sent notifications older than `days` days. Returns `{"purged": count}`. |

#### `client.crl` — CRL Management

| Method              | Description                                 |
|---------------------|---------------------------------------------|
| `rebuild() -> dict` | Force a CRL rebuild. Returns health status. |

#### `client.maintenance` — Maintenance Mode

| Method                        | Description                                            |
|-------------------------------|--------------------------------------------------------|
| `get_status() -> dict`        | Get current maintenance mode status.                   |
| `set_status(enabled) -> dict` | Enable (`True`) or disable (`False`) maintenance mode. |

### Error Handling

All API errors raise typed exceptions:

```python
from acmeeh_admin import (
    AcmeehAdminError,            # Base: any HTTP 4xx/5xx
    AcmeehAuthenticationError,   # 401 Unauthorized / 403 Forbidden
    AcmeehConnectionError,       # Server unreachable / timeout
)

try:
    client.users.get("nonexistent-id")
except AcmeehAuthenticationError as e:
    print(f"Auth failed: {e.detail}")  # Human-readable message
except AcmeehAdminError as e:
    print(f"[{e.status_code}] {e.detail}")
    print(f"RFC 7807 type: {e.error_type}")
    print(f"Raw response: {e.response}")
```

Error attributes:

| Attribute     | Type                        | Description                                |
|---------------|-----------------------------|--------------------------------------------|
| `status_code` | `int`                       | HTTP status code (0 for connection errors) |
| `detail`      | `str`                       | Human-readable error message               |
| `error_type`  | `str`                       | RFC 7807 problem `type` URI                |
| `response`    | `requests.Response \| None` | Raw response object                        |

### Pagination

List endpoints that support pagination return data via a `PaginatedIterator` internally. The resource methods handle this transparently — `list()` methods return the first page, while `list_all()` (where available) collects all pages into a flat list.

The pagination follows the `Link: <url>;rel="next"` header convention. `PaginatedIterator` implements the Python iterator protocol — each call to `__next__()` fetches the next page and returns its items as a list. The `collect()` method fetches all pages and returns a flat list.

> **Note:** `list_all()` is currently only available on the `client.audit` resource. Other resources provide single-page `list()` methods.

### Thread Safety

`AcmeehAdminClient` is **not thread-safe**. Each thread should create its own client instance. The underlying `requests.Session` is shared across all resource objects within a single client, and concurrent access may lead to race conditions.

```python
# Correct: separate client per thread
import threading

def worker(token):
    client = AcmeehAdminClient("https://acme.internal", token=token)
    users = client.users.list()

threads = [threading.Thread(target=worker, args=(token,)) for _ in range(4)]
```

### Synchronous Only

The library is **synchronous** — all methods block until the HTTP response is received. There is no built-in async support. If you need async operations, run client calls in a thread pool:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def list_users_async(client):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, client.users.list)
```

### Connection Pooling and Proxies

The client uses a persistent `requests.Session` internally, which provides automatic **connection pooling** (keep-alive) across requests to the same server.

**Proxy support** is available via standard environment variables:

```bash
export HTTP_PROXY=http://proxy.internal:8080
export HTTPS_PROXY=http://proxy.internal:8080
export NO_PROXY=localhost,127.0.0.1
```

### Retries

The library does **not** implement automatic retries or exponential backoff. If you need retry logic, wrap calls with a library like [`tenacity`](https://github.com/jd/tenacity):

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def get_users(client):
    return client.users.list()
```

---

## CLI

The `acmeeh-admin` CLI provides full access to the Admin API from the terminal.

### Global Options

```
Usage: acmeeh-admin [OPTIONS] COMMAND [ARGS]...

Options:
  --server TEXT              Server URL (env: ACMEEH_ADMIN_URL)
  --token TEXT               Bearer token (env: ACMEEH_ADMIN_TOKEN)
  --format [table|json]      Output format (default: table)
  --no-verify-ssl            Disable SSL certificate verification
  --api-prefix TEXT          Admin API path prefix (env: ACMEEH_ADMIN_API_PREFIX, default: /api)
  --version                  Show version and exit
  --help                     Show help and exit
```

### Configuration

The CLI stores configuration in `~/.acmeeh-admin.json`. Values are resolved in this priority order:

1. CLI flags (`--server`, `--token`, `--no-verify-ssl`, `--api-prefix`)
2. Environment variables (`ACMEEH_ADMIN_URL`, `ACMEEH_ADMIN_TOKEN`, `ACMEEH_ADMIN_VERIFY_SSL`, `ACMEEH_ADMIN_API_PREFIX`)
3. Config file (`~/.acmeeh-admin.json`)

Config file format (written automatically by `acmeeh-admin login`). Login saves `server_url`, `token`, `api_prefix`, and `verify_ssl`:

```json
{
  "server_url": "https://acme.internal",
  "token": "your-bearer-token",
  "api_prefix": "/api",
  "verify_ssl": true
}
```

Environment variables:

| Variable                    | Description                                           |
|-----------------------------|-------------------------------------------------------|
| `ACMEEH_ADMIN_URL`         | Server URL                                            |
| `ACMEEH_ADMIN_TOKEN`       | Bearer token                                          |
| `ACMEEH_ADMIN_VERIFY_SSL`  | SSL verification (`true`/`false`/`0`/`1`/`yes`/`no`) |
| `ACMEEH_ADMIN_API_PREFIX`  | Admin API path prefix (default: `/api`)               |

### Authentication

```bash
# Interactive login — prompts for username and password (and server URL if not already set)
acmeeh-admin login

# All subsequent commands use the saved token
acmeeh-admin users list

# Logout (revokes token on server and removes it from config; server URL is preserved)
acmeeh-admin logout

# Or pass credentials per-command
acmeeh-admin --server https://acme.internal --token <TOKEN> users list
```

### Command Reference

#### `users` — Admin User Management

```bash
acmeeh-admin users list                          # List all admin users
acmeeh-admin users create <USERNAME> <EMAIL>     # Create user (default role: auditor)
acmeeh-admin users create <USERNAME> <EMAIL> --role admin
acmeeh-admin users get <USER_ID>                 # Get user details
acmeeh-admin users update <USER_ID> --role admin # Update user role
acmeeh-admin users update <USER_ID> --enabled    # Enable user
acmeeh-admin users update <USER_ID> --disabled   # Disable user
acmeeh-admin users delete <USER_ID>              # Delete user (with confirmation)
acmeeh-admin users delete <USER_ID> --yes        # Delete without confirmation (scripting)
acmeeh-admin users me                            # Current user's profile
acmeeh-admin users reset-password                # Reset current user's password
```

#### `audit` — Audit Log

```bash
acmeeh-admin audit list                                     # List recent audit entries
acmeeh-admin audit list --action login --since 2024-01-01   # Filter by action and date
acmeeh-admin audit list --user-id <ID> --limit 50           # Filter by user with page size
acmeeh-admin audit list --until 2024-06-01 --cursor <TOKEN> # Paginate with cursor
acmeeh-admin audit export                                                      # Export full log as NDJSON
acmeeh-admin audit export --action cert.revoke                                 # Export filtered by action
acmeeh-admin audit export --user-id <ID>                                       # Export filtered by user
acmeeh-admin audit export --since 2024-01-01 --until 2024-02-01               # Export date range
acmeeh-admin audit export -o audit.json                                        # Write NDJSON to file
acmeeh-admin audit export --since 2024-01-01 --until 2024-02-01 -o audit.json  # Export date range to file
```

#### `eab` — EAB Credential Management

```bash
acmeeh-admin eab list                                        # List all EAB credentials
acmeeh-admin eab create <KID>                                # Create EAB credential
acmeeh-admin eab create <KID> --label "prod-01"              # Create with label
acmeeh-admin eab get <CRED_ID>                               # Get credential details
acmeeh-admin eab revoke <CRED_ID>                            # Revoke credential
acmeeh-admin eab add-identifier <EAB_ID> <IDENTIFIER_ID>     # Link an allowed identifier
acmeeh-admin eab remove-identifier <EAB_ID> <IDENTIFIER_ID>  # Unlink an allowed identifier
acmeeh-admin eab list-identifiers <EAB_ID>                   # List linked identifiers
acmeeh-admin eab assign-profile <EAB_ID> <PROFILE_ID>        # Assign a CSR profile
acmeeh-admin eab unassign-profile <EAB_ID>                   # Remove CSR profile assignment (auto-resolves profile ID)
acmeeh-admin eab get-profile <EAB_ID>                        # Get assigned CSR profile
```

#### `identifiers` — Allowed Identifier Management

```bash
acmeeh-admin identifiers list                              # List all allowed identifiers
acmeeh-admin identifiers create dns "*.example.com"        # Allow a DNS identifier
acmeeh-admin identifiers create ip 10.0.0.1                # Allow an IP identifier
acmeeh-admin identifiers get <ID>                          # Get identifier details
acmeeh-admin identifiers delete <ID>                       # Delete (with confirmation)
acmeeh-admin identifiers delete <ID> --yes                 # Delete without confirmation (scripting)
acmeeh-admin identifiers add-account <ID> <ACCOUNT_ID>     # Link to ACME account
acmeeh-admin identifiers remove-account <ID> <ACCOUNT_ID>  # Unlink from account
acmeeh-admin identifiers list-for-account <ACCOUNT_ID>     # List identifiers for account
```

#### `profiles` — CSR Profile Management

```bash
acmeeh-admin profiles list                                       # List all profiles
acmeeh-admin profiles create "web-server" '{"key_type":"rsa"}'   # Create profile
acmeeh-admin profiles create "web-server" '{"key_type":"rsa"}' --description "Web servers"
acmeeh-admin profiles get <PROFILE_ID>                           # Get profile details
acmeeh-admin profiles update <ID> "new-name" '{"key_type":"ec"}'                     # Full replacement
acmeeh-admin profiles update <ID> "new-name" '{"key_type":"ec"}' --description "EC profile"
acmeeh-admin profiles delete <PROFILE_ID>                        # Delete (with confirmation)
acmeeh-admin profiles delete <PROFILE_ID> --yes                  # Delete without confirmation (scripting)
acmeeh-admin profiles validate <PROFILE_ID> <CSR_BASE64>         # Dry-run CSR validation
acmeeh-admin profiles assign-account <PROFILE_ID> <ACCOUNT_ID>   # Assign to account
acmeeh-admin profiles unassign-account <PROFILE_ID> <ACCOUNT_ID> # Unassign from account
acmeeh-admin profiles get-for-account <ACCOUNT_ID>               # Get account's profile
```

#### `certificates` — Certificate Operations

```bash
acmeeh-admin certificates search                                   # List all certificates
acmeeh-admin certificates search --domain example.com              # Filter by domain
acmeeh-admin certificates search --status active --limit 10        # Filter by status
acmeeh-admin certificates search --expiring-before 2024-12-31      # Expiring soon
acmeeh-admin certificates search --account-id <ACCT_ID>            # Filter by account
acmeeh-admin certificates search --serial <SERIAL>                 # Filter by serial
acmeeh-admin certificates search --limit 20 --offset 40            # Paginate results
acmeeh-admin certificates get <SERIAL>                             # Get by serial number
acmeeh-admin certificates get-by-fingerprint <SHA256_HEX>          # Get by fingerprint
acmeeh-admin certificates bulk-revoke '{"domain":"old.example.com"}' --dry-run  # Preview
acmeeh-admin certificates bulk-revoke '{"domain":"old.example.com"}' --reason 4 # Revoke
```

#### `notifications` — Notification Management

```bash
acmeeh-admin notifications list                          # List all notifications
acmeeh-admin notifications list --status failed           # Filter by status
acmeeh-admin notifications list --limit 20 --offset 40    # Paginate results
acmeeh-admin notifications retry                          # Retry failed notifications
acmeeh-admin notifications purge                          # Purge sent notifications (30 days)
acmeeh-admin notifications purge --days 7                 # Purge older than 7 days
```

#### `crl` — CRL Management

```bash
acmeeh-admin crl rebuild                         # Force a CRL rebuild
```

#### `maintenance` — Maintenance Mode

```bash
acmeeh-admin maintenance status                  # Get current status
acmeeh-admin maintenance set on                  # Enable maintenance mode
acmeeh-admin maintenance set off                 # Disable maintenance mode
```

### Output Formats

The CLI supports two output formats:

**Table** (default) — human-readable aligned columns:

```
ID                                    USERNAME  EMAIL              ROLE     ENABLED
------------------------------------  --------  -----------------  -------  -------
a1b2c3d4-e5f6-7890-abcd-ef1234567890  admin     admin@example.com  admin    True
```

**JSON** (`--format json`) — machine-readable, suitable for piping to `jq`:

```bash
acmeeh-admin --format json users list | jq '.[].username'
```

Table format details:

- Column values longer than 60 characters are truncated with `...`
- Empty result sets display `(no results)`
- Single-record responses (e.g., `users get`, `users me`) are displayed as indented key-value pairs instead of a table
- Column headers are automatically derived from JSON keys and displayed in uppercase
- The `--format` flag is a global option and must appear **before** the subcommand: `acmeeh-admin --format json users list`

### CLI Output Messages

Mutation commands (create, update, delete, assign, etc.) print specific messages to stdout upon success. These are useful for scripting and verification:

| Command                           | Output on Success                                       |
|-----------------------------------|---------------------------------------------------------|
| `login`                           | `Logged in as <username>`                               |
| `logout`                          | `Logged out.`                                           |
| `users delete`                    | `User deleted.`                                         |
| `identifiers delete`              | `Identifier deleted.`                                   |
| `identifiers add-account`         | `Account associated.`                                   |
| `identifiers remove-account`      | `Account removed.`                                      |
| `profiles delete`                 | `Profile deleted.`                                      |
| `profiles assign-account`         | `Profile assigned.`                                     |
| `profiles unassign-account`       | `Profile unassigned.`                                   |
| `profiles get-for-account`        | `No profile assigned.` (when no profile exists)         |
| `eab add-identifier`              | `OK`                                                    |
| `eab remove-identifier`           | `OK`                                                    |
| `eab assign-profile`              | `OK`                                                    |
| `eab unassign-profile`            | `OK` (or `No CSR profile assigned to this EAB credential.` if none exists) |
| `audit export -o <file>`          | `Exported <N> entries to <file>`                        |

Commands that return structured data (`create`, `get`, `list`, `search`, `me`, `reset-password`, `retry`, `purge`, `rebuild`, `status`, `set`, `revoke`, etc.) print the response in the selected `--format` (table or JSON).

### Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success |
| `1`  | Error — API error, connection failure, or missing configuration |

All API errors and connection failures are caught by the `handle_errors` decorator and printed to stderr before exiting with code 1. Missing server URL also exits with code 1.

### CLI Examples

The following walkthroughs show common operator workflows with sample terminal output.

#### First-Time Setup

```bash
# Log in interactively — saves credentials to ~/.acmeeh-admin.json
$ acmeeh-admin login
Server URL: https://acme.internal
Username: admin
Password: ********
Logged in as admin

# Verify your session
$ acmeeh-admin users me
  id        a1b2c3d4-e5f6-7890-abcd-ef1234567890
  username  admin
  email     admin@example.com
  role      admin
  enabled   True
```

#### Onboarding a New Operator

```bash
# Create an auditor account
$ acmeeh-admin users create jdoe jdoe@example.com
  id        f7e6d5c4-b3a2-1098-7654-321fedcba098
  username  jdoe
  email     jdoe@example.com
  role      auditor
  enabled   True
  password  Xk9#mP2$vL5nQ8

# Promote to admin later
$ acmeeh-admin users update f7e6d5c4-b3a2-1098-7654-321fedcba098 --role admin
  id        f7e6d5c4-b3a2-1098-7654-321fedcba098
  username  jdoe
  email     jdoe@example.com
  role      admin
  enabled   True

# Disable an account
$ acmeeh-admin users update f7e6d5c4-b3a2-1098-7654-321fedcba098 --disabled
  id        f7e6d5c4-b3a2-1098-7654-321fedcba098
  username  jdoe
  email     jdoe@example.com
  role      admin
  enabled   False
```

#### Provisioning EAB Credentials for a New ACME Client

```bash
# Create credentials for a production host
$ acmeeh-admin eab create web-prod-01 --label "Production web server"
  id          c9d8e7f6-5a4b-3c2d-1e0f-a9b8c7d6e5f4
  kid         web-prod-01
  label       Production web server
  hmac_key    base64url-encoded-hmac-key-here
  revoked     False
  used        False
  created_at  2026-02-20T10:30:00Z

# List all credentials
$ acmeeh-admin eab list
ID                                    KID          LABEL                   REVOKED  USED   CREATED_AT
------------------------------------  -----------  ----------------------  -------  -----  --------------------
c9d8e7f6-5a4b-3c2d-1e0f-a9b8c7d6e5f4  web-prod-01  Production web server  False    False  2026-02-20T10:30:00Z

# Revoke a compromised credential
$ acmeeh-admin eab revoke c9d8e7f6-5a4b-3c2d-1e0f-a9b8c7d6e5f4
  id       c9d8e7f6-5a4b-3c2d-1e0f-a9b8c7d6e5f4
  kid      web-prod-01
  revoked  True
```

#### Managing Identifier Allowlists

```bash
# Allow a wildcard domain and a specific IP
$ acmeeh-admin identifiers create dns "*.example.com"
  id                a1234567-b890-cdef-1234-567890abcdef
  identifier_type   dns
  identifier_value  *.example.com

$ acmeeh-admin identifiers create ip 10.0.1.50
  id                b2345678-c901-def0-2345-678901bcdef0
  identifier_type   ip
  identifier_value  10.0.1.50

# Restrict an identifier to a specific ACME account
$ acmeeh-admin identifiers add-account a1234567-b890-cdef-1234-567890abcdef acct-uuid-here
Account associated.

# View identifier details with linked accounts
$ acmeeh-admin identifiers get a1234567-b890-cdef-1234-567890abcdef
  id                a1234567-b890-cdef-1234-567890abcdef
  identifier_type   dns
  identifier_value  *.example.com
  account_ids       ['acct-uuid-here']
```

#### Setting Up CSR Profiles

```bash
# Create a profile enforcing RSA 2048+ keys
$ acmeeh-admin profiles create "web-server" \
    '{"key_type":"rsa","min_key_size":2048,"allowed_sans":["dns"]}' \
    --description "Standard web server profile"
  id           d4567890-ef12-3456-7890-abcdef123456
  name         web-server
  description  Standard web server profile
  created_at   2026-02-20T11:00:00Z

# Assign the profile to an ACME account
$ acmeeh-admin profiles assign-account d4567890-ef12-3456-7890-abcdef123456 acct-uuid-here
Profile assigned.

# Check which profile is assigned to an account
$ acmeeh-admin profiles get-for-account acct-uuid-here
  id           d4567890-ef12-3456-7890-abcdef123456
  name         web-server
  description  Standard web server profile
```

#### Certificate Operations

```bash
# Search for certificates expiring within 30 days
$ acmeeh-admin certificates search --expiring-before 2026-03-22 --status active --limit 5
SERIAL_NUMBER  SAN_VALUES              NOT_AFTER             REVOKED_AT
-------------  ----------------------  --------------------  ----------
01:AB:CD:EF    ['web.example.com']     2026-03-15T00:00:00Z
02:DE:FA:01    ['api.example.com']     2026-03-20T00:00:00Z

# Inspect a specific certificate
$ acmeeh-admin certificates get 01:AB:CD:EF
  serial_number   01:AB:CD:EF
  san_values      ['web.example.com']
  not_before      2025-03-15T00:00:00Z
  not_after       2026-03-15T00:00:00Z
  fingerprint     a1b2c3d4e5f6...
  account_id      acct-uuid-here
  order_id        order-uuid-here
  revoked_at      None
  revocation_reason  None

# Preview a bulk revocation (dry run)
$ acmeeh-admin certificates bulk-revoke '{"domain":"old.example.com"}' --dry-run
  matched  3
  revoked  0
  dry_run  True

# Execute the bulk revocation (reason 4 = superseded)
$ acmeeh-admin certificates bulk-revoke '{"domain":"old.example.com"}' --reason 4
  matched  3
  revoked  3
  dry_run  False
```

#### Audit Log Review

```bash
# Recent audit entries
$ acmeeh-admin audit list --limit 5
ID                                    ACTION          USER_ID                               CREATED_AT            DETAILS
------------------------------------  --------------  ------------------------------------  --------------------  -------
e1234567-...  user.login      a1b2c3d4-...  2026-02-20T09:00:00Z  {}
e2345678-...  cert.revoke     a1b2c3d4-...  2026-02-20T09:15:00Z  {"serial": "01:AB:CD:EF"}
e3456789-...  eab.create      a1b2c3d4-...  2026-02-20T10:30:00Z  {"kid": "web-prod-01"}

# Export a date range to a file for compliance
$ acmeeh-admin audit export --since 2026-01-01 --until 2026-02-01 -o jan-audit.json
Exported 142 entries to jan-audit.json
```

#### Operational Tasks

```bash
# Enable maintenance mode before upgrades
$ acmeeh-admin maintenance set on
  enabled     True
  message     Maintenance mode is active

$ acmeeh-admin maintenance status
  enabled     True
  message     Maintenance mode is active

# Disable after upgrade
$ acmeeh-admin maintenance set off
  enabled     False

# Force a CRL rebuild after mass revocation
$ acmeeh-admin crl rebuild
  status       ok
  last_update  2026-02-20T12:00:00Z

# Retry failed email notifications
$ acmeeh-admin notifications retry
  retried  5

# Purge old notifications (older than 7 days)
$ acmeeh-admin notifications purge --days 7
  purged  23
```

#### Scripting with JSON Output

```bash
# Pipe JSON output to jq for scripting
$ acmeeh-admin --format json users list | jq '.[].username'
"admin"
"jdoe"

# Extract expiring certificate serials into a variable
$ SERIALS=$(acmeeh-admin --format json certificates search \
    --expiring-before 2026-03-22 --status active | jq -r '.[].serial_number')

# Loop over results
$ for serial in $SERIALS; do
    echo "Notifying owner of $serial..."
  done

# One-liner: count active EAB credentials
$ acmeeh-admin --format json eab list | jq '[.[] | select(.revoked == false)] | length'
3

# Use with environment variables (e.g., in CI/CD)
$ export ACMEEH_ADMIN_URL=https://acme.internal
$ export ACMEEH_ADMIN_TOKEN=your-bearer-token
$ acmeeh-admin --format json certificates search --status active | jq length
42

# Without SSL verification (self-signed dev certs)
$ acmeeh-admin --no-verify-ssl --server https://localhost:8443 users me

# Bypass confirmation prompts for automated deletions (--yes)
$ acmeeh-admin users delete $USER_ID --yes
$ acmeeh-admin identifiers delete $ID --yes
$ acmeeh-admin profiles delete $PROFILE_ID --yes
```

---

## Architecture

```
acmeeh_admin/
  __init__.py            # Public API: AcmeehAdminClient, exceptions
  client.py              # AcmeehAdminClient — main entry point
  _http.py               # HttpSession — requests wrapper, auth, error parsing
  _pagination.py         # PaginatedIterator — Link header pagination
  exceptions.py          # AcmeehAdminError, AcmeehAuthenticationError, AcmeehConnectionError
  resources/
    _base.py             # BaseResource — shared base for all resource classes
    auth.py              # AuthResource — login/logout
    users.py             # UsersResource — admin user CRUD
    audit.py             # AuditResource — audit log queries and export
    eab.py               # EabResource — EAB credential management
    identifiers.py       # IdentifiersResource — allowed identifier management
    profiles.py          # ProfilesResource — CSR profile management
    certificates.py      # CertificatesResource — certificate search and bulk ops
    notifications.py     # NotificationsResource — notification management
    crl.py               # CrlResource — CRL rebuild
    maintenance.py       # MaintenanceResource — maintenance mode toggle
  cli/
    main.py              # CLI entry point (click group)
    config.py            # ~/.acmeeh-admin.json management
    output.py            # Table and JSON formatting
    _helpers.py          # pass_client, handle_errors decorators
    auth.py              # login/logout commands
    users.py             # users command group
    audit.py             # audit command group
    eab.py               # eab command group
    identifiers.py       # identifiers command group
    profiles.py          # profiles command group
    certificates.py      # certificates command group
    notifications.py     # notifications command group
    crl.py               # crl command group
    maintenance.py       # maintenance command group
```

The library follows a layered architecture:

1. **`HttpSession`** handles HTTP transport, base URL joining, bearer token injection, SSL config, timeouts, and RFC 7807 error parsing.
2. **Resource classes** map 1:1 to API endpoint groups. Each resource receives the `HttpSession` and exposes typed methods.
3. **`AcmeehAdminClient`** is the top-level facade that composes all resources.
4. **CLI** uses Click decorators. The `pass_client` helper constructs an `AcmeehAdminClient` from the resolved configuration, and `handle_errors` provides clean error output.

---

## REST API Endpoints

The following table lists every REST endpoint the library wraps. All paths are relative to the configured `api_prefix` (default: `/api`).

### Authentication

| Method | Path               | Library Method               | CLI Command          |
|--------|--------------------|------------------------------|----------------------|
| POST   | `/auth/login`      | `client.login()`             | `acmeeh-admin login` |
| POST   | `/auth/logout`     | `client.logout()`            | `acmeeh-admin logout`|

### Users

| Method | Path                 | Library Method                 | CLI Command                  |
|--------|----------------------|--------------------------------|------------------------------|
| GET    | `/users`             | `client.users.list()`          | `users list`                 |
| POST   | `/users`             | `client.users.create()`        | `users create`               |
| GET    | `/users/{id}`        | `client.users.get()`           | `users get`                  |
| PATCH  | `/users/{id}`        | `client.users.update()`        | `users update`               |
| DELETE | `/users/{id}`        | `client.users.delete()`        | `users delete`               |
| GET    | `/me`                | `client.users.me()`            | `users me`                   |
| POST   | `/me/reset-password` | `client.users.reset_password()`| `users reset-password`       |

### Audit Log

| Method | Path                | Library Method           | CLI Command    |
|--------|---------------------|--------------------------|----------------|
| GET    | `/audit-log`        | `client.audit.list()`    | `audit list`   |
| GET    | `/audit-log` (all)  | `client.audit.list_all()`| —              |
| POST   | `/audit-log/export` | `client.audit.export()`  | `audit export` |

### EAB Credentials

| Method | Path                                               | Library Method                        | CLI Command                |
|--------|-----------------------------------------------------|---------------------------------------|----------------------------|
| GET    | `/eab`                                              | `client.eab.list()`                   | `eab list`                 |
| POST   | `/eab`                                              | `client.eab.create()`                 | `eab create`               |
| GET    | `/eab/{id}`                                         | `client.eab.get()`                    | `eab get`                  |
| POST   | `/eab/{id}/revoke`                                  | `client.eab.revoke()`                 | `eab revoke`               |
| PUT    | `/eab/{id}/allowed-identifiers/{identifier_id}`     | `client.eab.add_identifier()`         | `eab add-identifier`       |
| DELETE | `/eab/{id}/allowed-identifiers/{identifier_id}`     | `client.eab.remove_identifier()`      | `eab remove-identifier`    |
| GET    | `/eab/{id}/allowed-identifiers`                     | `client.eab.list_identifiers()`       | `eab list-identifiers`     |
| PUT    | `/eab/{id}/csr-profile/{profile_id}`                | `client.eab.assign_csr_profile()`     | `eab assign-profile`       |
| DELETE | `/eab/{id}/csr-profile/{profile_id}`                | `client.eab.unassign_csr_profile()`   | `eab unassign-profile` *   |
| GET    | `/eab/{id}/csr-profile`                             | `client.eab.get_csr_profile()`        | `eab get-profile`          |

> \* The `eab unassign-profile` CLI command only takes `<EAB_ID>`. It automatically looks up the currently assigned profile and resolves the `profile_id` before calling the DELETE endpoint. If no profile is assigned, it prints a message and exits without making a request.

### Allowed Identifiers

| Method | Path                                                    | Library Method                           | CLI Command                      |
|--------|----------------------------------------------------------|------------------------------------------|----------------------------------|
| GET    | `/allowed-identifiers`                                   | `client.identifiers.list()`              | `identifiers list`               |
| POST   | `/allowed-identifiers`                                   | `client.identifiers.create()`            | `identifiers create`             |
| GET    | `/allowed-identifiers/{id}`                              | `client.identifiers.get()`               | `identifiers get`                |
| DELETE | `/allowed-identifiers/{id}`                              | `client.identifiers.delete()`            | `identifiers delete`             |
| PUT    | `/allowed-identifiers/{id}/accounts/{account_id}`        | `client.identifiers.add_account()`       | `identifiers add-account`        |
| DELETE | `/allowed-identifiers/{id}/accounts/{account_id}`        | `client.identifiers.remove_account()`    | `identifiers remove-account`     |
| GET    | `/accounts/{account_id}/allowed-identifiers`             | `client.identifiers.list_for_account()`  | `identifiers list-for-account`   |

### CSR Profiles

| Method | Path                                              | Library Method                         | CLI Command                     |
|--------|---------------------------------------------------|----------------------------------------|---------------------------------|
| GET    | `/csr-profiles`                                   | `client.profiles.list()`               | `profiles list`                 |
| POST   | `/csr-profiles`                                   | `client.profiles.create()`             | `profiles create`               |
| GET    | `/csr-profiles/{id}`                              | `client.profiles.get()`                | `profiles get`                  |
| PUT    | `/csr-profiles/{id}`                              | `client.profiles.update()`             | `profiles update`               |
| DELETE | `/csr-profiles/{id}`                              | `client.profiles.delete()`             | `profiles delete`               |
| POST   | `/csr-profiles/{id}/validate`                     | `client.profiles.validate()`           | `profiles validate`             |
| PUT    | `/csr-profiles/{id}/accounts/{account_id}`        | `client.profiles.assign_account()`     | `profiles assign-account`       |
| DELETE | `/csr-profiles/{id}/accounts/{account_id}`        | `client.profiles.unassign_account()`   | `profiles unassign-account`     |
| GET    | `/accounts/{account_id}/csr-profile`              | `client.profiles.get_for_account()`    | `profiles get-for-account`      |

### Certificates

| Method | Path                                       | Library Method                          | CLI Command                        |
|--------|--------------------------------------------|-----------------------------------------|------------------------------------|
| GET    | `/certificates`                            | `client.certificates.search()`          | `certificates search`              |
| GET    | `/certificates/{serial}`                   | `client.certificates.get_by_serial()`   | `certificates get`                 |
| GET    | `/certificates/by-fingerprint/{fp}`        | `client.certificates.get_by_fingerprint()` | `certificates get-by-fingerprint` |
| POST   | `/certificates/bulk-revoke`                | `client.certificates.bulk_revoke()`     | `certificates bulk-revoke`         |

### Notifications

| Method | Path                     | Library Method                     | CLI Command              |
|--------|--------------------------|-------------------------------------|--------------------------|
| GET    | `/notifications`         | `client.notifications.list()`       | `notifications list`     |
| POST   | `/notifications/retry`   | `client.notifications.retry()`      | `notifications retry`    |
| POST   | `/notifications/purge`   | `client.notifications.purge()`      | `notifications purge`    |

### CRL

| Method | Path            | Library Method         | CLI Command    |
|--------|-----------------|------------------------|----------------|
| POST   | `/crl/rebuild`  | `client.crl.rebuild()` | `crl rebuild`  |

### Maintenance

| Method | Path             | Library Method                       | CLI Command          |
|--------|------------------|--------------------------------------|----------------------|
| GET    | `/maintenance`   | `client.maintenance.get_status()`    | `maintenance status` |
| POST   | `/maintenance`   | `client.maintenance.set_status()`    | `maintenance set`    |

---

## Testing

Run the test suite:

```bash
pip install -e ".[dev]"
pytest tests/
```

Tests use the [`responses`](https://github.com/getsentry/responses) library to mock HTTP calls without hitting a real server.

### Test Structure

```
tests/
  conftest.py                   # Shared fixtures (mocked_responses, client)
  test_client.py                # AcmeehAdminClient composition and auth delegation
  test_http.py                  # HttpSession transport, URL joining, error parsing
  test_http_extended.py         # Timeout, connection errors, SSL config
  test_pagination.py            # Link header parsing
  test_pagination_iterator.py   # PaginatedIterator multi-page collection
  resources/
    test_auth.py                # Login/logout token handling
    test_users.py               # Admin user CRUD
    test_audit.py               # Audit log listing and export
    test_audit_extended.py      # Audit list_all pagination and export filters
    test_eab.py                 # EAB credential management
    test_eab_extended.py        # EAB identifier/profile linkage
    test_identifiers.py         # Allowed identifier management
    test_profiles.py            # CSR profile management
    test_certificates.py        # Certificate search and bulk revoke
    test_notifications.py       # Notification list, retry, purge
    test_notifications_extended.py # Notification filter edge cases
    test_crl.py                 # CRL rebuild
    test_maintenance.py         # Maintenance mode toggle
  cli/
    conftest.py                 # CLI test fixtures (Click CliRunner)
    test_main.py                # CLI group and global options
    test_config.py              # Config file load/save/resolution
    test_helpers.py             # pass_client and handle_errors decorators
    test_output.py              # Table and JSON formatting
    test_auth.py                # login/logout commands
    test_users.py               # users command group
    test_audit.py               # audit command group
    test_eab.py                 # eab command group
    test_identifiers.py         # identifiers command group
    test_profiles.py            # profiles command group
    test_certificates.py        # certificates command group
    test_notifications.py       # notifications command group
    test_crl.py                 # crl command group
    test_maintenance.py         # maintenance command group
```

Run a specific test file or test:

```bash
pytest tests/test_client.py
pytest tests/resources/test_eab.py -k "test_revoke"
pytest tests/ -v           # Verbose output
```

## Security Considerations

### Token Storage

The CLI stores bearer tokens in **plaintext** in `~/.acmeeh-admin.json`. Ensure this file has restrictive permissions:

```bash
chmod 600 ~/.acmeeh-admin.json
```

On shared systems, prefer passing the token via the `ACMEEH_ADMIN_TOKEN` environment variable or the `--token` CLI flag instead of relying on the config file.

### SSL Verification

When `verify_ssl=False` is set (or `--no-verify-ssl` is used), the library suppresses `urllib3` InsecureRequestWarning messages. This is intended for development environments with self-signed certificates. **Always enable SSL verification in production.**

### Sensitive Response Data

Certain API responses contain secrets that are only available once:

- `users create` — returns the generated password in the response
- `eab create` — returns the HMAC key in the response
- `users reset-password` — returns the new password in the response

These values are not retrievable again. Store them securely immediately after creation.

---

## Troubleshooting

### Connection Refused

```
Connection error: Cannot connect to https://acme.internal: ...
```

- Verify the server URL is correct and the ACMEEH server is running.
- Check firewall rules and network connectivity.
- If behind a proxy, set `HTTP_PROXY`/`HTTPS_PROXY` environment variables.

### SSL Certificate Errors

```
Connection error: Cannot connect to https://acme.internal: SSLError(...)
```

- For self-signed development certificates, use `--no-verify-ssl` (CLI) or `verify_ssl=False` (library).
- In production, install the CA certificate in the system trust store instead of disabling verification.

### Authentication Failures

```
Error [401]: Unauthorized
```

- Token may have expired — run `acmeeh-admin login` to get a fresh token.
- Verify the token is being resolved correctly: check `--token` flag, `ACMEEH_ADMIN_TOKEN` env var, and `~/.acmeeh-admin.json`.
- Confirm the user account is enabled: `acmeeh-admin users me`.

### Missing Server URL

```
Error: No server URL. Use --server, ACMEEH_ADMIN_URL, or 'acmeeh-admin login'.
```

- Run `acmeeh-admin login` to save the server URL to the config file, or pass `--server` explicitly, or set `ACMEEH_ADMIN_URL`.

### JSON Parse Errors in CLI

```
json.JSONDecodeError: ...
```

- When passing JSON arguments (e.g., `bulk-revoke`, `profiles create`), ensure the JSON string is valid and properly quoted for your shell:
  ```bash
  # Correct (single quotes around JSON)
  acmeeh-admin profiles create "name" '{"key_type":"rsa"}'

  # Windows cmd (escaped double quotes)
  acmeeh-admin profiles create "name" "{\"key_type\":\"rsa\"}"
  ```

---

## Contributing

### Development Setup

```bash
git clone <repo-url>
cd acmeeh-admin
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/                              # Full test suite
pytest tests/ -v                           # Verbose output
pytest tests/test_client.py                # Single file
pytest tests/resources/test_eab.py -k "test_revoke"  # Single test
```

### Code Style

- Type annotations on all public methods (Python 3.10+ union syntax `X | Y`)
- `from __future__ import annotations` in all modules (except `__init__.py`)
- Private modules prefixed with underscore (`_http.py`, `_pagination.py`, `_helpers.py`)
- Resource classes inherit from `BaseResource`
- CLI commands use `@handle_errors` and `@pass_client` decorators
- Confirmation prompts on destructive CLI operations (`delete`) via `@click.confirmation_option` (skippable with `--yes`)

### Project Layout

- Source code lives in `src/acmeeh_admin/` (src layout)
- Tests mirror the source structure under `tests/`
- Build configuration is in `pyproject.toml` (setuptools backend)

---

## License

MIT
