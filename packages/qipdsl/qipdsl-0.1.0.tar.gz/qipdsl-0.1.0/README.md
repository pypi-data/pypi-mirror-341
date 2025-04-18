# QIP-DSL CUDA-ONLY PACKAGE

This is a CUDA-only build of QIP-DSL, designed for production use on systems with NVIDIA GPUs.

## Requirements

- CUDA 12.8.61 or higher
- NVIDIA GPU with Compute Capability 6.0 or higher
- Python 3.6 or higher

## Installation

```bash
# Install from the provided wheel file
pip install qipdsl-0.1.0-cuda-only.whl

# Or install from source
pip install -e .
```

## Important Note

This package will **NOT** work on systems without CUDA. It will raise an error
at runtime if no CUDA-capable devices are found.

## Documentation

See the `docs/` directory for complete documentation.
