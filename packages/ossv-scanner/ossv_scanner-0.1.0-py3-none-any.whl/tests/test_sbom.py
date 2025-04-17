"""
Tests for SBOM generation.
"""

import os
import json
import unittest
import tempfile
from pathlib import Path

from ossv_scanner.sbom.generator import SBOMGenerator
from ossv_scanner.parsers.dependency import Dependency


class TestSBOMGenerator(unittest.TestCase):
    """Test cases for SBOM generator."""

    def setUp(self):
        """Set up test fixtures."""
        # Create sample dependencies
        self.dependencies = [
            {
                "name": "requests",
                "version": "2.25.1",
                "package_type": "pypi",
                "is_direct": True,
                "purl": "pkg:pypi/requests@2.25.1"
            },
            {
                "name": "flask",
                "version": "2.0.1",
                "package_type": "pypi",
                "is_direct": True,
                "purl": "pkg:pypi/flask@2.0.1"
            },
            {
                "name": "express",
                "version": "4.17.1",
                "package_type": "npm",
                "is_direct": True,
                "purl": "pkg:npm/express@4.17.1"
            }
        ]
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = self.temp_dir.name
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_sbom_generation(self):
        """Test generating an SBOM."""
        # Create SBOM generator
        generator = SBOMGenerator()
        
        # Generate SBOM
        sbom = generator.generate(self.dependencies, self.project_dir)
        
        # Check that the SBOM was generated correctly
        self.assertIsNotNone(sbom)
        self.assertEqual(sbom["dependencies_count"], len(self.dependencies))
        self.assertIn("json", sbom)
        self.assertIn("xml", sbom)
        
        # Check JSON format
        sbom_json = json.loads(sbom["json"])
        self.assertIn("bomFormat", sbom_json)
        self.assertEqual(sbom_json["bomFormat"], "CycloneDX")
        self.assertIn("components", sbom_json)
        self.assertEqual(len(sbom_json["components"]), len(self.dependencies))


if __name__ == "__main__":
    unittest.main()
