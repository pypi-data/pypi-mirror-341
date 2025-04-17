# py-net-diags

A Python package for network diagnostics that collects various metrics about your machine's network connection.

## Installation

### Basic Installation

```bash
pip install py-net-diags
```

### With Optional speedcheck Support

```bash
pip install py-net-diags[speedcheck]
```

## Configuration

### Environment Variables

Create a `.env` file based on the provided `.env-sample`:

```
# ConnectWise API Configuration
RUNNING_IN_ASIO=true/false    # Set to true if running in ASIO environment
CW_BASE_URL=your_cw_url       # ConnectWise base URL
AUTHORIZATION=your_auth_token # ConnectWise authorization token
CLIENTID=your_client_id       # ConnectWise client ID

# Retry Configuration
RETRY_ATTEMPTS=3              # Number of retry attempts for operations
RETRY_DELAY=2                 # Delay in seconds between retry attempts
```

### Input Configuration

Create an `input.json` file to specify endpoints to scan:

```json
{
  "Endpoints_1744302956989": "cloudflare.com,10.0.0.1",
  "ticket_id": "12345"        # Optional: ConnectWise ticket ID
}
```

You can add any number of comma-separated endpoints to scan.

## Usage Examples

```python
from py_net_diags.network_diagnostics import NetworkDiagnostics

# Initialize the diagnostics tool
diag = NetworkDiagnostics()

# Run all diagnostics
results = diag.run_diagnostics()
print(results)

# Save the results to a file (txt, json, pdf)
diag.save_results_as_txt("/path/to/output.txt")
diag.save_results_as_json("/path/to/output.json")
diag.save_results_as_pdf("/path/to/output.pdf")
```

## Conda Environment Setup

### Basic Environment

```yaml
name: net-diags
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
    - py-net-diags
```

### With speedcheck Support

```yaml
name: net-diags-full
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
    - "py-net-diags[speedcheck]"
```

Save either of these as `environment.yml` and create the environment with:

```bash
conda env create -f environment.yml
```

## License

MIT