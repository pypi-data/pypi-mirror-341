# QIP-DSL: Quantum-Inspired Probabilistic Domain-Specific Language (CUDA-only)

QIP-DSL is a high-performance Quantum-Inspired Probabilistic Domain-Specific Language designed for quantum simulation, optimization, and machine learning tasks. It leverages CUDA for GPU acceleration to provide exceptional performance for matrix operations and quantum-inspired algorithms.

## Features

- **CUDA-Accelerated Matrix Operations**: High-performance matrix operations optimized for NVIDIA GPUs
- **Quantum-Inspired Algorithms**: Implementations of quantum-inspired optimization and simulation algorithms
- **Entanglement Simulation**: Tools for simulating quantum entanglement and related phenomena
- **Probabilistic Sampling**: Efficient sampling from complex probability distributions

## Requirements

- CUDA 12.0 or higher
- NVIDIA GPU with Compute Capability 6.0 or higher
- Python 3.6 or higher

## Installation

```bash
pip install qipdsl
```

## Important Note

This package will **NOT** work on systems without CUDA. It will raise an error at runtime if no CUDA-capable devices are found.
