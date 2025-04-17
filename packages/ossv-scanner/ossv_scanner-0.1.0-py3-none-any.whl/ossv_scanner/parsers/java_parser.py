"""
Parser for Java/Maven projects.
"""

import os
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Set, Tuple

from ossv_scanner.parsers.parser_base import BaseParser
from ossv_scanner.parsers.dependency import Dependency

logger = logging.getLogger(__name__)


class JavaParser(BaseParser):
    """Parser for Java/Maven projects (pom.xml)."""

    # XML namespaces used in pom.xml
    NAMESPACES = {
        "mvn": "http://maven.apache.org/POM/4.0.0",
    }
    
    @classmethod
    def can_handle(cls, project_path: str) -> bool:
        """
        Check if this parser can handle the given project.

        Args:
            project_path: Path to the project directory.

        Returns:
            True if this parser can handle the project, False otherwise.
        """
        # Check for pom.xml
        for root, _, files in os.walk(project_path):
            if "pom.xml" in files:
                return True
        
        # Check for build.gradle (future extension)
        for root, _, files in os.walk(project_path):
            if "build.gradle" in files:
                return True
        
        return False
    
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse dependencies from the project.

        Returns:
            List of dependency dictionaries with at least name and version keys.
        """
        logger.debug(f"Parsing Java dependencies from {self.project_path}")
        dependencies = []
        
        # Find all pom.xml files
        pom_files = self.find_files("pom.xml")
        
        for file_path in pom_files:
            deps = self.parse_file(file_path)
            dependencies.extend(deps)
        
        # TODO: Add support for build.gradle parsing
        
        # Remove duplicates while preserving order
        unique_deps = []
        seen = set()
        for dep in dependencies:
            key = (dep.name, dep.version)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        # Convert to dictionary format
        return self.to_dict(unique_deps)
    
    def parse_file(self, file_path: str) -> List[Dependency]:
        """
        Parse dependencies from a pom.xml file.

        Args:
            file_path: Path to the pom.xml file.

        Returns:
            List of Dependency objects.
        """
        logger.debug(f"Parsing pom.xml at {file_path}")
        dependencies = []
        
        if not self._is_valid_file(file_path):
            logger.warning(f"File {file_path} does not exist or is not readable.")
            return dependencies
        
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Handle namespace
            if "}" in root.tag:
                namespace = root.tag.split("}")[0] + "}"
                self.NAMESPACES["mvn"] = namespace[1:-1]
            else:
                namespace = ""
            
            # Extract properties for variable substitution
            properties = self._extract_properties(root, namespace)
            
            # Extract parent pom information
            parent_group_id, parent_artifact_id, parent_version = self._extract_parent_info(root, namespace)
            
            # Extract this project's coordinates
            project_group_id = self._find_text(root, f"{namespace}groupId") or parent_group_id
            project_artifact_id = self._find_text(root, f"{namespace}artifactId") or parent_artifact_id
            project_version = self._find_text(root, f"{namespace}version") or parent_version
            
            if None in (project_group_id, project_artifact_id):
                logger.warning(f"Missing group or artifact ID in {file_path}")
            
            # Add this project as a dependency if it has a valid ID
            if project_group_id and project_artifact_id and project_version:
                project_dep = Dependency(
                    name=f"{project_group_id}:{project_artifact_id}",
                    version=project_version,
                    package_type="maven",
                    is_direct=True
                )
                dependencies.append(project_dep)
            
            # Extract dependencies
            deps_element = root.find(f"{namespace}dependencies")
            if deps_element is not None:
                for dep_elem in deps_element.findall(f"{namespace}dependency"):
                    group_id = self._find_text(dep_elem, f"{namespace}groupId")
                    artifact_id = self._find_text(dep_elem, f"{namespace}artifactId")
                    version = self._find_text(dep_elem, f"{namespace}version")
                    
                    # Skip invalid dependencies
                    if not group_id or not artifact_id:
                        continue
                    
                    # Resolve property references in version
                    if version and version.startswith("${") and version.endswith("}"):
                        prop_name = version[2:-1]
                        version = properties.get(prop_name, "unknown")
                    
                    # Skip test dependencies
                    scope = self._find_text(dep_elem, f"{namespace}scope")
                    if scope == "test":
                        continue
                    
                    dependencies.append(
                        Dependency(
                            name=f"{group_id}:{artifact_id}",
                            version=version or "unknown",
                            package_type="maven",
                            is_direct=True
                        )
                    )
        
        except Exception as e:
            logger.warning(f"Error parsing pom.xml {file_path}: {str(e)}")
        
        logger.debug(f"Found {len(dependencies)} dependencies in {file_path}")
        return dependencies
    
    def _extract_properties(self, root: ET.Element, namespace: str) -> Dict[str, str]:
        """
        Extract property values from pom.xml.

        Args:
            root: XML root element.
            namespace: XML namespace.

        Returns:
            Dictionary of property names to values.
        """
        properties = {}
        
        # Handle known built-in properties
        project_group_id = self._find_text(root, f"{namespace}groupId")
        project_artifact_id = self._find_text(root, f"{namespace}artifactId")
        project_version = self._find_text(root, f"{namespace}version")
        
        if project_group_id:
            properties["project.groupId"] = project_group_id
        if project_artifact_id:
            properties["project.artifactId"] = project_artifact_id
        if project_version:
            properties["project.version"] = project_version
        
        # Extract user-defined properties
        props_elem = root.find(f"{namespace}properties")
        if props_elem is not None:
            for prop in props_elem:
                # Strip namespace from tag
                tag = prop.tag
                if "}" in tag:
                    tag = tag.split("}")[1]
                
                properties[tag] = prop.text or ""
        
        return properties
    
    def _extract_parent_info(self, root: ET.Element, namespace: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Extract parent POM information.

        Args:
            root: XML root element.
            namespace: XML namespace.

        Returns:
            Tuple of (group_id, artifact_id, version) for the parent POM.
        """
        parent_elem = root.find(f"{namespace}parent")
        if parent_elem is not None:
            group_id = self._find_text(parent_elem, f"{namespace}groupId")
            artifact_id = self._find_text(parent_elem, f"{namespace}artifactId")
            version = self._find_text(parent_elem, f"{namespace}version")
            return group_id, artifact_id, version
        
        return None, None, None
    
    def _find_text(self, elem: ET.Element, tag: str) -> Optional[str]:
        """
        Find text content of a tag in an element.

        Args:
            elem: XML element.
            tag: Tag name.

        Returns:
            Text content or None if not found.
        """
        child = elem.find(tag)
        if child is not None:
            return child.text
        return None
