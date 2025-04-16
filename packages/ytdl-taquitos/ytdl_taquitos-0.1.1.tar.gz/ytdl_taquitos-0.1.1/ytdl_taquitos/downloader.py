import asyncio
import os
from pathlib import Path
from typing import Optional, Union
import aiohttp
from tqdm import tqdm

class Downloader:
    """Handles downloading of video and audio files."""
    
    def __init__(
        self,
        output_dir: Union[str, Path] = "./downloads",
        speed_limit: Optional[float] = None,
        chunk_size: int = 1024 * 1024,  # 1MB chunks
    ):
        """Initialize the downloader.
        
        Args:
            output_dir: Directory where files will be saved
            speed_limit: Download speed limit in bytes per second
            chunk_size: Size of chunks to download at a time
        """
        self.output_dir = Path(output_dir)
        self.speed_limit = speed_limit
        self.chunk_size = chunk_size
        self._session = None
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def download_file(
        self,
        url: str,
        filename: str,
        headers: Optional[dict] = None,
    ) -> Path:
        """Download a file with progress tracking.
        
        Args:
            url: URL of the file to download
            filename: Name to save the file as
            headers: Optional HTTP headers
            
        Returns:
            Path: Path to the downloaded file
        """
        session = await self._get_session()
        output_path = self.output_dir / filename
        
        # Get file size if available
        async with session.head(url, headers=headers) as response:
            total_size = int(response.headers.get("content-length", 0))
        
        # Download file with progress bar
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise ValueError(f"Failed to download file: {response.status}")
            
            with open(output_path, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=filename,
            ) as pbar:
                async for chunk in response.content.iter_chunked(self.chunk_size):
                    f.write(chunk)
                    pbar.update(len(chunk))
                    
                    # Apply speed limit if specified
                    if self.speed_limit:
                        await asyncio.sleep(len(chunk) / self.speed_limit)
        
        return output_path
    
    async def download_subtitle(
        self,
        url: str,
        lang: str,
        video_id: str,
    ) -> Path:
        """Download a subtitle file.
        
        Args:
            url: URL of the subtitle file
            lang: Language code of the subtitle
            video_id: ID of the video
            
        Returns:
            Path: Path to the downloaded subtitle file
        """
        filename = f"{video_id}.{lang}.srt"
        return await self.download_file(url, filename)
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None 