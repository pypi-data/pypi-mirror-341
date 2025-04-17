"""
Tests for dependency parsers.
"""

import os
import unittest
import tempfile
from pathlib import Path

from ossv_scanner.parsers import get_parser_for_project
from ossv_scanner.parsers.python_parser import PythonParser
from ossv_scanner.parsers.javascript_parser import JavaScriptParser
from ossv_scanner.parsers.java_parser import JavaParser


class TestParsers(unittest.TestCase):
    """Test cases for dependency parsers."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = self.temp_dir.name
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_python_parser_detection(self):
        """Test that the Python parser is detected for Python projects."""
        # Create a requirements.txt file
        with open(os.path.join(self.project_dir, "requirements.txt"), "w") as f:
            f.write("requests==2.25.1\nflask==2.0.1\n")
        
        # Get parser for the project
        parser = get_parser_for_project(self.project_dir)
        
        # Check that the correct parser was returned
        self.assertIsInstance(parser, PythonParser)
    
    def test_javascript_parser_detection(self):
        """Test that the JavaScript parser is detected for Node.js projects."""
        # Create a package.json file
        with open(os.path.join(self.project_dir, "package.json"), "w") as f:
            f.write('{"name": "test-project", "dependencies": {"express": "^4.17.1"}}')
        
        # Get parser for the project
        parser = get_parser_for_project(self.project_dir)
        
        # Check that the correct parser was returned
        self.assertIsInstance(parser, JavaScriptParser)
    
    def test_java_parser_detection(self):
        """Test that the Java parser is detected for Java/Maven projects."""
        # Create a pom.xml file
        with open(os.path.join(self.project_dir, "pom.xml"), "w") as f:
            f.write('<project><groupId>com.example</groupId><artifactId>test</artifactId></project>')
        
        # Get parser for the project
        parser = get_parser_for_project(self.project_dir)
        
        # Check that the correct parser was returned
        self.assertIsInstance(parser, JavaParser)
    
    def test_python_parser_parsing(self):
        """Test parsing Python dependencies."""
        # Create a requirements.txt file with some dependencies
        with open(os.path.join(self.project_dir, "requirements.txt"), "w") as f:
            f.write("requests==2.25.1\nflask==2.0.1\npandas>=1.3.0\n")
        
        # Create a parser
        parser = PythonParser(self.project_dir)
        
        # Parse dependencies
        dependencies = parser.parse()
        
        # Check that the dependencies were parsed correctly
        self.assertEqual(len(dependencies), 3)
        self.assertTrue(any(dep["name"] == "requests" and dep["version"] == "2.25.1" for dep in dependencies))
        self.assertTrue(any(dep["name"] == "flask" and dep["version"] == "2.0.1" for dep in dependencies))
        self.assertTrue(any(dep["name"] == "pandas" for dep in dependencies))


if __name__ == "__main__":
    unittest.main()
