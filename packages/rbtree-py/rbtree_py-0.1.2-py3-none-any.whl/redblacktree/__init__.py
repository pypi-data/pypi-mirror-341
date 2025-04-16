# redblacktree/__init__.py
"""
A Python implementation of a Red-Black Tree data structure.
"""

from .tree import RedBlackTree, RBNode, RED, BLACK

__version__ = "0.1.2"

__all__ = [
    "RedBlackTree",
    "RBNode",
    "RED",
    "BLACK",
    "__version__",
]
