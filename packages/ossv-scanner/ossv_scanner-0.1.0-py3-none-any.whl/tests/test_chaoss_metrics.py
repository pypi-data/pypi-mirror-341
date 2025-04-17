"""
Tests for CHAOSS metrics calculation.
"""

import unittest
from datetime import datetime, timezone, timedelta

from ossv_scanner.utils.chaoss_metrics import CHAOSSMetrics


class TestCHAOSSMetrics(unittest.TestCase):
    """Test cases for CHAOSS metrics calculation."""

    def setUp(self):
        """Set up test fixtures."""
        # Create sample data
        self.dependencies = [
            {
                "name": "requests",
                "version": "2.25.1",
                "package_type": "pypi",
                "is_direct": True,
                "license": "Apache-2.0",
                "purl": "pkg:pypi/requests@2.25.1"
            },
            {
                "name": "flask",
                "version": "2.0.1",
                "package_type": "pypi",
                "is_direct": True,
                "license": "BSD-3-Clause",
                "purl": "pkg:pypi/flask@2.0.1"
            },
            {
                "name": "werkzeug",
                "version": "2.0.0",
                "package_type": "pypi",
                "is_direct": False,
                "license": "BSD-3-Clause",
                "purl": "pkg:pypi/werkzeug@2.0.0"
            },
            {
                "name": "express",
                "version": "4.17.1",
                "package_type": "npm",
                "is_direct": True,
                "license": "MIT",
                "purl": "pkg:npm/express@4.17.1"
            },
            {
                "name": "body-parser",
                "version": "1.19.0",
                "package_type": "npm",
                "is_direct": False,
                "license": None,
                "purl": "pkg:npm/body-parser@1.19.0"
            }
        ]
        
        self.vulnerabilities = {
            "requests@2.25.1": [
                {
                    "cve_id": "CVE-2021-1234",
                    "description": "Test vulnerability",
                    "severity": "HIGH",
                    "cvss_score": 7.5,
                    "published_date": (datetime.now(timezone.utc) - timedelta(days=180)).isoformat()
                }
            ],
            "express@4.17.1": [
                {
                    "cve_id": "CVE-2022-5678",
                    "description": "Test vulnerability 2",
                    "severity": "CRITICAL",
                    "cvss_score": 9.1,
                    "published_date": (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
                },
                {
                    "cve_id": "CVE-2021-8765",
                    "description": "Test vulnerability 3",
                    "severity": "MEDIUM",
                    "cvss_score": 5.4,
                    "published_date": (datetime.now(timezone.utc) - timedelta(days=365)).isoformat()
                }
            ]
        }
        
        self.sbom = {
            "project_name": "test_project",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dependencies_count": len(self.dependencies),
            "cyclonedx_version": "1.4"
        }
        
        # Create CHAOSS metrics calculator
        self.chaoss_metrics = CHAOSSMetrics()
    
    def test_calculate_metrics(self):
        """Test calculating CHAOSS metrics."""
        # Calculate metrics
        metrics = self.chaoss_metrics.calculate_metrics(
            "test_project",
            self.dependencies,
            self.vulnerabilities,
            self.sbom
        )
        
        # Check that metrics were calculated correctly
        self.assertIsNotNone(metrics)
        self.assertIn("risk", metrics)
        self.assertIn("value", metrics)
        self.assertIn("evolution", metrics)
        
        # Check risk metrics
        self.assertEqual(metrics["risk"]["vulnerability_count"], 3)
        self.assertAlmostEqual(metrics["risk"]["vulnerability_density"], 0.6, places=1)
        
        # Check value metrics
        self.assertEqual(metrics["value"]["total_dependencies"], 5)
        self.assertEqual(metrics["value"]["direct_dependencies"], 3)
        self.assertEqual(metrics["value"]["transitive_dependencies"], 2)
        
        # Check evolution metrics
        self.assertIn("vulnerability_discovery_rate", metrics["evolution"])
        if "average_vulnerability_age" in metrics["evolution"]:
            self.assertGreater(metrics["evolution"]["average_vulnerability_age"], 0)
    
    def test_license_metrics(self):
        """Test license metrics calculation."""
        # Calculate metrics
        metrics = self.chaoss_metrics.calculate_metrics(
            "test_project",
            self.dependencies,
            self.vulnerabilities,
            self.sbom
        )
        
        # Check license compliance metrics
        license_risk = metrics["risk"]["license_risk_score"]
        license_compliance = metrics["risk"]["license_compliance"]
        
        self.assertGreaterEqual(license_risk, 0)
        self.assertLessEqual(license_risk, 10)
        
        self.assertEqual(license_compliance["total_dependencies"], 5)
        self.assertEqual(license_compliance["with_license"], 4)
        self.assertEqual(license_compliance["without_license"], 1)
        self.assertAlmostEqual(license_compliance["compliance_rate"], 0.8, places=1)


if __name__ == "__main__":
    unittest.main()
