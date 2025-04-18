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

## Usage Examples

```python
from py_net_diags import NetworkDiagnostics

# Initialize the diagnostics tool
diag = NetworkDiagnostics()

# Run all diagnostics
results = diag.run_diagnostics()
print(results)

# Save the results to a file (txt, json, pdf)
paths = {
    "txt": "/path/to/output.txt",
    "json": "/path/to/output.json",
    "pdf": "/path/to/output.pdf"
}

diag.save_results_as_txt(paths["txt"])
diag.save_results_as_json(paths["json"])
diag.save_results_as_pdf(paths["pdf"])

# Optional: Upload to CW_PSA
import logging
from py_net_diags import ConnectWiseServiceAPI

logger = logging.getLogger(__name__)

service_api = ConnectWiseServiceAPI(log=logger)

# Makes sure the ticket id is an integer
ticket_id = diag.parse_ticket_id(ticket_id)

# Add an internal note:
note_response = service_api.add_ticket_note(ticket_id=ticket_id, note_text=md_msg, internal=True)
print(note_response)

# Add the PDF as an attachment on the ticket:
attachment_response = service_api.upload_attachment(ticket_id=ticket_id, file_path=paths["pdf"])
print(attachment_response)
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
