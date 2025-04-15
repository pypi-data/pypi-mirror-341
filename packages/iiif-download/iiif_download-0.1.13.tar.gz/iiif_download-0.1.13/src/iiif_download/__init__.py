"""
IIIF Downloader
==============

A Python package to download images from IIIF manifests.
"""

from .config import Config, config
from .image import IIIFImage
from .manifest import IIIFManifest

__version__ = "0.1.13"

__all__ = ["IIIFManifest", "IIIFImage", "config", "Config"]
