"""
Shared data models for code analysis parsers.
"""
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class LineStats:
    """Statistics for line lengths."""
    count: int = 0
    min_length: int = 0
    max_length: int = 0
    mean_length: float = 0.0
    median_length: float = 0.0
    std_length: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "count": self.count,
            "min": self.min_length,
            "max": self.max_length,
            "mean": round(self.mean_length, 2),
            "median": round(self.median_length, 2),
            "std": round(self.std_length, 2)
        }


@dataclass
class MethodMetrics:
    """Metrics for a single method/function."""
    name: str
    line_start: int
    line_end: int
    line_count: int
    arg_count: int
    line_stats: LineStats = field(default_factory=LineStats)
    # Optional language-specific fields
    access_modifier: Optional[str] = None  # public, private, protected, internal
    return_type: Optional[str] = None
    is_async: bool = False
    is_static: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "name": self.name,
            "lines": {
                "start": self.line_start,
                "end": self.line_end,
                "count": self.line_count
            },
            "arg_count": self.arg_count,
            "line_length_stats": self.line_stats.to_dict()
        }
        if self.access_modifier:
            result["access_modifier"] = self.access_modifier
        if self.return_type:
            result["return_type"] = self.return_type
        if self.is_async:
            result["is_async"] = True
        if self.is_static:
            result["is_static"] = True
        return result


@dataclass
class ClassMetrics:
    """Metrics for a single class."""
    name: str
    line_start: int
    line_end: int
    line_count: int
    constructor_param_count: int  # Parameters in constructor (__init__ for Python, ctor for C#)
    method_count: int
    methods: List[MethodMetrics] = field(default_factory=list)
    line_stats: LineStats = field(default_factory=LineStats)
    # Optional language-specific fields
    access_modifier: Optional[str] = None
    property_count: int = 0
    is_abstract: bool = False
    is_static: bool = False
    base_classes: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "name": self.name,
            "lines": {
                "start": self.line_start,
                "end": self.line_end,
                "count": self.line_count
            },
            "constructor_param_count": self.constructor_param_count,
            "method_count": self.method_count,
            "methods": [m.to_dict() for m in self.methods],
            "line_length_stats": self.line_stats.to_dict()
        }
        if self.access_modifier:
            result["access_modifier"] = self.access_modifier
        if self.property_count > 0:
            result["property_count"] = self.property_count
        if self.is_abstract:
            result["is_abstract"] = True
        if self.is_static:
            result["is_static"] = True
        if self.base_classes:
            result["base_classes"] = self.base_classes
        if self.interfaces:
            result["interfaces"] = self.interfaces
        return result


@dataclass
class FileMetrics:
    """Metrics for a single file."""
    path: str
    language: str  # "python", "csharp", etc.
    line_count: int
    class_count: int
    function_count: int  # Top-level functions (or namespace-level for C#)
    classes: List[ClassMetrics] = field(default_factory=list)
    functions: List[MethodMetrics] = field(default_factory=list)
    line_stats: LineStats = field(default_factory=LineStats)
    parse_error: Optional[str] = None
    # Optional language-specific fields
    namespaces: List[str] = field(default_factory=list)
    using_statements: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "path": self.path,
            "language": self.language,
            "line_count": self.line_count,
            "class_count": self.class_count,
            "function_count": self.function_count,
            "line_length_stats": self.line_stats.to_dict()
        }
        if self.classes:
            result["classes"] = [c.to_dict() for c in self.classes]
        if self.functions:
            result["functions"] = [f.to_dict() for f in self.functions]
        if self.parse_error:
            result["parse_error"] = self.parse_error
        if self.namespaces:
            result["namespaces"] = self.namespaces
        if self.using_statements:
            result["using_statements"] = self.using_statements
        return result


def calculate_line_stats(lines: List[str]) -> LineStats:
    """Calculate statistics for a list of lines."""
    if not lines:
        return LineStats()
    
    lengths = [len(line) for line in lines]
    
    return LineStats(
        count=len(lines),
        min_length=min(lengths),
        max_length=max(lengths),
        mean_length=statistics.mean(lengths),
        median_length=statistics.median(lengths),
        std_length=statistics.stdev(lengths) if len(lengths) > 1 else 0.0
    )