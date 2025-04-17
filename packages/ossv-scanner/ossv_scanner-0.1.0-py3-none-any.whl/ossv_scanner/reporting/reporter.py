"""
Reporter implementation for OSS Vulnerability Scanner.
"""

import os
import json
import logging
import datetime
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import jinja2, but provide a fallback implementation
try:
    import jinja2
    HAS_JINJA2 = True
except ImportError:
    logger.warning("jinja2 not found, using simplified template rendering")
    HAS_JINJA2 = False


class Reporter:
    """Reporter for generating vulnerability reports."""

    # Templates directory
    TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the reporter.

        Args:
            templates_dir: Directory containing Jinja2 templates. If None, use default.
        """
        self.templates_dir = templates_dir or self.TEMPLATES_DIR
        
        # Create templates directory if it doesn't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Set up Jinja2 environment if available
        if HAS_JINJA2:
            self.jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.templates_dir),
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )
        else:
            self.jinja_env = None
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def generate(
        self, results: Dict[str, Any], output_format: str, output_path: str
    ) -> str:
        """
        Generate a report from scan results.

        Args:
            results: Scan results.
            output_format: Report format (html, json, text).
            output_path: Path to write the report to.

        Returns:
            Path to the generated report.
        """
        logger.debug(f"Generating {output_format} report at {output_path}")
        
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Generate report based on format
            if output_format.lower() == "html":
                self._generate_html_report(results, output_path)
            elif output_format.lower() == "json":
                self._generate_json_report(results, output_path)
            elif output_format.lower() == "text":
                self._generate_text_report(results, output_path)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            logger.debug(f"Report generated successfully at {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _generate_html_report(self, results: Dict[str, Any], output_path: str) -> None:
        """
        Generate an HTML report.

        Args:
            results: Scan results.
            output_path: Path to write the report to.
        """
        try:
            # Prepare data for template
            template_data = self._prepare_template_data(results)
            
            # Use Jinja2 if available, otherwise fallback to simple template
            if HAS_JINJA2:
                try:
                    # Load template
                    template = self.jinja_env.get_template("html_report.html.j2")
                    
                    # Render template
                    html_content = template.render(**template_data)
                    
                    # Write to file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                
                except jinja2.exceptions.TemplateNotFound:
                    logger.error("HTML template not found. Creating a basic template.")
                    self._create_html_template()
                    self._generate_html_report(results, output_path)
            else:
                # Simple fallback template rendering without Jinja2
                html_content = self._generate_simple_html_report(template_data)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
        
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            raise
    
    def _generate_json_report(self, results: Dict[str, Any], output_path: str) -> None:
        """
        Generate a JSON report.

        Args:
            results: Scan results.
            output_path: Path to write the report to.
        """
        try:
            # Prepare data for export
            export_data = {
                "report_type": "ossv-scanner-report",
                "generated_at": datetime.datetime.utcnow().isoformat(),
                "project_path": results.get("project_path"),
                "dependencies": results.get("dependencies", []),
                "vulnerabilities": results.get("vulnerabilities", {}),
                "metrics": results.get("metrics", {}),
                "sbom": results.get("sbom", {}),
                "chaoss_metrics": results.get("chaoss_metrics", {})
            }
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
        
        except Exception as e:
            logger.error(f"Error generating JSON report: {str(e)}")
            raise
    
    def _generate_text_report(self, results: Dict[str, Any], output_path: str) -> None:
        """
        Generate a text report.

        Args:
            results: Scan results.
            output_path: Path to write the report to.
        """
        try:
            # Prepare data for template
            template_data = self._prepare_template_data(results)
            
            # Use Jinja2 if available, otherwise fallback to simple template
            if HAS_JINJA2:
                try:
                    # Load template
                    template = self.jinja_env.get_template("text_report.txt.j2")
                    
                    # Render template
                    text_content = template.render(**template_data)
                    
                    # Write to file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(text_content)
                
                except jinja2.exceptions.TemplateNotFound:
                    logger.error("Text template not found. Creating a basic template.")
                    self._create_text_template()
                    self._generate_text_report(results, output_path)
            else:
                # Simple fallback template rendering without Jinja2
                text_content = self._generate_simple_text_report(template_data)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
        
        except Exception as e:
            logger.error(f"Error generating text report: {str(e)}")
            raise
    
    def _prepare_template_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for templates.

        Args:
            results: Scan results.

        Returns:
            Dictionary of template data.
        """
        # Get vulnerability statistics
        vuln_stats = self._calculate_vulnerability_stats(results.get("vulnerabilities", {}))
        
        # Get the dependency with the most vulnerabilities
        most_vulnerable_dep = None
        max_vulns = 0
        for dep_id, vulns in results.get("vulnerabilities", {}).items():
            if len(vulns) > max_vulns:
                max_vulns = len(vulns)
                most_vulnerable_dep = dep_id
        
        # Create template data
        template_data = {
            "report_title": "OSS Vulnerability Scan Report",
            "generated_at": datetime.datetime.utcnow().isoformat(),
            "project_path": results.get("project_path", ""),
            "project_name": os.path.basename(results.get("project_path", "")),
            "dependencies": results.get("dependencies", []),
            "vulnerabilities": results.get("vulnerabilities", {}),
            "metrics": results.get("metrics", {}),
            "vuln_stats": vuln_stats,
            "most_vulnerable_dep": most_vulnerable_dep,
            "sbom": results.get("sbom", {}),
            "chaoss_metrics": results.get("chaoss_metrics", None),
        }
        
        return template_data
    
    def _calculate_vulnerability_stats(self, vulnerabilities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Calculate vulnerability statistics.

        Args:
            vulnerabilities: Vulnerability data.

        Returns:
            Dictionary of vulnerability statistics.
        """
        stats = {
            "total_vulns": 0,
            "severity_counts": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "unknown": 0,
            },
            "affected_deps": 0,
            "cve_years": {},
        }
        
        # Count vulnerabilities by severity
        for dep_id, vulns in vulnerabilities.items():
            stats["total_vulns"] += len(vulns)
            
            if len(vulns) > 0:
                stats["affected_deps"] += 1
            
            for vuln in vulns:
                severity = vuln.get("severity", "UNKNOWN").lower()
                stats["severity_counts"][severity] = stats["severity_counts"].get(severity, 0) + 1
                
                # Count CVEs by year
                cve_id = vuln.get("cve_id", "")
                if cve_id.startswith("CVE-"):
                    try:
                        year = cve_id.split("-")[1]
                        stats["cve_years"][year] = stats["cve_years"].get(year, 0) + 1
                    except (IndexError, ValueError):
                        pass
        
        return stats
    
    def _create_default_templates(self) -> None:
        """Create default templates if they don't exist."""
        self._create_html_template()
        self._create_text_template()
    
    def _create_html_template(self) -> None:
        """Create the default HTML template."""
        template_path = os.path.join(self.templates_dir, "html_report.html.j2")
        
        if not os.path.exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4 {
            color: #2c3e50;
        }
        .container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .summary {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .severity-critical {
            color: #721c24;
            background-color: #f8d7da;
            padding: 3px 5px;
            border-radius: 3px;
        }
        .severity-high {
            color: #856404;
            background-color: #fff3cd;
            padding: 3px 5px;
            border-radius: 3px;
        }
        .severity-medium {
            color: #0c5460;
            background-color: #d1ecf1;
            padding: 3px 5px;
            border-radius: 3px;
        }
        .severity-low {
            color: #155724;
            background-color: #d4edda;
            padding: 3px 5px;
            border-radius: 3px;
        }
        .severity-unknown {
            color: #383d41;
            background-color: #e2e3e5;
            padding: 3px 5px;
            border-radius: 3px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .chart-container {
            margin-bottom: 30px;
            min-height: 400px;
        }
        .no-vulns {
            color: #155724;
            background-color: #d4edda;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>{{ report_title }}</h1>
    <div class="container">
        <h2>Summary</h2>
        <div class="summary">
            <p><strong>Project:</strong> {{ project_name }}</p>
            <p><strong>Path:</strong> {{ project_path }}</p>
            <p><strong>Report Generated:</strong> {{ generated_at }}</p>
            <p><strong>Dependencies Scanned:</strong> {{ dependencies|length }}</p>
            <p><strong>Vulnerabilities Found:</strong> {{ vuln_stats.total_vulns }}</p>
            <p><strong>Affected Dependencies:</strong> {{ vuln_stats.affected_deps }}</p>
        </div>
    </div>

    <div class="container">
        <h2>Vulnerability Overview</h2>
        {% if vuln_stats.total_vulns > 0 %}
            <div class="chart-container">
                <div id="severity_chart_placeholder"></div>
            </div>
            <div class="chart-container">
                <div id="top_deps_chart_placeholder"></div>
            </div>
            {% if vuln_stats.cve_years %}
            <div class="chart-container">
                <div id="cve_age_chart_placeholder"></div>
            </div>
            {% endif %}
        {% else %}
            <div class="no-vulns">No vulnerabilities found. Great job!</div>
        {% endif %}
    </div>

    {% if vulnerabilities %}
    <div class="container">
        <h2>Vulnerability Details</h2>
        <div id="vuln_details_table_placeholder"></div>
        
        <h3>Vulnerabilities by Dependency</h3>
        {% for dep_id, vulns in vulnerabilities.items() %}
            <h4>{{ dep_id }} ({{ vulns|length }} vulnerabilities)</h4>
            <table>
                <thead>
                    <tr>
                        <th>CVE ID</th>
                        <th>Severity</th>
                        <th>CVSS Score</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {% for vuln in vulns %}
                    <tr>
                        <td><a href="https://nvd.nist.gov/vuln/detail/{{ vuln.cve_id }}" target="_blank">{{ vuln.cve_id }}</a></td>
                        <td><span class="severity-{{ vuln.severity|lower }}">{{ vuln.severity }}</span></td>
                        <td>{{ vuln.cvss_score }}</td>
                        <td>{{ vuln.description|truncate(150) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endfor %}
    </div>
    {% endif %}

    <div class="container">
        <h2>Scan Metrics</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {% for key, value in metrics.items() %}
                <tr>
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="container">
        <h2>Software Bill of Materials (SBOM)</h2>
        <p>SBOM format: CycloneDX {{ sbom.cyclonedx_version }}</p>
        <p>Dependencies count: {{ sbom.dependencies_count }}</p>
        <p>Generated at: {{ sbom.generated_at }}</p>
    </div>

    {% if chaoss_metrics %}
    <div class="container">
        <h2>CHAOSS Metrics</h2>
        
        <h3>Risk Metrics</h3>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Vulnerability Count</td>
                    <td>{{ chaoss_metrics.risk.vulnerability_count }}</td>
                </tr>
                <tr>
                    <td>Vulnerability Density</td>
                    <td>{{ "%.2f"|format(chaoss_metrics.risk.vulnerability_density) }}</td>
                </tr>
                <tr>
                    <td>Critical Vulnerability Density</td>
                    <td>{{ "%.2f"|format(chaoss_metrics.risk.critical_vulnerability_density) }}</td>
                </tr>
                <tr>
                    <td>License Risk Score</td>
                    <td>{{ "%.2f"|format(chaoss_metrics.risk.license_risk_score) }}</td>
                </tr>
                <tr>
                    <td>Security Score</td>
                    <td>{{ "%.2f"|format(chaoss_metrics.risk.odc_security_score) }} / 10</td>
                </tr>
            </tbody>
        </table>
        
        <h3>Value Metrics</h3>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Total Dependencies</td>
                    <td>{{ chaoss_metrics.value.total_dependencies }}</td>
                </tr>
                <tr>
                    <td>Direct Dependencies</td>
                    <td>{{ chaoss_metrics.value.direct_dependencies }}</td>
                </tr>
                <tr>
                    <td>Transitive Dependencies</td>
                    <td>{{ chaoss_metrics.value.transitive_dependencies }}</td>
                </tr>
                <tr>
                    <td>Dependency Depth</td>
                    <td>{{ chaoss_metrics.value.dependency_depth }}</td>
                </tr>
            </tbody>
        </table>
        
        <h3>Evolution Metrics</h3>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Vulnerability Discovery Rate</td>
                    <td>{{ "%.2f"|format(chaoss_metrics.evolution.vulnerability_discovery_rate) }} per year</td>
                </tr>
                {% if chaoss_metrics.evolution.average_vulnerability_age %}
                <tr>
                    <td>Average Vulnerability Age</td>
                    <td>{{ chaoss_metrics.evolution.average_vulnerability_age }} days</td>
                </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
    {% endif %}

    <footer>
        <p>Generated with OSS Vulnerability Scanner</p>
    </footer>
</body>
</html>
""")
            logger.debug(f"Created HTML template at {template_path}")
    
    def _create_text_template(self) -> None:
        """Create the default text template."""
        template_path = os.path.join(self.templates_dir, "text_report.txt.j2")
        
        if not os.path.exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write("""{{ report_title }}
{{ "=" * report_title|length }}

Summary
-------
Project: {{ project_name }}
Path: {{ project_path }}
Report Generated: {{ generated_at }}
Dependencies Scanned: {{ dependencies|length }}
Vulnerabilities Found: {{ vuln_stats.total_vulns }}
Affected Dependencies: {{ vuln_stats.affected_deps }}

Vulnerability Summary
--------------------
Critical: {{ vuln_stats.severity_counts.critical }}
High: {{ vuln_stats.severity_counts.high }}
Medium: {{ vuln_stats.severity_counts.medium }}
Low: {{ vuln_stats.severity_counts.low }}
Unknown: {{ vuln_stats.severity_counts.unknown }}

{% if vulnerabilities %}
Vulnerabilities by Dependency
----------------------------
{% for dep_id, vulns in vulnerabilities.items() %}
{{ dep_id }} ({{ vulns|length }} vulnerabilities)
{{ "-" * (dep_id|length + 3 + vulns|length|string|length + 15) }}
{% for vuln in vulns %}
* {{ vuln.cve_id }} - {{ vuln.severity }} (CVSS: {{ vuln.cvss_score }})
  {{ vuln.description|truncate(100) }}
{% endfor %}

{% endfor %}
{% else %}
No vulnerabilities found. Great job!
{% endif %}

Scan Metrics
-----------
{% for key, value in metrics.items() %}
{{ key }}: {{ value }}
{% endfor %}

Software Bill of Materials (SBOM)
--------------------------------
SBOM format: CycloneDX {{ sbom.cyclonedx_version }}
Dependencies count: {{ sbom.dependencies_count }}
Generated at: {{ sbom.generated_at }}

{% if chaoss_metrics %}
CHAOSS Metrics
-------------
Risk Metrics:
- Vulnerability Count: {{ chaoss_metrics.risk.vulnerability_count }}
- Vulnerability Density: {{ "%.2f"|format(chaoss_metrics.risk.vulnerability_density) }}
- Critical Vulnerability Density: {{ "%.2f"|format(chaoss_metrics.risk.critical_vulnerability_density) }}
- License Risk Score: {{ "%.2f"|format(chaoss_metrics.risk.license_risk_score) }}
- Security Score: {{ "%.2f"|format(chaoss_metrics.risk.odc_security_score) }} / 10

Value Metrics:
- Total Dependencies: {{ chaoss_metrics.value.total_dependencies }}
- Direct Dependencies: {{ chaoss_metrics.value.direct_dependencies }}
- Transitive Dependencies: {{ chaoss_metrics.value.transitive_dependencies }}
- Dependency Depth: {{ chaoss_metrics.value.dependency_depth }}

Evolution Metrics:
- Vulnerability Discovery Rate: {{ "%.2f"|format(chaoss_metrics.evolution.vulnerability_discovery_rate) }} per year
{% if chaoss_metrics.evolution.average_vulnerability_age %}
- Average Vulnerability Age: {{ chaoss_metrics.evolution.average_vulnerability_age }} days
{% endif %}
{% endif %}

Generated with OSS Vulnerability Scanner
""")
            logger.debug(f"Created text template at {template_path}")
    
    def _generate_simple_html_report(self, template_data: Dict[str, Any]) -> str:
        """
        Generate a simple HTML report without Jinja2.
        
        Args:
            template_data: Template data.
            
        Returns:
            HTML content.
        """
        # This is a simplified version of the HTML template
        # It doesn't support looping and complex conditions, but provides basic functionality
        
        project_name = template_data.get("project_name", "Unknown")
        project_path = template_data.get("project_path", "")
        generated_at = template_data.get("generated_at", "")
        total_deps = len(template_data.get("dependencies", []))
        vuln_stats = template_data.get("vuln_stats", {})
        total_vulns = vuln_stats.get("total_vulns", 0)
        affected_deps = vuln_stats.get("affected_deps", 0)
        
        # Create vulnerabilities table rows
        vuln_rows = []
        for dep_id, vulns in template_data.get("vulnerabilities", {}).items():
            for vuln in vulns:
                cve_id = vuln.get("cve_id", "N/A")
                severity = vuln.get("severity", "UNKNOWN")
                cvss_score = vuln.get("cvss_score", "N/A")
                description = vuln.get("description", "")
                if len(description) > 150:
                    description = description[:147] + "..."
                
                severity_class = f"severity-{severity.lower()}"
                
                vuln_rows.append(f"""
                <tr>
                    <td>{dep_id}</td>
                    <td><a href="https://nvd.nist.gov/vuln/detail/{cve_id}" target="_blank">{cve_id}</a></td>
                    <td><span class="{severity_class}">{severity}</span></td>
                    <td>{cvss_score}</td>
                    <td>{description}</td>
                </tr>
                """)
        
        # Generate CHAOSS metrics section if available
        chaoss_section = ""
        if template_data.get("chaoss_metrics"):
            chaoss = template_data["chaoss_metrics"]
            risk = chaoss.get("risk", {})
            value = chaoss.get("value", {})
            evolution = chaoss.get("evolution", {})
            
            # Format float values
            vuln_density = f"{risk.get('vulnerability_density', 0):.2f}"
            critical_density = f"{risk.get('critical_vulnerability_density', 0):.2f}"
            license_risk = f"{risk.get('license_risk_score', 0):.2f}"
            security_score = f"{risk.get('odc_security_score', 0):.2f}"
            vuln_discovery_rate = f"{evolution.get('vulnerability_discovery_rate', 0):.2f}"
            
            chaoss_section = f"""
            <div class="container">
                <h2>CHAOSS Metrics</h2>
                
                <h3>Risk Metrics</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Vulnerability Count</td>
                            <td>{risk.get('vulnerability_count', 0)}</td>
                        </tr>
                        <tr>
                            <td>Vulnerability Density</td>
                            <td>{vuln_density}</td>
                        </tr>
                        <tr>
                            <td>Critical Vulnerability Density</td>
                            <td>{critical_density}</td>
                        </tr>
                        <tr>
                            <td>License Risk Score</td>
                            <td>{license_risk}</td>
                        </tr>
                        <tr>
                            <td>Security Score</td>
                            <td>{security_score} / 10</td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>Value Metrics</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total Dependencies</td>
                            <td>{value.get('total_dependencies', 0)}</td>
                        </tr>
                        <tr>
                            <td>Direct Dependencies</td>
                            <td>{value.get('direct_dependencies', 0)}</td>
                        </tr>
                        <tr>
                            <td>Transitive Dependencies</td>
                            <td>{value.get('transitive_dependencies', 0)}</td>
                        </tr>
                        <tr>
                            <td>Dependency Depth</td>
                            <td>{value.get('dependency_depth', 0)}</td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>Evolution Metrics</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Vulnerability Discovery Rate</td>
                            <td>{vuln_discovery_rate} per year</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSS Vulnerability Scan Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
        }}
        .container {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .severity-critical {{
            color: #721c24;
            background-color: #f8d7da;
            padding: 3px 5px;
            border-radius: 3px;
        }}
        .severity-high {{
            color: #856404;
            background-color: #fff3cd;
            padding: 3px 5px;
            border-radius: 3px;
        }}
        .severity-medium {{
            color: #0c5460;
            background-color: #d1ecf1;
            padding: 3px 5px;
            border-radius: 3px;
        }}
        .severity-low {{
            color: #155724;
            background-color: #d4edda;
            padding: 3px 5px;
            border-radius: 3px;
        }}
        .severity-unknown {{
            color: #383d41;
            background-color: #e2e3e5;
            padding: 3px 5px;
            border-radius: 3px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .chart-container {{
            margin-bottom: 30px;
            min-height: 400px;
        }}
        .no-vulns {{
            color: #155724;
            background-color: #d4edda;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>OSS Vulnerability Scan Report</h1>
    <div class="container">
        <h2>Summary</h2>
        <div class="summary">
            <p><strong>Project:</strong> {project_name}</p>
            <p><strong>Path:</strong> {project_path}</p>
            <p><strong>Report Generated:</strong> {generated_at}</p>
            <p><strong>Dependencies Scanned:</strong> {total_deps}</p>
            <p><strong>Vulnerabilities Found:</strong> {total_vulns}</p>
            <p><strong>Affected Dependencies:</strong> {affected_deps}</p>
        </div>
    </div>

    <div class="container">
        <h2>Vulnerability Overview</h2>
        {"<div class='no-vulns'>No vulnerabilities found. Great job!</div>" if total_vulns == 0 else 
         "<div id='severity_chart_placeholder'></div><div id='top_deps_chart_placeholder'></div>"}
    </div>

    {f'''<div class="container">
        <h2>Vulnerability Details</h2>
        <div id="vuln_details_table_placeholder"></div>
        
        <h3>All Vulnerabilities</h3>
        <table>
            <thead>
                <tr>
                    <th>Dependency</th>
                    <th>CVE ID</th>
                    <th>Severity</th>
                    <th>CVSS Score</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {"".join(vuln_rows)}
            </tbody>
        </table>
    </div>''' if total_vulns > 0 else ""}

    <div class="container">
        <h2>Software Bill of Materials (SBOM)</h2>
        <p>Dependencies count: {total_deps}</p>
        <p>Generated at: {generated_at}</p>
    </div>
    
    {chaoss_section}

    <footer>
        <p>Generated with OSS Vulnerability Scanner</p>
    </footer>
</body>
</html>
"""
        return html_content
    
    def _generate_simple_text_report(self, template_data: Dict[str, Any]) -> str:
        """
        Generate a simple text report without Jinja2.
        
        Args:
            template_data: Template data.
            
        Returns:
            Text content.
        """
        # Extract data from template_data
        project_name = template_data.get("project_name", "Unknown")
        project_path = template_data.get("project_path", "")
        generated_at = template_data.get("generated_at", "")
        total_deps = len(template_data.get("dependencies", []))
        
        vuln_stats = template_data.get("vuln_stats", {})
        total_vulns = vuln_stats.get("total_vulns", 0)
        affected_deps = vuln_stats.get("affected_deps", 0)
        
        severity_counts = vuln_stats.get("severity_counts", {})
        critical = severity_counts.get("critical", 0)
        high = severity_counts.get("high", 0)
        medium = severity_counts.get("medium", 0)
        low = severity_counts.get("low", 0)
        unknown = severity_counts.get("unknown", 0)
        
        # Generate vulnerability section
        vuln_section = ""
        if total_vulns > 0:
            vuln_section = "Vulnerabilities by Dependency\n----------------------------\n"
            
            for dep_id, vulns in template_data.get("vulnerabilities", {}).items():
                vuln_section += f"\n{dep_id} ({len(vulns)} vulnerabilities)\n"
                vuln_section += "-" * (len(dep_id) + len(str(len(vulns))) + 18) + "\n"
                
                for vuln in vulns:
                    cve_id = vuln.get("cve_id", "N/A")
                    severity = vuln.get("severity", "UNKNOWN")
                    cvss_score = vuln.get("cvss_score", "N/A")
                    description = vuln.get("description", "")
                    if len(description) > 100:
                        description = description[:97] + "..."
                    
                    vuln_section += f"* {cve_id} - {severity} (CVSS: {cvss_score})\n"
                    vuln_section += f"  {description}\n"
                
                vuln_section += "\n"
        else:
            vuln_section = "No vulnerabilities found. Great job!\n"
        
        # Generate metrics section
        metrics_section = "Scan Metrics\n-----------\n"
        for key, value in template_data.get("metrics", {}).items():
            metrics_section += f"{key}: {value}\n"
        
        # Generate SBOM section
        sbom = template_data.get("sbom", {})
        sbom_section = f"""
Software Bill of Materials (SBOM)
--------------------------------
Dependencies count: {sbom.get("dependencies_count", total_deps)}
Generated at: {sbom.get("generated_at", generated_at)}
"""
        
        # Generate CHAOSS metrics section if available
        chaoss_section = ""
        if template_data.get("chaoss_metrics"):
            chaoss = template_data["chaoss_metrics"]
            risk = chaoss.get("risk", {})
            value = chaoss.get("value", {})
            evolution = chaoss.get("evolution", {})
            
            # Format float values
            vuln_density = f"{risk.get('vulnerability_density', 0):.2f}"
            critical_density = f"{risk.get('critical_vulnerability_density', 0):.2f}"
            license_risk = f"{risk.get('license_risk_score', 0):.2f}"
            security_score = f"{risk.get('odc_security_score', 0):.2f}"
            vuln_discovery_rate = f"{evolution.get('vulnerability_discovery_rate', 0):.2f}"
            
            chaoss_section = f"""
CHAOSS Metrics
-------------
Risk Metrics:
- Vulnerability Count: {risk.get('vulnerability_count', 0)}
- Vulnerability Density: {vuln_density}
- Critical Vulnerability Density: {critical_density}
- License Risk Score: {license_risk}
- Security Score: {security_score} / 10

Value Metrics:
- Total Dependencies: {value.get('total_dependencies', 0)}
- Direct Dependencies: {value.get('direct_dependencies', 0)}
- Transitive Dependencies: {value.get('transitive_dependencies', 0)}
- Dependency Depth: {value.get('dependency_depth', 0)}

Evolution Metrics:
- Vulnerability Discovery Rate: {vuln_discovery_rate} per year
"""
            if evolution.get("average_vulnerability_age"):
                chaoss_section += f"- Average Vulnerability Age: {evolution.get('average_vulnerability_age')} days\n"
        
        # Combine all sections
        title = "OSS Vulnerability Scan Report"
        title_line = "=" * len(title)
        
        text_content = f"""{title}
{title_line}

Summary
-------
Project: {project_name}
Path: {project_path}
Report Generated: {generated_at}
Dependencies Scanned: {total_deps}
Vulnerabilities Found: {total_vulns}
Affected Dependencies: {affected_deps}

Vulnerability Summary
--------------------
Critical: {critical}
High: {high}
Medium: {medium}
Low: {low}
Unknown: {unknown}

{vuln_section}
{metrics_section}
{sbom_section}
{chaoss_section}
Generated with OSS Vulnerability Scanner
"""
        
        return text_content