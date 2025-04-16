from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class VideoFormat:
    format_id: str
    ext: str
    quality: str
    filesize: Optional[int]
    url: str
    is_audio_only: bool = False
    is_video_only: bool = False
    fps: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    bitrate: Optional[int] = None

@dataclass
class VideoInfo:
    id: str
    title: str
    duration: int
    uploader: str
    uploader_id: str
    upload_date: str
    description: str
    formats: List[VideoFormat]
    thumbnail: str
    webpage_url: str
    subtitles: Dict[str, str]  # lang -> url

class BaseExtractor(ABC):
    """Base class for all platform-specific extractors."""
    
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Validate if the URL is compatible with this platform.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if the URL is valid for this platform
        """
        pass
    
    @abstractmethod
    async def extract_info(self, url: str) -> VideoInfo:
        """Extract information about a video.
        
        Args:
            url: The URL of the video
            
        Returns:
            VideoInfo: Information about the video
        """
        pass
    
    @abstractmethod
    async def get_formats(self, video_id: str) -> List[VideoFormat]:
        """Get available formats for a video.
        
        Args:
            video_id: The ID of the video
            
        Returns:
            List[VideoFormat]: List of available formats
        """
        pass
    
    @abstractmethod
    async def get_subtitles(self, video_id: str) -> Dict[str, str]:
        """Get available subtitles for a video.
        
        Args:
            video_id: The ID of the video
            
        Returns:
            Dict[str, str]: Dictionary mapping language codes to subtitle URLs
        """
        pass 