"""
Tests for caching.
"""

import os
import time
import unittest
import tempfile
from pathlib import Path

from ossv_scanner.caching.cache import Cache


class TestCache(unittest.TestCase):
    """Test cases for cache."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for cache
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir = self.temp_dir.name
        
        # Create cache
        self.cache = Cache(
            cache_dir=self.cache_dir,
            ttl=1,  # Short TTL for testing
            max_size=10_000_000  # 10 MB
        )
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Close cache
        self.cache.close()
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_cache_set_get(self):
        """Test setting and getting values from the cache."""
        # Set value
        key = "test_key"
        value = {"test": "value"}
        self.cache.set(key, value)
        
        # Get value
        cached_value = self.cache.get(key)
        
        # Check that the value was retrieved correctly
        self.assertEqual(cached_value, value)
    
    def test_cache_expiration(self):
        """Test that values expire after TTL."""
        # Set value with TTL of 1 second
        key = "expiring_key"
        value = {"test": "value"}
        self.cache.set(key, value)
        
        # Get value before expiration
        cached_value = self.cache.get(key)
        self.assertEqual(cached_value, value)
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Get value after expiration
        cached_value = self.cache.get(key)
        self.assertIsNone(cached_value)
    
    def test_cache_delete(self):
        """Test deleting values from the cache."""
        # Set value
        key = "delete_key"
        value = {"test": "value"}
        self.cache.set(key, value)
        
        # Delete value
        self.cache.delete(key)
        
        # Get value after deletion
        cached_value = self.cache.get(key)
        self.assertIsNone(cached_value)
    
    def test_cache_clear(self):
        """Test clearing the entire cache."""
        # Set multiple values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        # Clear cache
        self.cache.clear()
        
        # Get values after clearing
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
    
    def test_cache_stats(self):
        """Test cache statistics."""
        # Set and get values to generate statistics
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("nonexistent")  # Miss
        
        # Get statistics
        stats = self.cache.get_stats()
        
        # Check statistics
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["sets"], 1)
        self.assertEqual(stats["hit_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
