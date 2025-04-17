"""
Base parser class for dependency parsing.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set

from ossv_scanner.parsers.dependency import Dependency

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Base class for all dependency parsers."""

    def __init__(self, project_path: str):
        """
        Initialize the parser.

        Args:
            project_path: Path to the project directory.
        """
        self.project_path = project_path
        self.direct_dependencies: List[Dependency] = []
        self.transitive_dependencies: Dict[str, List[Dependency]] = {}
    
    @classmethod
    @abstractmethod
    def can_handle(cls, project_path: str) -> bool:
        """
        Check if this parser can handle the given project.

        Args:
            project_path: Path to the project directory.

        Returns:
            True if this parser can handle the project, False otherwise.
        """
        pass
    
    @abstractmethod
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse dependencies from the project.

        Returns:
            List of dependency dictionaries with at least name and version keys.
        """
        pass
    
    @abstractmethod
    def parse_file(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a specific file.

        Args:
            file_path: Path to the file to parse.

        Returns:
            List of Dependency objects.
        """
        pass
    
    def find_files(self, pattern: str) -> List[str]:
        """
        Find files matching the given pattern in the project.

        Args:
            pattern: File pattern to match.

        Returns:
            List of paths to matching files.
        """
        matches = []
        for root, _, files in os.walk(self.project_path):
            for filename in files:
                if filename == pattern:
                    matches.append(os.path.join(root, filename))
        
        logger.debug(f"Found {len(matches)} files matching pattern '{pattern}'")
        return matches
    
    def resolve_transitive_dependencies(self, dependencies: List[Dependency]) -> Dict[str, List[Dependency]]:
        """
        Resolve transitive dependencies.
        
        This is a placeholder that should be implemented by subclasses.

        Args:
            dependencies: List of direct dependencies.

        Returns:
            Dictionary mapping direct dependency names to lists of transitive dependencies.
        """
        # Default implementation returns empty transitive dependencies
        return {dep.name: [] for dep in dependencies}
    
    def to_dict(self, dependencies: List[Dependency]) -> List[Dict[str, Any]]:
        """
        Convert Dependency objects to dictionaries.

        Args:
            dependencies: List of Dependency objects.

        Returns:
            List of dependency dictionaries.
        """
        return [dep.to_dict() for dep in dependencies]
    
    def _is_valid_file(self, file_path: str) -> bool:
        """
        Check if a file exists and is readable.

        Args:
            file_path: Path to the file.

        Returns:
            True if the file exists and is readable, False otherwise.
        """
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
