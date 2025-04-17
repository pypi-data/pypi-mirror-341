"""
Metrics collection for OSS Vulnerability Scanner.
"""

import time
import logging
import threading
import datetime
import os
from typing import Dict, Any, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger(__name__)


class Metrics:
    """Collect and report metrics about scanner performance."""

    def __init__(self):
        """Initialize the metrics collector."""
        self.start_time = 0
        self.end_time = 0
        self.api_calls = 0
        self.api_errors = 0
        self.api_response_times = []
        self.cache_hits = 0
        self.cache_misses = 0
        self._lock = threading.RLock()
        self.dependencies_count = 0
        self.transitive_dependencies_count = 0
        self.vulnerability_count = 0
        
        # Initialize process monitoring if psutil is available
        if HAS_PSUTIL:
            try:
                self.process = psutil.Process()
            except Exception as e:
                logger.warning(f"Error initializing process monitoring: {str(e)}")
                self.process = None
        else:
            self.process = None
    
    def start_scan(self) -> None:
        """Record the start of a scan."""
        with self._lock:
            self.start_time = time.time()
    
    def end_scan(self) -> None:
        """Record the end of a scan."""
        with self._lock:
            self.end_time = time.time()
    
    def record_api_call(self, response_time: float, is_error: bool = False) -> None:
        """
        Record an API call.

        Args:
            response_time: Time taken for the API call in seconds.
            is_error: Whether the API call resulted in an error.
        """
        with self._lock:
            self.api_calls += 1
            self.api_response_times.append(response_time)
            if is_error:
                self.api_errors += 1
    
    def record_cache_hit(self) -> None:
        """Record a cache hit."""
        with self._lock:
            self.cache_hits += 1
    
    def record_cache_miss(self) -> None:
        """Record a cache miss."""
        with self._lock:
            self.cache_misses += 1
    
    def set_dependencies_count(self, direct: int, transitive: int) -> None:
        """
        Set the count of dependencies.

        Args:
            direct: Number of direct dependencies.
            transitive: Number of transitive dependencies.
        """
        with self._lock:
            self.dependencies_count = direct
            self.transitive_dependencies_count = transitive
    
    def set_vulnerability_count(self, count: int) -> None:
        """
        Set the count of vulnerabilities.

        Args:
            count: Number of vulnerabilities.
        """
        with self._lock:
            self.vulnerability_count = count
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.

        Returns:
            Dictionary of metrics.
        """
        with self._lock:
            # Calculate scan time
            scan_time = self.end_time - self.start_time if self.end_time > 0 else 0
            
            # Calculate average API response time
            avg_response_time = 0
            if self.api_response_times:
                avg_response_time = sum(self.api_response_times) / len(self.api_response_times)
            
            # Calculate cache hit rate
            cache_hit_rate = 0
            if (self.cache_hits + self.cache_misses) > 0:
                cache_hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses)
            
            # Get resource usage if psutil is available
            memory_usage = 0
            cpu_percent = 0
            
            if self.process:
                try:
                    memory_usage = self.process.memory_info().rss
                    cpu_percent = self.process.cpu_percent()
                except Exception as e:
                    logger.warning(f"Error getting process stats: {str(e)}")
            
            # Get thread count
            thread_count = threading.active_count()
            
            # Get current time with timezone
            current_time = datetime.datetime.now(datetime.timezone.utc)
            
            return {
                "scan_time_seconds": scan_time,
                "api_calls": self.api_calls,
                "api_errors": self.api_errors,
                "api_error_rate": self.api_errors / self.api_calls if self.api_calls > 0 else 0,
                "avg_api_response_time": avg_response_time,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": cache_hit_rate,
                "dependencies_count": self.dependencies_count,
                "transitive_dependencies_count": self.transitive_dependencies_count,
                "vulnerability_count": self.vulnerability_count,
                "memory_usage_bytes": memory_usage,
                "cpu_percent": cpu_percent,
                "thread_count": thread_count,
                "timestamp": current_time.isoformat(),
            }
    
    def log_metrics(self) -> None:
        """Log metrics to the logger."""
        metrics = self.get_metrics()
        logger.info(f"Scan completed in {metrics['scan_time_seconds']:.2f} seconds")
        logger.info(f"API calls: {metrics['api_calls']}, errors: {metrics['api_errors']}")
        logger.info(f"Cache hit rate: {metrics['cache_hit_rate']:.2%}")
        logger.info(f"Dependencies: {metrics['dependencies_count']} direct, {metrics['transitive_dependencies_count']} transitive")
        logger.info(f"Vulnerabilities: {metrics['vulnerability_count']}")
        logger.info(f"Memory usage: {metrics['memory_usage_bytes'] / (1024 * 1024):.1f} MB")
        logger.info(f"CPU usage: {metrics['cpu_percent']:.1f}%")