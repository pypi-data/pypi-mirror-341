# redblacktree/__init__.py
"""
A Python implementation of a Red-Black Tree data structure.
"""

from .tree import BLACK, RED, RBNode, RedBlackTree

__version__ = "0.1.4"

__all__ = [
    "RedBlackTree",
    "RBNode",
    "RED",
    "BLACK",
    "__version__",
]
