"""
Parser for JavaScript/Node.js projects.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Set

from ossv_scanner.parsers.parser_base import BaseParser
from ossv_scanner.parsers.dependency import Dependency

logger = logging.getLogger(__name__)


class JavaScriptParser(BaseParser):
    """Parser for JavaScript/Node.js projects (package.json)."""

    @classmethod
    def can_handle(cls, project_path: str) -> bool:
        """
        Check if this parser can handle the given project.

        Args:
            project_path: Path to the project directory.

        Returns:
            True if this parser can handle the project, False otherwise.
        """
        # Check for package.json
        for root, _, files in os.walk(project_path):
            if "package.json" in files:
                return True
        
        return False
    
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse dependencies from the project.

        Returns:
            List of dependency dictionaries with at least name and version keys.
        """
        logger.debug(f"Parsing JavaScript dependencies from {self.project_path}")
        dependencies = []
        
        # Find all package.json files
        package_files = self.find_files("package.json")
        
        for file_path in package_files:
            deps = self.parse_file(file_path)
            dependencies.extend(deps)
        
        # Check for package-lock.json or yarn.lock for transitive dependencies
        lock_files = self.find_files("package-lock.json") + self.find_files("yarn.lock")
        transitive_deps = []
        
        for file_path in lock_files:
            trans_deps = self.parse_lock_file(file_path)
            transitive_deps.extend(trans_deps)
        
        # Combine direct and transitive dependencies
        all_deps = dependencies + transitive_deps
        
        # Remove duplicates while preserving order
        unique_deps = []
        seen = set()
        for dep in all_deps:
            key = (dep.name, dep.version)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        # Convert to dictionary format
        return self.to_dict(unique_deps)
    
    def parse_file(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a package.json file.

        Args:
            file_path: Path to the package.json file.

        Returns:
            List of Dependency objects.
        """
        logger.debug(f"Parsing package.json at {file_path}")
        dependencies = []
        
        if not self._is_valid_file(file_path):
            logger.warning(f"File {file_path} does not exist or is not readable.")
            return dependencies
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Extract dependencies
            dep_types = [
                ("dependencies", True),
                ("devDependencies", True),
                ("peerDependencies", True),
                ("optionalDependencies", True),
            ]
            
            for dep_type, is_direct in dep_types:
                if dep_type in package_data:
                    for name, version in package_data[dep_type].items():
                        # Clean version string (remove semver ranges like ^, ~, etc.)
                        clean_version = self._clean_version(version)
                        
                        dependencies.append(
                            Dependency(
                                name=name,
                                version=clean_version,
                                package_type="npm",
                                is_direct=is_direct,
                                license=self._get_license(package_data)
                            )
                        )
        
        except Exception as e:
            logger.warning(f"Error parsing package.json {file_path}: {str(e)}")
        
        logger.debug(f"Found {len(dependencies)} dependencies in {file_path}")
        return dependencies
    
    def parse_lock_file(self, file_path: str) -> List[Dependency]:
        """
        Parse transitive dependencies from a lock file.

        Args:
            file_path: Path to the lock file.

        Returns:
            List of Dependency objects.
        """
        logger.debug(f"Parsing lock file at {file_path}")
        dependencies = []
        
        if not self._is_valid_file(file_path):
            logger.warning(f"File {file_path} does not exist or is not readable.")
            return dependencies
        
        try:
            if file_path.endswith("package-lock.json"):
                dependencies = self._parse_npm_lock(file_path)
            elif file_path.endswith("yarn.lock"):
                dependencies = self._parse_yarn_lock(file_path)
        
        except Exception as e:
            logger.warning(f"Error parsing lock file {file_path}: {str(e)}")
        
        logger.debug(f"Found {len(dependencies)} transitive dependencies in {file_path}")
        return dependencies
    
    def _parse_npm_lock(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from an npm package-lock.json file.

        Args:
            file_path: Path to the package-lock.json file.

        Returns:
            List of Dependency objects.
        """
        dependencies = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lock_data = json.load(f)
        
        # npm v1 format
        if "dependencies" in lock_data:
            self._extract_npm_deps(lock_data["dependencies"], dependencies)
        
        # npm v2+ format
        if "packages" in lock_data:
            for pkg_path, pkg_data in lock_data["packages"].items():
                if pkg_path and pkg_path != "":  # Skip root package
                    name = pkg_path.split("/")[-1]
                    if "@" in name:
                        # Handle scoped packages like @org/package
                        scope_parts = pkg_path.split("/")
                        if len(scope_parts) >= 2:
                            name = f"{scope_parts[-2]}/{scope_parts[-1]}"
                    
                    version = pkg_data.get("version", "unknown")
                    
                    dependencies.append(
                        Dependency(
                            name=name,
                            version=version,
                            package_type="npm",
                            is_direct=False,
                            license=pkg_data.get("license")
                        )
                    )
        
        return dependencies
    
    def _extract_npm_deps(self, deps_data: Dict[str, Any], dependencies: List[Dependency], parent: Optional[str] = None) -> None:
        """
        Extract dependencies from npm lock data.

        Args:
            deps_data: Dependencies data from lock file.
            dependencies: List to append dependencies to.
            parent: Parent dependency name.
        """
        for name, data in deps_data.items():
            if "version" in data:
                dependencies.append(
                    Dependency(
                        name=name,
                        version=data["version"],
                        package_type="npm",
                        is_direct=parent is None,
                        parent=parent,
                        license=data.get("license")
                    )
                )
            
            # Recursively process dependencies
            if "dependencies" in data:
                self._extract_npm_deps(data["dependencies"], dependencies, name)
    
    def _parse_yarn_lock(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a yarn.lock file.

        Args:
            file_path: Path to the yarn.lock file.

        Returns:
            List of Dependency objects.
        """
        dependencies = []
        
        # Yarn lock is not JSON, but we can do some basic parsing
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by package definitions
        packages = content.split("\n\n")
        
        for package in packages:
            lines = package.strip().split("\n")
            if not lines:
                continue
            
            # Extract package name and version from first line
            name_line = lines[0].strip('"\'')
            if "@" in name_line:
                try:
                    # Format is typically "name@version:"
                    parts = name_line.split("@")
                    if name_line.startswith("@"):
                        # Scoped package like @org/package
                        name = f"@{parts[1]}"
                        version_spec = "@".join(parts[2:])
                    else:
                        name = parts[0]
                        version_spec = "@".join(parts[1:])
                    
                    # Find actual version in the block
                    version = "unknown"
                    for line in lines:
                        if line.strip().startswith("version "):
                            version = line.split("\"")[1]
                            break
                    
                    dependencies.append(
                        Dependency(
                            name=name,
                            version=version,
                            package_type="npm",
                            is_direct=False
                        )
                    )
                except Exception as e:
                    logger.debug(f"Error parsing yarn.lock entry: {str(e)}")
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """
        Clean version string by removing semver operators.

        Args:
            version: Version string.

        Returns:
            Cleaned version string.
        """
        # Handle semver range operators
        for prefix in ["^", "~", ">=", ">", "<=", "<", "="]:
            if version.startswith(prefix):
                version = version[len(prefix):]
        
        # Handle version ranges
        if " - " in version:
            version = version.split(" - ")[1]  # Take the higher version
        
        # Handle complex ranges with ||
        if "||" in version:
            versions = [self._clean_version(v.strip()) for v in version.split("||")]
            version = max(versions)  # Take the highest version
        
        # Handle x-ranges
        if "x" in version or "*" in version:
            version = version.replace("x", "0").replace("*", "0")
        
        # Return "latest" as is
        if version == "latest":
            return "latest"
        
        # Remove any remaining non-version characters
        import re
        version = re.sub(r'[^\d.]', '', version) or "unknown"
        
        return version
    
    def _get_license(self, package_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract license information from package data.

        Args:
            package_data: Package.json data.

        Returns:
            License string or None.
        """
        license_data = package_data.get("license")
        if isinstance(license_data, str):
            return license_data
        
        if isinstance(license_data, dict) and "type" in license_data:
            return license_data["type"]
        
        return None
