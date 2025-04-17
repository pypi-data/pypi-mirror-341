"""
SBOM generator implementation - standalone version with no external dependencies.
"""

import os
import uuid
import json
import logging
import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class SBOMGenerator:
    """Generator for Software Bill of Materials (SBOM) in CycloneDX format."""

    def __init__(self, schema_version: str = "1.4"):
        """
        Initialize the SBOM generator.

        Args:
            schema_version: CycloneDX schema version to use.
        """
        self.schema_version = schema_version
    
    def generate(self, dependencies: List[Dict[str, Any]], project_path: str) -> Dict[str, Any]:
        """
        Generate an SBOM from the dependencies.

        Args:
            dependencies: List of dependency dictionaries.
            project_path: Path to the project.

        Returns:
            Dictionary containing SBOM information.
        """
        logger.debug(f"Generating SBOM for project at {project_path}")
        
        try:
            # Create a new BOM
            timestamp = datetime.datetime.utcnow().isoformat()
            project_name = os.path.basename(os.path.abspath(project_path))
            bom_serial = str(uuid.uuid4())
            
            # Generate JSON SBOM
            json_sbom = self._generate_json_sbom(
                dependencies=dependencies,
                project_name=project_name,
                timestamp=timestamp,
                bom_serial=bom_serial
            )
            
            # Generate XML SBOM
            xml_sbom = self._generate_xml_sbom(
                dependencies=dependencies,
                project_name=project_name,
                timestamp=timestamp,
                bom_serial=bom_serial
            )
            
            return {
                "project_name": project_name,
                "generated_at": timestamp,
                "dependencies_count": len(dependencies),
                "json": json_sbom,
                "xml": xml_sbom,
                "cyclonedx_version": self.schema_version
            }
        
        except Exception as e:
            logger.error(f"Error generating SBOM: {str(e)}")
            raise
    
    def _generate_json_sbom(
        self, 
        dependencies: List[Dict[str, Any]], 
        project_name: str,
        timestamp: str,
        bom_serial: str
    ) -> str:
        """
        Generate a JSON SBOM.
        
        Args:
            dependencies: List of dependency dictionaries.
            project_name: Name of the project.
            timestamp: Timestamp string.
            bom_serial: BOM serial number.
            
        Returns:
            JSON SBOM as a string.
        """
        # Create the base SBOM structure
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": self.schema_version,
            "serialNumber": f"urn:uuid:{bom_serial}",
            "version": 1,
            "metadata": {
                "timestamp": timestamp,
                "tools": [
                    {
                        "vendor": "ossv-scanner",
                        "name": "ossv-scanner",
                        "version": "0.1.0"
                    }
                ],
                "component": {
                    "type": "application",
                    "name": project_name,
                    "version": "1.0.0"
                }
            },
            "components": []
        }
        
        # Add dependencies as components
        for dep in dependencies:
            component = {
                "type": "library",
                "name": dep.get("name", "unknown"),
                "version": dep.get("version", "unknown"),
                "purl": dep.get("purl", "")
            }
            
            if "license" in dep and dep["license"]:
                component["licenses"] = [
                    {
                        "license": {
                            "id": dep["license"]
                        }
                    }
                ]
            
            if "description" in dep and dep["description"]:
                component["description"] = dep["description"]
                
            if "homepage" in dep and dep["homepage"]:
                component["externalReferences"] = [
                    {
                        "type": "website",
                        "url": dep["homepage"]
                    }
                ]
                
            sbom["components"].append(component)
        
        # Return pretty-printed JSON
        return json.dumps(sbom, indent=2)
    
    def _generate_xml_sbom(
        self, 
        dependencies: List[Dict[str, Any]], 
        project_name: str,
        timestamp: str,
        bom_serial: str
    ) -> str:
        """
        Generate an XML SBOM.
        
        Args:
            dependencies: List of dependency dictionaries.
            project_name: Name of the project.
            timestamp: Timestamp string.
            bom_serial: BOM serial number.
            
        Returns:
            XML SBOM as a string.
        """
        # Create a simplified XML representation
        # For a full implementation, consider using an XML library
        xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<bom xmlns="http://cyclonedx.org/schema/bom/{self.schema_version}" serialNumber="urn:uuid:{bom_serial}" version="1">',
            '  <metadata>',
            f'    <timestamp>{timestamp}</timestamp>',
            '    <tools>',
            '      <tool>',
            '        <vendor>ossv-scanner</vendor>',
            '        <name>ossv-scanner</name>',
            '        <version>0.1.0</version>',
            '      </tool>',
            '    </tools>',
            '    <component type="application">',
            f'      <name>{project_name}</name>',
            '      <version>1.0.0</version>',
            '    </component>',
            '  </metadata>',
            '  <components>'
        ]
        
        # Add components
        for dep in dependencies:
            xml.append(f'    <component type="library">')
            xml.append(f'      <name>{dep.get("name", "unknown")}</name>')
            xml.append(f'      <version>{dep.get("version", "unknown")}</version>')
            
            if "purl" in dep and dep["purl"]:
                xml.append(f'      <purl>{dep["purl"]}</purl>')
                
            if "license" in dep and dep["license"]:
                xml.append('      <licenses>')
                xml.append('        <license>')
                xml.append(f'          <id>{dep["license"]}</id>')
                xml.append('        </license>')
                xml.append('      </licenses>')
                
            if "description" in dep and dep["description"]:
                xml.append(f'      <description>{dep["description"]}</description>')
                
            if "homepage" in dep and dep["homepage"]:
                xml.append('      <externalReferences>')
                xml.append('        <reference type="website">')
                xml.append(f'          <url>{dep["homepage"]}</url>')
                xml.append('        </reference>')
                xml.append('      </externalReferences>')
                
            xml.append('    </component>')
        
        xml.append('  </components>')
        xml.append('</bom>')
        
        return '\n'.join(xml)