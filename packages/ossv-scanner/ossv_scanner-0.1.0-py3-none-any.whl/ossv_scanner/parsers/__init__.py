"""
Package parsers module for OSS Vulnerability Scanner.
"""

import os
import logging
from typing import Optional, Type, List

from ossv_scanner.parsers.parser_base import BaseParser
from ossv_scanner.parsers.python_parser import PythonParser
from ossv_scanner.parsers.javascript_parser import JavaScriptParser
from ossv_scanner.parsers.java_parser import JavaParser

logger = logging.getLogger(__name__)

# Registry of available parsers
PARSERS = [
    PythonParser,
    JavaScriptParser,
    JavaParser,
]


def get_parser_for_project(project_path: str) -> Optional[BaseParser]:
    """
    Determine and return the appropriate parser for the given project.

    Args:
        project_path: Path to the project directory.

    Returns:
        An instance of the appropriate parser, or None if no parser is found.
    """
    logger.debug(f"Finding suitable parser for project at {project_path}")
    
    # Check each parser to see if it can handle this project
    for parser_class in PARSERS:
        if parser_class.can_handle(project_path):
            logger.debug(f"Found suitable parser: {parser_class.__name__}")
            return parser_class(project_path)
    
    logger.warning(f"No suitable parser found for project at {project_path}")
    return None


def get_available_parsers() -> List[str]:
    """
    Get a list of available parser names.

    Returns:
        List of parser class names.
    """
    return [parser.__name__ for parser in PARSERS]
