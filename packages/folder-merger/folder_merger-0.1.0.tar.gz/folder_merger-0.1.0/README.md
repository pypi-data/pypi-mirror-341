# Folder Merger

A Python utility for safely merging multiple folders while handling file conflicts intelligently.

## Features

- Recursively merges folders while preserving directory structure
- Detects and handles file conflicts automatically
- Skips duplicate files using MD5 hash comparison
- Progress tracking with tqdm
- Comprehensive logging

## Installation

```bash
pip install folder-merger
```

## Usage

### Command Line Interface

```bash
folder-merger --source /path/to/source --destination /path/to/destination
```

### Python API

```python
from folder_merger import MergeManager

manager = MergeManager(
    source_root="/path/to/source",
    output_path="/path/to/destination"
)
manager.merge_all()
```

## How it Works

1. The tool recursively walks through the source directory
2. For each file:
   - Checks if file exists in destination
   - If file exists, compares MD5 hashes to detect duplicates
   - If files are different, creates a conflict copy with "_conflict" suffix
   - If file doesn't exist, copies it to destination

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 