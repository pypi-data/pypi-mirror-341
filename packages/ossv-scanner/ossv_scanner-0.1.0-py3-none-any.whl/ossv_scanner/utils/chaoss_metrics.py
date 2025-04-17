"""
CHAOSS metrics implementation for OSS Vulnerability Scanner.

This module implements Community Health Analytics Open Source Software (CHAOSS)
metrics for evaluating the health and sustainability of open source projects.
"""

import os
import logging
import datetime
import statistics
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class CHAOSSMetrics:
    """Calculate CHAOSS metrics for open source projects."""

    def __init__(self):
        """Initialize the CHAOSS metrics calculator."""
        self.metrics = {}
    
    def calculate_metrics(
        self, 
        project_path: str,
        dependencies: List[Dict[str, Any]],
        vulnerabilities: Dict[str, List[Dict[str, Any]]],
        sbom: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate CHAOSS metrics for a project.

        Args:
            project_path: Path to the project.
            dependencies: List of dependency dictionaries.
            vulnerabilities: Dictionary mapping dependency IDs to vulnerabilities.
            sbom: SBOM data.

        Returns:
            Dictionary of CHAOSS metrics.
        """
        logger.debug(f"Calculating CHAOSS metrics for project at {project_path}")
        
        # Calculate Risk metrics
        risk_metrics = self._calculate_risk_metrics(dependencies, vulnerabilities)
        
        # Calculate Value metrics
        value_metrics = self._calculate_value_metrics(dependencies)
        
        # Calculate Evolution metrics
        evolution_metrics = self._calculate_evolution_metrics(vulnerabilities)
        
        # Combine all metrics
        self.metrics = {
            "risk": risk_metrics,
            "value": value_metrics,
            "evolution": evolution_metrics,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        return self.metrics
    
    def _calculate_risk_metrics(
        self, 
        dependencies: List[Dict[str, Any]],
        vulnerabilities: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Calculate CHAOSS Risk metrics.

        Args:
            dependencies: List of dependency dictionaries.
            vulnerabilities: Dictionary mapping dependency IDs to vulnerabilities.

        Returns:
            Dictionary of Risk metrics.
        """
        # Count total vulnerabilities
        total_vulns = sum(len(vulns) for vulns in vulnerabilities.values())
        
        # Count vulnerabilities by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0}
        for dep_vulns in vulnerabilities.values():
            for vuln in dep_vulns:
                severity = vuln.get("severity", "UNKNOWN").lower()
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Calculate vulnerability density (vulns per dependency)
        vuln_density = total_vulns / len(dependencies) if dependencies else 0
        
        # Calculate critical vulnerability density
        critical_density = (
            (severity_counts["critical"] + severity_counts["high"]) / len(dependencies)
            if dependencies else 0
        )
        
        # Calculate license risk score
        license_risk, license_compliance = self._calculate_license_metrics(dependencies)
        
        return {
            "vulnerability_count": total_vulns,
            "vulnerability_density": vuln_density,
            "critical_vulnerability_density": critical_density,
            "severity_distribution": severity_counts,
            "license_risk_score": license_risk,
            "license_compliance": license_compliance,
            "odc_security_score": self._calculate_odc_security_score(
                total_vulns, severity_counts, len(dependencies)
            ),
        }
    
    def _calculate_value_metrics(self, dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate CHAOSS Value metrics.

        Args:
            dependencies: List of dependency dictionaries.

        Returns:
            Dictionary of Value metrics.
        """
        # Calculate dependency count
        total_deps = len(dependencies)
        direct_deps = sum(1 for dep in dependencies if dep.get("is_direct", True))
        transitive_deps = total_deps - direct_deps
        
        # Analyze dependency types
        package_types = {}
        for dep in dependencies:
            pkg_type = dep.get("package_type", "unknown")
            package_types[pkg_type] = package_types.get(pkg_type, 0) + 1
        
        # Calculate dependency depth (simplified)
        depth = self._estimate_dependency_depth(dependencies)
        
        return {
            "total_dependencies": total_deps,
            "direct_dependencies": direct_deps,
            "transitive_dependencies": transitive_deps,
            "dependency_depth": depth,
            "package_types": package_types,
            "dependency_freshness": self._calculate_dependency_freshness(dependencies),
        }
    
    def _calculate_evolution_metrics(
        self, vulnerabilities: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Calculate CHAOSS Evolution metrics.

        Args:
            vulnerabilities: Dictionary mapping dependency IDs to vulnerabilities.

        Returns:
            Dictionary of Evolution metrics.
        """
        # Collect CVE publication dates
        cve_dates = []
        cve_years = {}
        
        for vulns in vulnerabilities.values():
            for vuln in vulns:
                if "published_date" in vuln and vuln["published_date"]:
                    try:
                        date_str = vuln["published_date"]
                        # Ensure proper timezone format and parsing
                        if date_str.endswith("Z"):
                            date_str = date_str.replace("Z", "+00:00")
                        
                        # Parse the date, handling different ISO formats
                        try:
                            date = datetime.datetime.fromisoformat(date_str)
                        except ValueError:
                            # Fall back to a simpler parsing if fromisoformat fails
                            date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                            # Make naive datetime timezone-aware
                            date = date.replace(tzinfo=datetime.timezone.utc)
                        
                        # Ensure the date has timezone info
                        if date.tzinfo is None:
                            date = date.replace(tzinfo=datetime.timezone.utc)
                            
                        cve_dates.append(date)
                        
                        year = date.year
                        cve_years[year] = cve_years.get(year, 0) + 1
                    except (ValueError, TypeError) as e:
                        logger.debug(f"Error parsing date '{vulns.get('published_date')}': {str(e)}")
                        pass
        
        # Calculate average age of vulnerabilities
        avg_age = None
        if cve_dates:
            # Ensure a timezone-aware now
            now = datetime.datetime.now(datetime.timezone.utc)
            
            # Calculate age for each vulnerability
            ages = []
            for date in cve_dates:
                # Double-check that each date has timezone info
                if date.tzinfo is None:
                    date = date.replace(tzinfo=datetime.timezone.utc)
                ages.append((now - date).days)
                
            avg_age = statistics.mean(ages) if ages else None
        
        return {
            "vulnerability_discovery_rate": len(cve_dates) / len(cve_years) if cve_years else 0,
            "average_vulnerability_age": avg_age,
            "vulnerability_age_distribution": self._calculate_age_distribution(cve_dates),
            "cve_years_distribution": dict(sorted(cve_years.items())),
        }
    
    def _calculate_license_metrics(
        self, dependencies: List[Dict[str, Any]]
    ) -> Tuple[float, Dict[str, int]]:
        """
        Calculate license risk score and compliance.

        Args:
            dependencies: List of dependency dictionaries.

        Returns:
            Tuple of (license_risk_score, license_compliance_dict).
        """
        # Count licenses
        licenses = {}
        unknown_count = 0
        
        for dep in dependencies:
            license_str = dep.get("license")
            if license_str:
                licenses[license_str] = licenses.get(license_str, 0) + 1
            else:
                unknown_count += 1
        
        # Calculate license compliance
        compliance = {
            "total_dependencies": len(dependencies),
            "with_license": len(dependencies) - unknown_count,
            "without_license": unknown_count,
            "compliance_rate": (len(dependencies) - unknown_count) / len(dependencies) if dependencies else 0,
        }
        
        # Calculate rough risk score based on unknown licenses
        # This is a simplified model - a real implementation would assess each license's compatibility
        license_risk_score = unknown_count / len(dependencies) * 10 if dependencies else 0
        
        return license_risk_score, compliance
    
    def _calculate_odc_security_score(
        self, total_vulns: int, severity_counts: Dict[str, int], total_deps: int
    ) -> float:
        """
        Calculate a security score based on Open Source Security Foundation metrics.

        Args:
            total_vulns: Total number of vulnerabilities.
            severity_counts: Dictionary of vulnerability counts by severity.
            total_deps: Total number of dependencies.

        Returns:
            Security score (0-10, 10 being best).
        """
        if total_deps == 0:
            return 10.0
        
        # Weighted score - critical vulns have highest impact
        weighted_score = (
            severity_counts["critical"] * 10 +
            severity_counts["high"] * 5 +
            severity_counts["medium"] * 2 +
            severity_counts["low"] * 0.5
        )
        
        # Normalize to 0-10 scale, inverse (10 is best)
        norm_factor = total_deps * 0.5  # Rough normalization factor
        raw_score = 10 - min(10, weighted_score / norm_factor)
        
        return max(0, raw_score)
    
    def _estimate_dependency_depth(self, dependencies: List[Dict[str, Any]]) -> int:
        """
        Estimate the depth of the dependency tree.

        Args:
            dependencies: List of dependency dictionaries.

        Returns:
            Estimated depth of dependency tree.
        """
        # This is a simplified implementation
        # A real implementation would use the full dependency tree
        direct_deps = [d for d in dependencies if d.get("is_direct", True)]
        transitive_deps = [d for d in dependencies if not d.get("is_direct", True)]
        
        if not transitive_deps:
            return 1
        
        # Rough estimate based on ratio
        return min(5, max(2, int(len(transitive_deps) / len(direct_deps) + 1))) if direct_deps else 1
    
    def _calculate_dependency_freshness(
        self, dependencies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate dependency freshness metrics.

        Args:
            dependencies: List of dependency dictionaries.

        Returns:
            Dictionary of freshness metrics.
        """
        # This is a placeholder - real implementation would check latest versions
        versions = {}
        for dep in dependencies:
            package_type = dep.get("package_type", "unknown")
            if package_type not in versions:
                versions[package_type] = []
            
            versions[package_type].append(dep.get("version", "unknown"))
        
        return {
            "dependency_types": list(versions.keys()),
            "version_sample": {k: v[:5] for k, v in versions.items()},
            # Additional freshness metrics would require external API calls
            # to check latest versions of each dependency
        }
    
    def _calculate_age_distribution(
        self, dates: List[datetime.datetime]
    ) -> Dict[str, int]:
        """
        Calculate age distribution of vulnerabilities.

        Args:
            dates: List of vulnerability publication dates.

        Returns:
            Dictionary mapping age ranges to counts.
        """
        if not dates:
            return {}
        
        # Make sure we use timezone-aware datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Define age buckets (in days)
        buckets = {
            "0-90 days": 0,
            "91-180 days": 0,
            "181-365 days": 0,
            "1-2 years": 0,
            "2+ years": 0
        }
        
        for date in dates:
            # Ensure date has timezone info
            if date.tzinfo is None:
                date = date.replace(tzinfo=datetime.timezone.utc)
                
            age = (now - date).days
            
            if age <= 90:
                buckets["0-90 days"] += 1
            elif age <= 180:
                buckets["91-180 days"] += 1
            elif age <= 365:
                buckets["181-365 days"] += 1
            elif age <= 730:
                buckets["1-2 years"] += 1
            else:
                buckets["2+ years"] += 1
        
        return buckets
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metrics to a dictionary.

        Returns:
            Dictionary of all metrics.
        """
        return self.metrics