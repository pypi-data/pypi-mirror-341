"""
Cache implementation for OSS Vulnerability Scanner.
"""

import os
import json
import time
import logging
import hashlib
import threading
from typing import Dict, Any, Optional, Union

from diskcache import Cache as DiskCache

logger = logging.getLogger(__name__)


class Cache:
    """Cache implementation for storing vulnerability data and API responses."""

    def __init__(
        self,
        cache_dir: str,
        ttl: int = 86400,  # 24 hours
        max_size: int = 1_000_000_000  # 1 GB
    ):
        """
        Initialize the cache.

        Args:
            cache_dir: Directory to store cache files.
            ttl: Time-to-live for cache entries in seconds.
            max_size: Maximum size of the cache in bytes.
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.max_size = max_size
        self._lock = threading.RLock()
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize disk cache
        self._cache = DiskCache(cache_dir, size_limit=max_size)
        
        logger.debug(f"Cache initialized at {cache_dir}")
        
        # Track cache metrics
        self.hits = 0
        self.misses = 0
        self.sets = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Cached value or None if not found.
        """
        hashed_key = self._hash_key(key)
        
        with self._lock:
            try:
                value = self._cache.get(hashed_key, default=None, expire_time=True)
                
                if value is None:
                    self.misses += 1
                    return None
                
                # value is a tuple of (data, expire_time)
                data, expire_time = value
                
                # Check if expired
                if expire_time is not None and expire_time < time.time():
                    self.misses += 1
                    return None
                
                self.hits += 1
                return data
            
            except Exception as e:
                logger.warning(f"Error getting from cache: {str(e)}")
                self.misses += 1
                return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to store.
            ttl: Time-to-live in seconds. If None, use the default TTL.

        Returns:
            True if successful, False otherwise.
        """
        hashed_key = self._hash_key(key)
        ttl = ttl or self.ttl
        
        with self._lock:
            try:
                self._cache.set(hashed_key, value, expire=ttl)
                self.sets += 1
                return True
            
            except Exception as e:
                logger.warning(f"Error setting cache: {str(e)}")
                return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key.

        Returns:
            True if successful, False otherwise.
        """
        hashed_key = self._hash_key(key)
        
        with self._lock:
            try:
                return self._cache.delete(hashed_key)
            
            except Exception as e:
                logger.warning(f"Error deleting from cache: {str(e)}")
                return False
    
    def clear(self) -> bool:
        """
        Clear the entire cache.

        Returns:
            True if successful, False otherwise.
        """
        with self._lock:
            try:
                self._cache.clear()
                return True
            
            except Exception as e:
                logger.warning(f"Error clearing cache: {str(e)}")
                return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary of cache statistics.
        """
        with self._lock:
            try:
                hit_rate = 0
                if (self.hits + self.misses) > 0:
                    hit_rate = self.hits / (self.hits + self.misses)
                
                stats = {
                    "hits": self.hits,
                    "misses": self.misses,
                    "sets": self.sets,
                    "hit_rate": hit_rate,
                    "size": self._cache.volume(),
                    "max_size": self.max_size,
                    "utilization": self._cache.volume() / self.max_size if self.max_size > 0 else 0,
                    "entry_count": len(self._cache),
                }
                
                return stats
            
            except Exception as e:
                logger.warning(f"Error getting cache stats: {str(e)}")
                return {
                    "hits": self.hits,
                    "misses": self.misses,
                    "sets": self.sets,
                    "error": str(e)
                }
    
    def _hash_key(self, key: str) -> str:
        """
        Hash a cache key to ensure it's valid for the filesystem.

        Args:
            key: Original cache key.

        Returns:
            Hashed key.
        """
        return hashlib.md5(key.encode("utf-8")).hexdigest()
    
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and close the cache."""
        self.close()
    
    def close(self):
        """Close the cache."""
        with self._lock:
            try:
                self._cache.close()
            except Exception as e:
                logger.warning(f"Error closing cache: {str(e)}")
