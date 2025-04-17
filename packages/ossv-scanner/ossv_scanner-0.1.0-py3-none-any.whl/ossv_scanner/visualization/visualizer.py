"""
Visualization implementation for OSS Vulnerability Scanner.
"""

import os
import json
import logging
import tempfile
from typing import Dict, List, Any, Optional
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Visualizer:
    """Visualizer for creating visual representations of vulnerability data."""

    def __init__(self):
        """Initialize the visualizer."""
        # Set up styles for matplotlib
        sns.set_style("whitegrid")
        plt.rcParams["figure.figsize"] = (10, 6)
    
    def generate(self, results: Dict[str, Any], report_path: str) -> bool:
        """
        Generate visualizations for the scan results.

        Args:
            results: Scan results dictionary.
            report_path: Path to the HTML report to embed visualizations in.

        Returns:
            True if successful, False otherwise.
        """
        logger.debug(f"Generating visualizations for report at {report_path}")
        
        try:
            # Check if report exists and is HTML
            if not os.path.exists(report_path) or not report_path.endswith(".html"):
                logger.warning(f"Report file {report_path} does not exist or is not HTML.")
                return False
            
            # Extract vulnerability data from results
            vulnerabilities = results.get("vulnerabilities", {})
            if not vulnerabilities:
                logger.info("No vulnerabilities found, skipping visualizations.")
                return True
            
            # Generate charts using Plotly
            chart_data = self._generate_plotly_charts(vulnerabilities)
            
            # Embed the charts in the HTML report
            self._embed_charts_in_report(report_path, chart_data)
            
            return True
        
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
            return False
    
    def _generate_plotly_charts(self, vulnerabilities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, str]:
        """
        Generate Plotly charts for vulnerabilities.

        Args:
            vulnerabilities: Vulnerability data.

        Returns:
            Dictionary mapping chart names to HTML strings.
        """
        chart_data = {}
        
        try:
            # Prepare data for charts
            severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
            dep_vuln_counts = {}
            cve_years = {}
            
            for dep_id, vulns in vulnerabilities.items():
                dep_vuln_counts[dep_id] = len(vulns)
                
                for vuln in vulns:
                    severity = vuln.get("severity", "UNKNOWN")
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                    # Extract year from CVE ID (e.g., CVE-2022-1234 -> 2022)
                    cve_id = vuln.get("cve_id", "")
                    if cve_id and cve_id.startswith("CVE-"):
                        try:
                            year = cve_id.split("-")[1]
                            cve_years[year] = cve_years.get(year, 0) + 1
                        except (IndexError, ValueError):
                            pass
            
            # Generate severity distribution chart
            chart_data["severity_chart"] = self._create_severity_chart(severity_counts)
            
            # Generate top vulnerable dependencies chart
            chart_data["top_deps_chart"] = self._create_top_dependencies_chart(dep_vuln_counts)
            
            # Generate CVE age chart
            if cve_years:
                chart_data["cve_age_chart"] = self._create_cve_age_chart(cve_years)
            
            # Generate vulnerability details table
            chart_data["vuln_details_table"] = self._create_vuln_details_table(vulnerabilities)
            
            return chart_data
        
        except Exception as e:
            logger.error(f"Error generating Plotly charts: {str(e)}")
            return {}
    
    def _create_severity_chart(self, severity_counts: Dict[str, int]) -> str:
        """
        Create a chart showing vulnerability severity distribution.

        Args:
            severity_counts: Dictionary mapping severity levels to counts.

        Returns:
            HTML string of the chart.
        """
        # Sort severities by risk level
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]
        labels = []
        values = []
        colors = []
        
        for severity in severity_order:
            count = severity_counts.get(severity, 0)
            if count > 0:
                labels.append(severity)
                values.append(count)
                
                # Set colors based on severity
                if severity == "CRITICAL":
                    colors.append("rgb(203, 24, 29)")
                elif severity == "HIGH":
                    colors.append("rgb(248, 106, 43)")
                elif severity == "MEDIUM":
                    colors.append("rgb(255, 193, 7)")
                elif severity == "LOW":
                    colors.append("rgb(40, 167, 69)")
                else:
                    colors.append("rgb(108, 117, 125)")
        
        # Create pie chart with labels
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors,
            textinfo="label+value+percent",
            pull=[0.1 if label == "CRITICAL" else 0 for label in labels],
        )])
        
        fig.update_layout(
            title="Vulnerability Severity Distribution",
            font=dict(size=14),
            legend_title="Severity",
            height=500,
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_top_dependencies_chart(self, dep_vuln_counts: Dict[str, int]) -> str:
        """
        Create a chart showing the top vulnerable dependencies.

        Args:
            dep_vuln_counts: Dictionary mapping dependency IDs to vulnerability counts.

        Returns:
            HTML string of the chart.
        """
        # Sort dependencies by vulnerability count (descending)
        sorted_deps = sorted(
            dep_vuln_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Take top 10
        top_deps = sorted_deps[:10]
        
        # If more than 10, add an "Others" category
        other_count = sum(count for _, count in sorted_deps[10:])
        if other_count > 0:
            top_deps.append(("Others", other_count))
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[dep for dep, _ in top_deps],
            y=[count for _, count in top_deps],
            text=[count for _, count in top_deps],
            textposition="outside",
            marker_color="rgba(76, 114, 176, 0.8)",
            hoverinfo="x+y",
        ))
        
        fig.update_layout(
            title="Top Vulnerable Dependencies",
            xaxis=dict(title="Dependency"),
            yaxis=dict(title="Number of Vulnerabilities"),
            font=dict(size=14),
            height=500,
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_cve_age_chart(self, cve_years: Dict[str, int]) -> str:
        """
        Create a chart showing CVE distribution by year.

        Args:
            cve_years: Dictionary mapping years to CVE counts.

        Returns:
            HTML string of the chart.
        """
        # Sort years
        sorted_years = sorted(cve_years.items())
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[year for year, _ in sorted_years],
            y=[count for _, count in sorted_years],
            mode="markers+lines",
            name="CVEs",
            marker=dict(size=10),
            line=dict(width=3),
            hoverinfo="x+y",
        ))
        
        fig.update_layout(
            title="CVE Distribution by Year",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Number of CVEs"),
            font=dict(size=14),
            height=400,
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_vuln_details_table(self, vulnerabilities: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Create an interactive table of vulnerability details.

        Args:
            vulnerabilities: Vulnerability data.

        Returns:
            HTML string of the table.
        """
        # Prepare data for table
        table_data = []
        
        for dep_id, vulns in vulnerabilities.items():
            for vuln in vulns:
                table_data.append({
                    "Dependency": dep_id,
                    "CVE ID": vuln.get("cve_id", "N/A"),
                    "Severity": vuln.get("severity", "UNKNOWN"),
                    "CVSS Score": vuln.get("cvss_score", "N/A"),
                    "Published": vuln.get("published_date", "N/A"),
                })
        
        # Sort by severity and CVSS score
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
        table_data.sort(
            key=lambda x: (
                severity_order.get(x["Severity"], 999),
                -float(x["CVSS Score"]) if isinstance(x["CVSS Score"], (int, float)) else 0
            )
        )
        
        # Create table with Plotly
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(table_data[0].keys()) if table_data else [],
                fill_color="rgb(76, 114, 176)",
                align="left",
                font=dict(color="white", size=14),
            ),
            cells=dict(
                values=[
                    [item[key] for item in table_data]
                    for key in table_data[0].keys()
                ] if table_data else [],
                fill_color=[
                    ["rgb(255, 255, 255)"] * len(table_data)
                ] + [
                    [
                        "rgba(203, 24, 29, 0.2)" if item["Severity"] == "CRITICAL" else
                        "rgba(248, 106, 43, 0.2)" if item["Severity"] == "HIGH" else
                        "rgba(255, 193, 7, 0.2)" if item["Severity"] == "MEDIUM" else
                        "rgba(40, 167, 69, 0.2)" if item["Severity"] == "LOW" else
                        "rgb(255, 255, 255)"
                        for item in table_data
                    ]
                ] + [["rgb(255, 255, 255)"] * len(table_data)] * 3,
                align="left",
                font=dict(size=13),
            )
        )])
        
        fig.update_layout(
            title="Vulnerability Details",
            height=600,
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _embed_charts_in_report(self, report_path: str, chart_data: Dict[str, str]) -> None:
        """
        Embed charts in the HTML report.

        Args:
            report_path: Path to the HTML report.
            chart_data: Dictionary mapping chart names to HTML strings.
        """
        try:
            # Read the HTML report
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find chart placeholders and replace them
            for chart_name, chart_html in chart_data.items():
                placeholder = soup.find(id=f"{chart_name}_placeholder")
                if placeholder:
                    placeholder.clear()
                    placeholder.append(BeautifulSoup(chart_html, 'html.parser'))
            
            # Write updated HTML back to file
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            logger.debug(f"Successfully embedded charts in report at {report_path}")
        
        except Exception as e:
            logger.error(f"Error embedding charts in report: {str(e)}")
            raise
