"""
Scoras package initialization.
"""

__version__ = "0.2.3"
__author__ = "Anderson L. Amaral"

# Import core functionality
from .core import ScoringMixin, Graph, Node, Edge

# Provide convenience imports
__all__ = ['ScoringMixin', 'Graph', 'Node', 'Edge']
