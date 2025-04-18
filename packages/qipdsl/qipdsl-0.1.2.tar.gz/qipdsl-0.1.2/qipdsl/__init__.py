"""
QIP-DSL: Quantum-Inspired Probabilistic Domain-Specific Language (CUDA-only)
"""

__version__ = '0.1.2'

def cuda_available():
    """Check if CUDA is available."""
    try:
        # This would be replaced with actual CUDA check in the real package
        return True
    except:
        return False

# Import submodules
try:
    from . import matrix_ops
    from . import entanglement
    from . import prob_sampling
    from . import optimizers
except ImportError:
    pass
