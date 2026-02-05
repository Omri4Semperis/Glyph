"""
Python-specific code parser using the ast module.
"""
import ast
from typing import List, Tuple, Union

from tools.parsers.base_parser import BaseParser
from tools.parsers.shared_models import (
    FileMetrics,
    ClassMetrics,
    MethodMetrics,
    calculate_line_stats
)


class PythonParser(BaseParser):
    """Parser for Python source files using the ast module."""
    
    @property
    def language_name(self) -> str:
        return "python"
    
    @property
    def file_extensions(self) -> Tuple[str, ...]:
        return ('.py',)
    
    def parse_file(self, file_path: str) -> FileMetrics:
        """Parse a Python file and return its metrics."""
        try:
            content, lines = self.read_file(file_path)
        except Exception as e:
            return FileMetrics(
                path=file_path,
                language=self.language_name,
                line_count=0,
                class_count=0,
                function_count=0,
                parse_error=f"Failed to read file: {str(e)}"
            )
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return FileMetrics(
                path=file_path,
                language=self.language_name,
                line_count=len(lines),
                class_count=0,
                function_count=0,
                line_stats=calculate_line_stats(lines),
                parse_error=f"Syntax error: {str(e)}"
            )
        
        classes: List[ClassMetrics] = []
        functions: List[MethodMetrics] = []
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(self._analyze_class(node, lines))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(self._analyze_function(node, lines))
        
        return FileMetrics(
            path=file_path,
            language=self.language_name,
            line_count=len(lines),
            class_count=len(classes),
            function_count=len(functions),
            classes=classes,
            functions=functions,
            line_stats=calculate_line_stats(lines)
        )
    
    def _count_function_args(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> int:
        """Count the number of arguments in a function, excluding 'self' and 'cls'."""
        args = node.args
        total = len(args.args) + len(args.posonlyargs) + len(args.kwonlyargs)
        
        # Exclude 'self' and 'cls' for methods
        if args.args:
            first_arg = args.args[0].arg
            if first_arg in ('self', 'cls'):
                total -= 1
        
        # Add *args and **kwargs if present
        if args.vararg:
            total += 1
        if args.kwarg:
            total += 1
        
        return total
    
    def _analyze_function(
        self,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        file_lines: List[str]
    ) -> MethodMetrics:
        """Analyze a function/method node."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        
        # Get the lines belonging to this function
        func_lines = file_lines[line_start - 1:line_end]
        
        # Check if async
        is_async = isinstance(node, ast.AsyncFunctionDef)
        
        # Check for decorators that might indicate static
        is_static = any(
            (isinstance(d, ast.Name) and d.id == 'staticmethod') or
            (isinstance(d, ast.Attribute) and d.attr == 'staticmethod')
            for d in node.decorator_list
        )
        
        return MethodMetrics(
            name=node.name,
            line_start=line_start,
            line_end=line_end,
            line_count=line_end - line_start + 1,
            arg_count=self._count_function_args(node),
            line_stats=calculate_line_stats(func_lines),
            is_async=is_async,
            is_static=is_static
        )
    
    def _analyze_class(self, node: ast.ClassDef, file_lines: List[str]) -> ClassMetrics:
        """Analyze a class node."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        
        # Get the lines belonging to this class
        class_lines = file_lines[line_start - 1:line_end]
        
        # Find __init__ and count its parameters
        constructor_param_count = 0
        methods: List[MethodMetrics] = []
        
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_metrics = self._analyze_function(item, file_lines)
                methods.append(method_metrics)
                
                if item.name == '__init__':
                    constructor_param_count = method_metrics.arg_count
        
        # Get base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(f"{base.value.id if isinstance(base.value, ast.Name) else '...'}.{base.attr}")
        
        return ClassMetrics(
            name=node.name,
            line_start=line_start,
            line_end=line_end,
            line_count=line_end - line_start + 1,
            constructor_param_count=constructor_param_count,
            method_count=len(methods),
            methods=methods,
            line_stats=calculate_line_stats(class_lines),
            base_classes=base_classes
        )