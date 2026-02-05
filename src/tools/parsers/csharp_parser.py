"""
C#-specific code parser using regex-based parsing.
"""
import re
from typing import List, Tuple, Optional, Dict, Any

from tools.parsers.base_parser import BaseParser
from tools.parsers.shared_models import (
    FileMetrics,
    ClassMetrics,
    MethodMetrics,
    calculate_line_stats
)


class CSharpParser(BaseParser):
    """Parser for C# source files using regex-based parsing."""
    
    # Regex patterns for C# code elements
    USING_PATTERN = re.compile(r'^\s*using\s+([\w.]+)\s*;', re.MULTILINE)
    NAMESPACE_PATTERN = re.compile(r'^\s*namespace\s+([\w.]+)', re.MULTILINE)
    
    # Class/struct/interface pattern
    CLASS_PATTERN = re.compile(
        r'^\s*(?P<access>public|private|protected|internal|protected\s+internal|private\s+protected)?\s*'
        r'(?P<modifiers>(?:static|abstract|sealed|partial)\s+)*'
        r'(?P<type>class|struct|interface|record)\s+'
        r'(?P<name>\w+)\s*'
        r'(?:<[^>]+>)?\s*'  # Generic type parameters
        r'(?::\s*(?P<inheritance>[^{]+))?'  # Inheritance/interfaces
        r'\s*\{',
        re.MULTILINE
    )
    
    # Method pattern (including constructors)
    METHOD_PATTERN = re.compile(
        r'^\s*(?P<access>public|private|protected|internal|protected\s+internal|private\s+protected)?\s*'
        r'(?P<modifiers>(?:(?:static|virtual|override|abstract|sealed|async|extern|partial|new)\s+)*)'
        r'(?P<return_type>[\w<>\[\],\s\.]+?)?\s+'
        r'(?P<name>\w+)\s*'
        r'(?:<[^>]+>)?\s*'  # Generic type parameters
        r'\((?P<params>[^)]*)\)',
        re.MULTILINE
    )
    
    # Constructor pattern
    CONSTRUCTOR_PATTERN = re.compile(
        r'^\s*(?P<access>public|private|protected|internal)?\s*'
        r'(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*'
        r'(?::\s*(?:base|this)\s*\([^)]*\))?\s*'
        r'\{',
        re.MULTILINE
    )
    
    # Property pattern
    PROPERTY_PATTERN = re.compile(
        r'^\s*(?P<access>public|private|protected|internal|protected\s+internal|private\s+protected)?\s*'
        r'(?P<modifiers>(?:(?:static|virtual|override|abstract|sealed|new)\s+)*)'
        r'(?P<type>[\w<>\[\],\s\.]+)\s+'
        r'(?P<name>\w+)\s*'
        r'(?:\{|=>)',
        re.MULTILINE
    )
    
    @property
    def language_name(self) -> str:
        return "csharp"
    
    @property
    def file_extensions(self) -> Tuple[str, ...]:
        return ('.cs',)
    
    def parse_file(self, file_path: str) -> FileMetrics:
        """Parse a C# file and return its metrics."""
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
        
        # Extract using statements
        using_statements = self.USING_PATTERN.findall(content)
        
        # Extract namespaces
        namespaces = self.NAMESPACE_PATTERN.findall(content)
        
        # Find all classes/structs/interfaces
        classes: List[ClassMetrics] = []
        functions: List[MethodMetrics] = []  # Top-level methods (rare in C#)
        
        try:
            classes = self._find_classes(content, lines)
        except Exception as e:
            return FileMetrics(
                path=file_path,
                language=self.language_name,
                line_count=len(lines),
                class_count=0,
                function_count=0,
                line_stats=calculate_line_stats(lines),
                using_statements=using_statements,
                namespaces=namespaces,
                parse_error=f"Parse error: {str(e)}"
            )
        
        return FileMetrics(
            path=file_path,
            language=self.language_name,
            line_count=len(lines),
            class_count=len(classes),
            function_count=len(functions),
            classes=classes,
            functions=functions,
            line_stats=calculate_line_stats(lines),
            using_statements=using_statements,
            namespaces=namespaces
        )
    
    def _find_classes(self, content: str, lines: List[str]) -> List[ClassMetrics]:
        """Find all classes/structs/interfaces in the content."""
        classes = []
        
        for match in self.CLASS_PATTERN.finditer(content):
            class_name = match.group('name')
            class_type = match.group('type')
            access = match.group('access') or 'internal'  # Default in C#
            modifiers = match.group('modifiers') or ''
            inheritance = match.group('inheritance')
            
            # Calculate line number
            line_start = content[:match.start()].count('\n') + 1
            
            # Find the closing brace to determine class end
            class_start_pos = match.end() - 1  # Position of opening brace
            class_end_pos = self._find_matching_brace(content, class_start_pos)
            
            if class_end_pos == -1:
                # Couldn't find matching brace, estimate
                line_end = line_start + 10
            else:
                line_end = content[:class_end_pos].count('\n') + 1
            
            # Get class content
            class_content = content[match.start():class_end_pos + 1] if class_end_pos != -1 else ""
            class_lines = lines[line_start - 1:line_end]
            
            # Parse inheritance
            base_classes = []
            interfaces = []
            if inheritance:
                parts = [p.strip() for p in inheritance.split(',')]
                for part in parts:
                    # In C#, interfaces typically start with 'I' by convention
                    # But this isn't reliable, so we just collect them all
                    if part.startswith('I') and len(part) > 1 and part[1].isupper():
                        interfaces.append(part)
                    else:
                        base_classes.append(part)
            
            # Find methods within this class
            methods = self._find_methods(class_content, lines, line_start)
            
            # Find constructor params
            constructor_param_count = self._find_constructor_params(class_content, class_name)
            
            # Find properties
            property_count = len(self.PROPERTY_PATTERN.findall(class_content))
            
            # Determine if abstract/static
            is_abstract = 'abstract' in modifiers
            is_static = 'static' in modifiers
            
            classes.append(ClassMetrics(
                name=class_name,
                line_start=line_start,
                line_end=line_end,
                line_count=line_end - line_start + 1,
                constructor_param_count=constructor_param_count,
                method_count=len(methods),
                methods=methods,
                line_stats=calculate_line_stats(class_lines),
                access_modifier=access.replace('  ', ' ').strip(),
                property_count=property_count,
                is_abstract=is_abstract,
                is_static=is_static,
                base_classes=base_classes,
                interfaces=interfaces
            ))
        
        return classes
    
    def _find_methods(self, class_content: str, all_lines: List[str], class_start_line: int) -> List[MethodMetrics]:
        """Find all methods within a class."""
        methods = []
        
        for match in self.METHOD_PATTERN.finditer(class_content):
            method_name = match.group('name')
            return_type = match.group('return_type')
            access = match.group('access') or 'private'  # Default in C#
            modifiers = match.group('modifiers') or ''
            params = match.group('params')
            
            # Skip if this looks like a constructor (no return type and name matches class)
            if not return_type or return_type.strip() == '':
                continue
            
            # Skip common false positives
            if method_name in ('if', 'for', 'foreach', 'while', 'switch', 'catch', 'using', 'lock'):
                continue
            
            # Skip property accessors
            if method_name in ('get', 'set', 'add', 'remove'):
                continue
            
            # Calculate line number relative to class
            relative_line = class_content[:match.start()].count('\n')
            line_start = class_start_line + relative_line
            
            # Find method end (look for closing brace or semicolon for abstract/extern)
            method_start_pos = match.end()
            remaining = class_content[method_start_pos:]
            
            # Look for opening brace or semicolon
            brace_pos = remaining.find('{')
            semi_pos = remaining.find(';')
            
            if semi_pos != -1 and (brace_pos == -1 or semi_pos < brace_pos):
                # Abstract/extern method ending with semicolon
                line_end = line_start
            elif brace_pos != -1:
                # Method with body
                body_start = method_start_pos + brace_pos
                body_end = self._find_matching_brace(class_content, body_start)
                if body_end != -1:
                    line_end = class_start_line + class_content[:body_end].count('\n')
                else:
                    line_end = line_start + 5  # Estimate
            else:
                line_end = line_start
            
            # Count parameters
            arg_count = self._count_parameters(params)
            
            # Get method lines
            method_lines = all_lines[line_start - 1:line_end] if line_end <= len(all_lines) else []
            
            # Check modifiers
            is_async = 'async' in modifiers
            is_static = 'static' in modifiers
            
            methods.append(MethodMetrics(
                name=method_name,
                line_start=line_start,
                line_end=line_end,
                line_count=max(1, line_end - line_start + 1),
                arg_count=arg_count,
                line_stats=calculate_line_stats(method_lines),
                access_modifier=access.replace('  ', ' ').strip(),
                return_type=return_type.strip() if return_type else None,
                is_async=is_async,
                is_static=is_static
            ))
        
        return methods
    
    def _find_constructor_params(self, class_content: str, class_name: str) -> int:
        """Find the constructor parameter count for a class."""
        # Look for constructor pattern matching the class name
        pattern = re.compile(
            rf'^\s*(?:public|private|protected|internal)?\s*{re.escape(class_name)}\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        match = pattern.search(class_content)
        if match:
            params = match.group(1)
            return self._count_parameters(params)
        
        return 0
    
    def _count_parameters(self, params_str: str) -> int:
        """Count the number of parameters in a parameter string."""
        if not params_str or not params_str.strip():
            return 0
        
        # Handle generic types with commas (e.g., Dictionary<string, int>)
        # by temporarily replacing content inside angle brackets
        depth = 0
        cleaned = []
        for char in params_str:
            if char == '<':
                depth += 1
                cleaned.append(char)
            elif char == '>':
                depth -= 1
                cleaned.append(char)
            elif char == ',' and depth > 0:
                cleaned.append('\x00')  # Placeholder
            else:
                cleaned.append(char)
        
        cleaned_str = ''.join(cleaned)
        params = [p.strip() for p in cleaned_str.split(',') if p.strip()]
        
        # Filter out 'this' for extension methods
        params = [p for p in params if not p.startswith('this ')]
        
        return len(params)
    
    def _find_matching_brace(self, content: str, start_pos: int) -> int:
        """Find the position of the closing brace matching the opening brace at start_pos."""
        if start_pos >= len(content) or content[start_pos] != '{':
            return -1
        
        depth = 1
        pos = start_pos + 1
        in_string = False
        in_char = False
        in_comment = False
        in_block_comment = False
        
        while pos < len(content) and depth > 0:
            char = content[pos]
            prev_char = content[pos - 1] if pos > 0 else ''
            next_char = content[pos + 1] if pos < len(content) - 1 else ''
            
            # Handle comments
            if not in_string and not in_char:
                if char == '/' and next_char == '/' and not in_block_comment:
                    in_comment = True
                elif char == '\n' and in_comment:
                    in_comment = False
                elif char == '/' and next_char == '*' and not in_comment:
                    in_block_comment = True
                elif char == '*' and next_char == '/' and in_block_comment:
                    in_block_comment = False
                    pos += 1
            
            # Handle strings and chars
            if not in_comment and not in_block_comment:
                if char == '"' and prev_char != '\\':
                    in_string = not in_string
                elif char == "'" and prev_char != '\\' and not in_string:
                    in_char = not in_char
            
            # Count braces
            if not in_string and not in_char and not in_comment and not in_block_comment:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
            
            pos += 1
        
        return pos - 1 if depth == 0 else -1