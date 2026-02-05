"""
Language-specific code parsers for static analysis.
"""
from tools.parsers.base_parser import BaseParser
from tools.parsers.python_parser import PythonParser
from tools.parsers.csharp_parser import CSharpParser
from tools.parsers.shared_models import (
    LineStats,
    MethodMetrics,
    ClassMetrics,
    FileMetrics,
    calculate_line_stats
)

__all__ = [
    'BaseParser',
    'PythonParser', 
    'CSharpParser',
    'LineStats',
    'MethodMetrics',
    'ClassMetrics',
    'FileMetrics',
    'calculate_line_stats'
]