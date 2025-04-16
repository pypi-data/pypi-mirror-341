# Dynaccount

**Dynaccount** is a Python client for the [Dynatrace Account Management API].
It focuses on providing Dynatrace administrators an easier way to understand their environments, groups, policies, and subscription usage.

[Dynatrace Account Management API]: https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/account-management-api

## Requirements

1. Python 3.8 or higher
2. OAuth Client Credentials with scopes: account-env-read account-idm-read iam-policies-management

## Install

```bash
$ pip install dt
```

## Example Use Case

```python
import dynaccount

# Initialize client class
account_client = dynaccount.DynatraceClient("client_id_goes_here", "client_secret_goes_here", "account_urn_goes_here")

# Get policies matching your keyword search (regex is supported)
all_account_policies_detailed = dynaccount.get_policies_detailed(account_client, "search_policies_here", regex=False)

# Initialize exporter class
exporter = dynaccount.Exporter()

# Export to JSON
exporter.policies_to_json(all_account_policies_detailed)
```

## To-Do

- Create tests
- Dynamic scope options
- Add write functionality
- Introduce all API endpoints