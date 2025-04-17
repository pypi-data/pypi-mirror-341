"""
Dependency class for representing a software dependency.
"""

from typing import Dict, Any, Optional, List


class Dependency:
    """Class representing a software dependency."""

    def __init__(
        self,
        name: str,
        version: str,
        package_type: str,
        license: Optional[str] = None,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        is_direct: bool = True,
        parent: Optional[str] = None,
        purl: Optional[str] = None,
    ):
        """
        Initialize a Dependency.

        Args:
            name: Name of the dependency.
            version: Version of the dependency.
            package_type: Type of package (e.g., "npm", "pypi", "maven").
            license: License of the dependency.
            description: Description of the dependency.
            homepage: Homepage URL of the dependency.
            is_direct: Whether this is a direct dependency or a transitive one.
            parent: Name of the parent dependency if this is a transitive dependency.
            purl: Package URL (purl) if known.
        """
        self.name = name
        self.version = version
        self.package_type = package_type
        self.license = license
        self.description = description
        self.homepage = homepage
        self.is_direct = is_direct
        self.parent = parent
        self.purl = purl or self._generate_purl()
    
    def _generate_purl(self) -> str:
        """
        Generate a Package URL (purl) for this dependency.

        Returns:
            Package URL string.
        """
        # Map of package types to purl types
        type_map = {
            "npm": "npm",
            "pypi": "pypi",
            "maven": "maven",
            "nuget": "nuget",
            "gem": "gem",
            "golang": "golang",
            "composer": "composer",
            "cargo": "cargo",
        }
        
        purl_type = type_map.get(self.package_type.lower(), self.package_type.lower())
        return f"pkg:{purl_type}/{self.name}@{self.version}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the dependency to a dictionary.

        Returns:
            Dictionary representation of the dependency.
        """
        return {
            "name": self.name,
            "version": self.version,
            "package_type": self.package_type,
            "license": self.license,
            "description": self.description,
            "homepage": self.homepage,
            "is_direct": self.is_direct,
            "parent": self.parent,
            "purl": self.purl,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dependency":
        """
        Create a Dependency from a dictionary.

        Args:
            data: Dictionary containing dependency data.

        Returns:
            A new Dependency instance.
        """
        return cls(
            name=data["name"],
            version=data["version"],
            package_type=data["package_type"],
            license=data.get("license"),
            description=data.get("description"),
            homepage=data.get("homepage"),
            is_direct=data.get("is_direct", True),
            parent=data.get("parent"),
            purl=data.get("purl"),
        )
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality of dependencies based on name, version, and type.

        Args:
            other: Another dependency to compare with.

        Returns:
            True if dependencies are equal, False otherwise.
        """
        if not isinstance(other, Dependency):
            return False
        
        return (
            self.name == other.name
            and self.version == other.version
            and self.package_type == other.package_type
        )
    
    def __hash__(self) -> int:
        """
        Generate a hash for the dependency based on name, version, and type.

        Returns:
            Hash value.
        """
        return hash((self.name, self.version, self.package_type))
    
    def __str__(self) -> str:
        """
        Get string representation of the dependency.

        Returns:
            String representation.
        """
        return f"{self.name}@{self.version} ({self.package_type})"
    
    def __repr__(self) -> str:
        """
        Get detailed string representation of the dependency.

        Returns:
            Detailed string representation.
        """
        return (
            f"Dependency(name='{self.name}', version='{self.version}', "
            f"package_type='{self.package_type}', is_direct={self.is_direct})"
        )
