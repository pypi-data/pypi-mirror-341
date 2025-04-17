"""
Main entry point for the OSS Vulnerability Scanner.
"""

import os
import sys
import time
import logging
import argparse
import json
import datetime  
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class Scanner:
    """Main scanner class that orchestrates the scanning process."""

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        nvd_api_key: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
        calculate_chaoss_metrics: bool = True,
        verbose: bool = False
    ):
        """
        Initialize the scanner.

        Args:
            cache_dir: Directory to use for caching. If None, a default directory will be used.
            nvd_api_key: API key for the NVD API. If None, the scanner will use rate-limited public access.
            timeout: Timeout for HTTP requests in seconds.
            max_retries: Maximum number of retries for failed requests.
            calculate_chaoss_metrics: Whether to calculate CHAOSS metrics.
            verbose: Whether to enable verbose logging.
        """
        self.cache_dir = cache_dir or os.path.expanduser("~/.ossv-cache")
        self.nvd_api_key = nvd_api_key or os.environ.get("NVD_API_KEY")
        self.timeout = timeout
        self.max_retries = max_retries
        self.calculate_chaoss_metrics = calculate_chaoss_metrics
        self.verbose = verbose
        
        # Set up logging level
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Initialize components
        try:
            from ossv_scanner.caching.cache import Cache
            from ossv_scanner.vulnerability.nvd_client import NVDClient
            from ossv_scanner.utils.metrics import Metrics
            self.cache = Cache(self.cache_dir)
            self.nvd_client = NVDClient(
                api_key=self.nvd_api_key,
                cache=self.cache,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
            self.metrics = Metrics()
            
            # Initialize CHAOSS metrics if enabled
            if calculate_chaoss_metrics:
                try:
                    from ossv_scanner.utils.chaoss_metrics import CHAOSSMetrics
                    self.chaoss_metrics = CHAOSSMetrics()
                except ImportError:
                    logger.warning("CHAOSS metrics module not found. CHAOSS metrics will be disabled.")
                    self.chaoss_metrics = None
                    self.calculate_chaoss_metrics = False
            else:
                self.chaoss_metrics = None
        except ImportError as e:
            logger.error(f"Error initializing components: {str(e)}")
            raise

    def scan(self, project_path: str, sbom_only: bool = False) -> Dict[str, Any]:
        """
        Scan a project for dependencies and vulnerabilities.

        Args:
            project_path: Path to the project to scan.
            sbom_only: If True, only generate SBOM without checking for vulnerabilities.

        Returns:
            A dictionary containing the scan results.
        """
        start_time = time.time()
        self.metrics.start_scan()
        
        print(f"Starting scan of project at: {project_path}")
        
        # Ensure project path exists
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project path {project_path} does not exist")
        
        # Get the appropriate parser for the project
        print("Analyzing project structure...")
        try:
            from ossv_scanner.parsers import get_parser_for_project
            parser = get_parser_for_project(project_path)
            if not parser:
                print("No suitable parser found for the project.")
                return {"error": "No suitable parser found for the project"}
        except ImportError as e:
            logger.error(f"Error importing parser module: {str(e)}")
            return {"error": f"Error importing parser module: {str(e)}"}
        
        # Parse dependencies
        print("Parsing dependencies...")
        print(f"Using parser: {parser.__class__.__name__}")
        dependencies = parser.parse()
        print(f"Found {len(dependencies)} direct dependencies")
        
        # Generate SBOM
        print("Generating SBOM...")
        try:
            from ossv_scanner.sbom.generator import SBOMGenerator
            sbom_generator = SBOMGenerator()
            sbom = sbom_generator.generate(dependencies, project_path)
            print("SBOM generated successfully")
        except ImportError as e:
            logger.error(f"Error importing SBOM generator: {str(e)}")
            return {"error": f"Error importing SBOM generator: {str(e)}"}
        
        results = {
            "project_path": project_path,
            "dependencies": dependencies,
            "sbom": sbom,
            "vulnerabilities": {},
            "metrics": {},
            "start_time": datetime.datetime.utcnow().isoformat(),
        }
        
        # Check for vulnerabilities if requested
        if not sbom_only:
            print("Checking for vulnerabilities...")
            vulnerabilities = self._check_vulnerabilities(dependencies)
            results["vulnerabilities"] = vulnerabilities
            
            total_vulns = sum(len(v) for v in vulnerabilities.values())
            print(f"Found {total_vulns} vulnerabilities")
        
        # Calculate and store metrics
        scan_time = time.time() - start_time
        self.metrics.end_scan()
        metrics_data = self.metrics.get_metrics()
        metrics_data["scan_time"] = scan_time
        results["metrics"] = metrics_data
        results["end_time"] = datetime.datetime.utcnow().isoformat()
        
        # Calculate CHAOSS metrics if enabled
        if self.calculate_chaoss_metrics and self.chaoss_metrics:
            print("Calculating CHAOSS metrics...")
            chaoss_metrics_data = self.chaoss_metrics.calculate_metrics(
                project_path, 
                results["dependencies"],
                results.get("vulnerabilities", {}),
                results.get("sbom", {})
            )
            results["chaoss_metrics"] = chaoss_metrics_data
            
            # Add debug statement
            print(f"CHAOSS metrics: {bool(results['chaoss_metrics'])}")
            print(f"CHAOSS metrics keys: {results['chaoss_metrics'].keys() if results['chaoss_metrics'] else 'None'}")
        
        print(f"Scan completed in {scan_time:.2f} seconds")
        
        return results
    
    def _check_vulnerabilities(self, dependencies: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Check dependencies for vulnerabilities.

        Args:
            dependencies: List of dependencies to check.

        Returns:
            A dictionary mapping dependency identifiers to lists of vulnerabilities.
        """
        vulnerabilities = {}
        total_deps = len(dependencies)
        
        print(f"Checking {total_deps} dependencies for vulnerabilities...")
        
        for i, dependency in enumerate(dependencies):
            dep_id = f"{dependency['name']}@{dependency['version']}"
            
            try:
                vulns = self.nvd_client.get_vulnerabilities(
                    dependency["name"], dependency["version"]
                )
                if vulns:
                    vulnerabilities[dep_id] = vulns
            except Exception as e:
                logger.error(f"Error checking vulnerabilities for {dep_id}: {str(e)}")
                vulnerabilities[dep_id] = [{"error": str(e)}]
            
            # Print progress
            if (i + 1) % 5 == 0 or (i + 1) == total_deps:
                print(f"Progress: {i + 1}/{total_deps} dependencies checked")
        
        return vulnerabilities
    
    def generate_report(
        self, 
        results: Dict[str, Any], 
        output_format: str = "html", 
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate a report from scan results.

        Args:
            results: Scan results from the scan method.
            output_format: Report format (html, json, text).
            output_path: Path to write the report to. If None, a default path will be used.

        Returns:
            Path to the generated report.
        """
        if "error" in results:
            raise ValueError(f"Cannot generate report from error results: {results['error']}")
        
        if not output_path:
            # Generate default filename based on project path and timestamp
            project_name = os.path.basename(results["project_path"])
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_path = f"ossv-report-{project_name}-{timestamp}.{output_format}"
        
        print(f"Generating {output_format} report...")
        
        try:
            from ossv_scanner.reporting.reporter import Reporter
            reporter = Reporter()
            report_path = reporter.generate(results, output_format, output_path)
            
            # Generate visualizations if HTML format
            if output_format.lower() == "html":
                try:
                    from ossv_scanner.visualization.visualizer import Visualizer
                    visualizer = Visualizer()
                    visualizer.generate(results, report_path)
                except ImportError as e:
                    logger.warning(f"Error importing visualizer: {str(e)}")
                    logger.warning("Visualizations will not be included in the report.")
            
            print(f"Report generated at: {report_path}")
            return report_path
        except ImportError as e:
            logger.error(f"Error importing reporter module: {str(e)}")
            
            # Fallback to JSON report if reporter module is not available
            if output_format.lower() == "json":
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                print(f"Fallback JSON report generated at: {output_path}")
                return output_path
            else:
                raise
                
    def generate_metrics_dashboard(
        self, 
        results: Dict[str, Any], 
        output_dir: Optional[str] = None,
        include_raw_data: bool = True
    ) -> str:
        """
        Generate a comprehensive metrics dashboard with visualizations.
        
        Args:
            results: Scan results
            output_dir: Directory to store dashboard and visualization files
            include_raw_data: Whether to include raw data in downloads
            
        Returns:
            Path to the generated dashboard HTML file
        """
        from ossv_scanner.metrics_dashboard.dashboard import MetricsDashboard
        
        # Create default output directory if not provided
        if not output_dir:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_dir = os.path.join(os.getcwd(), f"ossv-dashboard-{timestamp}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create metrics dashboard
        dashboard = MetricsDashboard()
        
        # Collect metrics
        print("Collecting comprehensive metrics...")
        dashboard_metrics = dashboard.collect_metrics(results)
        
        # Generate visualizations
        print("Generating metric visualizations...")
        vis_dir = os.path.join(output_dir, "visualizations")
        visualizations = dashboard.generate_visualizations(vis_dir)
        
        # Export raw data
        json_path = os.path.join(output_dir, "raw_metrics.json")
        csv_path = os.path.join(output_dir, "raw_metrics.csv")
        
        if include_raw_data:
            print("Exporting raw metrics data...")
            dashboard.export_raw_data("json", json_path)
            dashboard.export_raw_data("csv", csv_path)
        
        # Generate dashboard HTML
        dashboard_path = os.path.join(output_dir, "metrics_dashboard.html")
        
        # Pretty-print raw data for HTML display
        import json
        raw_data_pretty = json.dumps(dashboard_metrics, indent=2)
        
        try:
            from ossv_scanner.reporting.reporter import Reporter
            reporter = Reporter()
            
            # Use Jinja2 for template rendering if available
            if reporter.jinja_env:
                template = reporter.jinja_env.get_template("metrics_dashboard.html.j2")
                html_content = template.render(
                    project_name=os.path.basename(results.get("project_path", "")),
                    dashboard_metrics=dashboard_metrics,
                    visualizations=visualizations,
                    raw_data_json=os.path.relpath(json_path, output_dir),
                    raw_data_csv=os.path.relpath(csv_path, output_dir),
                    raw_data_pretty=raw_data_pretty
                )
                
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            else:
                # Fallback to basic HTML if Jinja2 is not available
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>OSS Vulnerability Scanner - Metrics Dashboard</title>
</head>
<body>
    <h1>OSS Vulnerability Scanner - Metrics Dashboard</h1>
    <p>Project: {os.path.basename(results.get("project_path", ""))}</p>
    <h2>Visualizations</h2>
    {' '.join(f'<img src="{vis_path}" style="max-width:100%;">' for vis_path in visualizations.values())}
    <h2>Raw Data</h2>
    <pre>{raw_data_pretty}</pre>
</body>
</html>""")
        
        except Exception as e:
            logger.error(f"Error generating dashboard: {str(e)}")
            # Create a simple fallback dashboard
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>OSS Vulnerability Scanner - Metrics Dashboard</title>
</head>
<body>
    <h1>OSS Vulnerability Scanner - Metrics Dashboard</h1>
    <p>Error generating full dashboard: {str(e)}</p>
    <h2>Raw Data</h2>
    <pre>{raw_data_pretty}</pre>
</body>
</html>""")
        
        print(f"Metrics dashboard generated at: {dashboard_path}")
        return dashboard_path


def main():
    """Command line entry point."""
    parser = argparse.ArgumentParser(description="OSS Vulnerability Scanner")
    parser.add_argument("project_path", help="Path to the project to scan")
    parser.add_argument("--sbom-only", action="store_true", help="Only generate SBOM without checking for vulnerabilities")
    parser.add_argument("--output-format", choices=["html", "json", "text"], default="html", help="Report output format")
    parser.add_argument("--output-path", help="Path to write the report to")
    parser.add_argument("--cache-dir", help="Directory to use for caching")
    parser.add_argument("--nvd-api-key", help="API key for the NVD API")
    parser.add_argument("--no-chaoss-metrics", action="store_true", help="Disable CHAOSS metrics calculation")
    parser.add_argument("--generate-dashboard", action="store_true", help="Generate metrics dashboard with visualizations")
    parser.add_argument("--dashboard-dir", help="Directory to store dashboard files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    try:
        scanner = Scanner(
            cache_dir=args.cache_dir,
            nvd_api_key=args.nvd_api_key,
            calculate_chaoss_metrics=not args.no_chaoss_metrics,
            verbose=args.verbose
        )
        
        results = scanner.scan(args.project_path, args.sbom_only)
        
        if "error" not in results:
            scanner.generate_report(results, args.output_format, args.output_path)
            
            # Generate metrics dashboard if requested
            if args.generate_dashboard:
                scanner.generate_metrics_dashboard(results, args.dashboard_dir)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()