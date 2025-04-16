"""
dtustatspy: A demonstration package for statistical analysis.

This package provides tools for sampling and analysis. The main sample
function is exposed directly at the package level for convenience.
"""

from .samples import sample

__all__ = ['sample']