"""A modern YouTube and video platform downloader library."""

__version__ = "0.1.0"

from .extractor.youtube import YouTubeExtractor
from .downloader import Downloader

__all__ = ["YouTubeExtractor", "Downloader"] 