# File Prompt CLI

A CLI tool for dispatching files to GCP Pub/Sub and listening for results.

## Installation

```bash
pip install file-prompt-tool
```

## Usage

The CLI tool provides a single command to dispatch files to GCP Pub/Sub and listen for results:

```bash
file-prompt "*.txt" \
  --prompt "Summarize this text" \
  --project-id "your-project-id" \
  --bucket "your-bucket-name" \
  --topic "your-topic-name" \
  --subscription "your-subscription-name"
```

### Arguments

- `files`: File paths or glob patterns to process (required)
- `--prompt`, `-p`: Prompt to use for processing (required)
- `--project-id`: GCP project ID (required)
- `--bucket`: GCS bucket name (required)
- `--topic`: Pub/Sub topic name (required)
- `--subscription`: Pub/Sub subscription name (required)
- `--timeout`, `-t`: Timeout in seconds for processing each file (default: 300)
- `--verbose`, `-v`: Enable verbose output (default: false)

### Example

```bash
# Process all text files in the current directory
file-prompt "*.txt" \
  --prompt "Summarize this text" \
  --project-id "my-project" \
  --bucket "my-bucket" \
  --topic "file-processing" \
  --subscription "file-results"

# Process specific files with verbose output
file-prompt file1.txt file2.txt \
  --prompt "Analyze this document" \
  --project-id "my-project" \
  --bucket "my-bucket" \
  --topic "file-processing" \
  --subscription "file-results" \
  --verbose
```

## Development

### Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:
```bash
black .
isort .
flake8
mypy .
```

## License

MIT
