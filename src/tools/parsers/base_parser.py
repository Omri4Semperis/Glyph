"""
Base parser abstract class for code analysis.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
from tools.parsers.shared_models import FileMetrics


class BaseParser(ABC):
    """Abstract base class for language-specific code parsers."""
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """Return the language name (e.g., 'python', 'csharp')."""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> Tuple[str, ...]:
        """Return supported file extensions (e.g., ('.py',), ('.cs',))."""
        pass
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file."""
        return file_path.lower().endswith(self.file_extensions)
    
    @abstractmethod
    def parse_file(self, file_path: str) -> FileMetrics:
        """
        Parse a file and return its metrics.
        
        Args:
            file_path: Absolute path to the file to analyze.
            
        Returns:
            FileMetrics object containing the analysis results.
        """
        pass
    
    def read_file(self, file_path: str) -> Tuple[str, List[str]]:
        """
        Read a file and return its content and lines.
        
        Args:
            file_path: Absolute path to the file to read.
            
        Returns:
            Tuple of (full content string, list of lines).
            
        Raises:
            Exception: If the file cannot be read.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        return content, lines