# Scribe Python Client

The Scribe Python Client is a library for interacting with the ScribeHub API. It provides a simple interface for accessing datasets, querying vulnerabilities, and managing products.

## Installation

Install the package using pip:

```bash
pip install scribe-python-client
```

## Usage
The client requires an API token for authentication. You can obtain your API token from the ScribeHub dashboard.
The CLI supports providing the `SCRIBE_TOKEN` as an argument, `--api-key`. You can set the `SCRIBE_TOKEN` environment variable to avoid passing the `--api_token` argument:

```bash
export SCRIBE_TOKEN=YOUR_API_TOKEN
scribe-client --api_call get-products
```

### CLI Usage

The package includes a CLI tool for quick interactions. After installation, you can use the `scribe-client` command. Below are examples for all supported commands:

### Examples

#### Get Products
Retrieve a list of products managed in Scribe:
```bash
scribe-client --api-call get-products --api-token YOUR_API_TOKEN
```
#### Get Product Vulnerabilities
Retrieve vulnerabilities for a specific product:
```bash
scribe-client --api-call get-product-vulnerabilities --product-name YOUR_PRODUCT_NAME --api-token YOUR_API_TOKEN
```

#### Get Policy Results
Retrieve policy results for a specific product:
```bash
scribe-client --api-call get-policy-results --product-name YOUR_PRODUCT_NAME --api-token YOUR_API_TOKEN
```

#### Get Datasets
Retrieve all datasets:
```bash
scribe-client --api-call get-datasets --api-token YOUR_API_TOKEN
```

#### List Attestations
List all attestations:
```bash
scribe-client --api-call list-attestations --api-token YOUR_API_TOKEN
```
#### Get Attestation
Retrieve a specific attestation by ID:
```bash
scribe-client --api-call get-attestation --attestation-id YOUR_ATTESTATION_ID --api-token YOUR_API_TOKEN
```
Attestation IDs ca n be obtained from the list of attestations - search for 'id' in the output.

#### Get Latest Attestation
Retrieve the latest attestation for a specific product:
```bash
scribe-client --api-call get-latest-attestation --product-name YOUR_PRODUCT_NAME --api-token YOUR_API_TOKEN
```

## Specific Dataset Commands

The Scribe Python Client allows you to interact with specific datasets for advanced queries and data retrieval. Below are details about these commands and examples of how to use them.

### Querying Specific Datasets

You can query specific datasets such as vulnerabilities, products, policies, and lineage. These commands allow you to run custom queries and retrieve detailed information.

#### Query Vulnerabilities Dataset
Run a custom query on the vulnerabilities dataset:
```bash
scribe-client --api-call query-vulnerabilities --query "{\"columns\": [\"vulnerability_id\", \"severity\"], \"filters\": [{\"col\": \"severity\", \"op\": \"==\", \"val\": \"High\"}], \"orderby\": [], \"row_limit\": 10}"
```

#### Query Products Dataset
Run a custom query on the products dataset:
```bash
scribe-client --api-call query-products --query "{\"columns\": [\"logical_app\", \"logical_app_version\"], \"filters\": [{\"col\": \"logical_app\", \"op\": \"like\", \"val\": \"%example%\"}], \"orderby\": [], \"row_limit\": 5}"
```

#### Query Policy Results Dataset
Run a custom query on the policy results dataset:
```bash
scribe-client --api-call query-policy-results --query "{\"columns\": [\"status\", \"time_evaluated\"], \"filters\": [{\"col\": \"status\", \"op\": \"==\", \"val\": \"Passed\"}], \"orderby\": [], \"row_limit\": 10}"
```

#### Query Lineage Dataset
Run a custom query on the lineage dataset:
```bash
scribe-client --api-call query-lineage --query "{\"columns\": [\"asset_name\", \"asset_type\"], \"filters\": [{\"col\": \"asset_type\", \"op\": \"==\", \"val\": \"repo\"}], \"orderby\": [], \"row_limit\": 10}"
```

### Notes
- Replace the `--query` argument with your desired query in JSON format.
- Ensure that the query structure matches the dataset schema for accurate results.
- Use the `--api-token` argument or set the `SCRIBE_TOKEN` environment variable for authentication.

### Library Usage

You can also use the library programmatically in your Python code:

```python
from scribe_python_client.client import ScribeClient

# Initialize the client
client = ScribeClient(api_token="YOUR_API_TOKEN")

# Get products
products = client.get_products()
print(products)

# Get datasets
datasets = client.get_datasets()
print(datasets)
```

## Features

- **Get Products**: Retrieve a list of products managed in Scribe.
- **Query Datasets**: Query datasets for vulnerabilities, policy results, and more.
- **CLI Support**: Use the `scribe-client` command for quick API interactions.

## Function Groups

The library provides the following hierarchical function groups:

### 1. Product Management
- **Get Products**: Retrieve a list of products managed in Scribe.
- **Get Product Vulnerabilities**: Retrieve vulnerabilities for a specific product.

### 2. Dataset Management
- **Get Datasets**: Retrieve all datasets.
- **Query Datasets**: Query datasets for vulnerabilities, policy results, and more.

### 3. Policy Management
- **Get Policy Results**: Retrieve policy results for a specific product.

### 4. Attestation Management
- **List Attestations**: List all attestations.
- **Get Attestation**: Retrieve a specific attestation by ID.
- **Get Latest Attestation**: Retrieve the latest attestation for a specific product.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.