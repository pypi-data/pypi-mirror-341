"""
Parser for Python projects.
"""

import os
import re
import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set, Optional, Tuple

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from ossv_scanner.parsers.parser_base import BaseParser
from ossv_scanner.parsers.dependency import Dependency

logger = logging.getLogger(__name__)


class PythonParser(BaseParser):
    """Parser for Python projects (requirements.txt, setup.py)."""

    REQUIREMENTS_PATTERNS = ["requirements.txt", "requirements-*.txt", "dev-requirements.txt"]
    SETUP_PATTERN = "setup.py"
    
    @classmethod
    def can_handle(cls, project_path: str) -> bool:
        """
        Check if this parser can handle the given project.

        Args:
            project_path: Path to the project directory.

        Returns:
            True if this parser can handle the project, False otherwise.
        """
        # Check for requirements.txt or setup.py
        for pattern in cls.REQUIREMENTS_PATTERNS:
            if cls._find_file(project_path, pattern):
                return True
        
        if cls._find_file(project_path, cls.SETUP_PATTERN):
            return True
        
        return False
    
    @classmethod
    def _find_file(cls, project_path: str, pattern: str) -> bool:
        """
        Find a file matching the given pattern in the project.

        Args:
            project_path: Path to the project directory.
            pattern: File pattern to match.

        Returns:
            True if a matching file is found, False otherwise.
        """
        for root, _, files in os.walk(project_path):
            for filename in files:
                if re.match(pattern, filename):
                    return True
        return False
    
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse dependencies from the project.

        Returns:
            List of dependency dictionaries with at least name and version keys.
        """
        dependencies = []
        
        # Parse requirements.txt files
        for pattern in self.REQUIREMENTS_PATTERNS:
            for file_path in self.find_files_with_pattern(pattern):
                deps = self.parse_file(file_path)
                dependencies.extend(deps)
        
        # Parse setup.py
        setup_files = self.find_files(self.SETUP_PATTERN)
        for file_path in setup_files:
            deps = self.parse_setup_py(file_path)
            dependencies.extend(deps)
        
        # Remove duplicates while preserving order
        unique_deps = []
        seen = set()
        for dep in dependencies:
            key = (dep.name, dep.version)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        # Resolve transitive dependencies (if possible)
        self.direct_dependencies = unique_deps
        self.transitive_dependencies = self.resolve_transitive_dependencies(unique_deps)
        
        # Convert to dictionary format
        result = self.to_dict(unique_deps)
        
        # Add transitive dependencies to result
        for dep_name, trans_deps in self.transitive_dependencies.items():
            for trans_dep in trans_deps:
                trans_dict = trans_dep.to_dict()
                if trans_dict not in result:  # Avoid duplicates
                    result.append(trans_dict)
        
        return result
    
    def parse_file(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a requirements.txt file.

        Args:
            file_path: Path to the requirements.txt file.

        Returns:
            List of Dependency objects.
        """
        logger.debug(f"Parsing Python dependencies from {file_path}")
        dependencies = []
        
        if not self._is_valid_file(file_path):
            logger.warning(f"File {file_path} does not exist or is not readable.")
            return dependencies
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Handle editable installs
                if line.startswith('-e'):
                    line = line[2:].strip()
                
                # Skip options lines
                if line.startswith('-'):
                    continue
                
                # Handle line continuations
                if line.endswith('\\'):
                    line = line[:-1].strip()
                
                # Handle multiple requirements on one line
                for req in line.split():
                    try:
                        # Parse the requirement
                        req_str = req.strip()
                        if req_str and not req_str.startswith('#'):
                            name, version = self._parse_requirement(req_str)
                            if name:
                                dependencies.append(
                                    Dependency(
                                        name=name,
                                        version=version or "unknown",
                                        package_type="pypi",
                                        is_direct=True,
                                    )
                                )
                    except Exception as e:
                        logger.warning(f"Error parsing requirement '{req}': {str(e)}")
        
        logger.debug(f"Found {len(dependencies)} dependencies in {file_path}")
        return dependencies
    
    def parse_setup_py(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a setup.py file.

        Args:
            file_path: Path to the setup.py file.

        Returns:
            List of Dependency objects.
        """
        logger.debug(f"Parsing Python dependencies from {file_path}")
        dependencies = []
        
        if not self._is_valid_file(file_path):
            logger.warning(f"File {file_path} does not exist or is not readable.")
            return dependencies
        
        try:
            # Run a Python script to extract install_requires
            script = (
                "import ast, sys, json; "
                "setup_args = {}; "
                "with open(sys.argv[1], 'r') as f: "
                "    tree = ast.parse(f.read()); "
                "    for node in ast.walk(tree): "
                "        if isinstance(node, ast.Call) and getattr(node, 'func', None) and getattr(node.func, 'id', None) == 'setup': "
                "            for kw in node.keywords: "
                "                if kw.arg == 'install_requires': "
                "                    if isinstance(kw.value, ast.List): "
                "                        setup_args['install_requires'] = [elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)]; "
                "print(json.dumps(setup_args))"
            )
            
            result = subprocess.run(
                ["python", "-c", script, file_path],
                capture_output=True,
                text=True,
                check=True,
            )
            
            setup_args = {}
            try:
                import json
                setup_args = json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON output from setup.py: {result.stdout}")
            
            install_requires = setup_args.get("install_requires", [])
            
            for req_str in install_requires:
                try:
                    name, version = self._parse_requirement(req_str)
                    if name:
                        dependencies.append(
                            Dependency(
                                name=name,
                                version=version or "unknown",
                                package_type="pypi",
                                is_direct=True,
                            )
                        )
                except Exception as e:
                    logger.warning(f"Error parsing requirement '{req_str}': {str(e)}")
        
        except Exception as e:
            logger.warning(f"Error parsing setup.py {file_path}: {str(e)}")
        
        logger.debug(f"Found {len(dependencies)} dependencies in {file_path}")
        return dependencies
    
    def _parse_requirement(self, req_str: str) -> Tuple[str, Optional[str]]:
        """
        Parse a requirement string to extract name and version.

        Args:
            req_str: Requirement string.

        Returns:
            Tuple of (name, version) where version might be None.
        """
        # Handle URLs or file paths
        if "://" in req_str or req_str.startswith(".") or req_str.startswith("/"):
            # Extract name from URL or path
            parts = req_str.split("#egg=")
            if len(parts) > 1:
                egg_part = parts[1].split("&")[0]
                return egg_part, None
            else:
                # Can't reliably extract name from URL without egg fragment
                return os.path.basename(req_str), None
        
        try:
            req = Requirement(req_str)
            name = req.name
            
            # Extract version from specifiers
            version = None
            if req.specifier:
                # Try to get the most specific version constraint
                for spec in req.specifier:
                    if spec.operator in ("==", "==="):
                        version = str(spec.version)
                        break
                
                # If no exact version, use the minimum version
                if not version:
                    min_versions = [
                        str(spec.version) 
                        for spec in req.specifier 
                        if spec.operator in (">=", ">")
                    ]
                    if min_versions:
                        version = min(min_versions, key=Version)
            
            return name, version
        
        except Exception as e:
            # Fallback parsing for invalid requirements
            logger.debug(f"Error parsing '{req_str}' with packaging.requirements: {str(e)}")
            
            # Basic parsing fallback
            parts = req_str.split("==")
            if len(parts) > 1:
                return parts[0].strip(), parts[1].strip()
            
            parts = req_str.split(">=")
            if len(parts) > 1:
                return parts[0].strip(), parts[1].strip()
            
            # Just return the name without version
            return req_str.split()[0].strip(), None
    
    def resolve_transitive_dependencies(self, dependencies: List[Dependency]) -> Dict[str, List[Dependency]]:
        """
        Resolve transitive dependencies for Python packages.
        
        This is a simplified implementation that tries to use pip to resolve dependencies.

        Args:
            dependencies: List of direct dependencies.

        Returns:
            Dictionary mapping direct dependency names to lists of transitive dependencies.
        """
        result = {dep.name: [] for dep in dependencies}
        
        # This would ideally use pip's resolution engine, but that's complex
        # In a real implementation, you could use something like pip-api or pip-tools
        
        return result
    
    def find_files_with_pattern(self, pattern: str) -> List[str]:
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
                if re.match(pattern, filename):
                    matches.append(os.path.join(root, filename))
        
        logger.debug(f"Found {len(matches)} files matching pattern '{pattern}'")
        return matches
