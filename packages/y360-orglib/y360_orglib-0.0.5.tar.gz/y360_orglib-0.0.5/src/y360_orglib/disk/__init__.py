"""
Disk Client module for interacting with the Y360 Disk.
"""

__version__ = "0.1.0"

from y360_orglib.disk.disk_client import DiskClient
from y360_orglib.disk.models import PublicResourcesList, Resource

__all__ = ["DiskClient", "PublicResourcesList", "Resource"]