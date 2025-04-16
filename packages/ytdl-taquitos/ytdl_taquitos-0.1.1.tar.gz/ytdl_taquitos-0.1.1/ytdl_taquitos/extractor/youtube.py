from ytdl_taquitos.extractor.base_extractor import BaseExtractor
import yt_dlp
import asyncio
from typing import Dict, List, Optional, Any
import os

class YouTubeExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self._ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        self._ydl = yt_dlp.YoutubeDL(self._ydl_opts)

    @staticmethod
    def validate_url(url: str) -> bool:
        extractors = yt_dlp.extractor.gen_extractors()
        for e in extractors:
            if e.suitable(url) and e.IE_NAME == 'youtube':
                return True
        return False

    async def extract_info(self, url: str) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, self._ydl.extract_info, url, False)
        
        if not info:
            raise ValueError("Could not extract video info")
        
        formats = []
        for f in info.get('formats', []):
            format_info = {
                'format_id': f.get('format_id', ''),
                'url': f.get('url', ''),
                'ext': f.get('ext', ''),
                'filesize': f.get('filesize', 0),
                'tbr': f.get('tbr', 0),
                'protocol': f.get('protocol', ''),
                'vcodec': f.get('vcodec', 'none'),
                'acodec': f.get('acodec', 'none'),
            }
            formats.append(format_info)

        return {
            'id': info.get('id', ''),
            'title': info.get('title', ''),
            'description': info.get('description', ''),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'formats': formats,
            'subtitles': info.get('subtitles', {}),
        }

    async def get_formats(self, url: str) -> List[Dict[str, Any]]:
        info = await self.extract_info(url)
        return info.get('formats', [])

    async def get_subtitles(self, url: str) -> Dict[str, List[Dict[str, str]]]:
        info = await self.extract_info(url)
        return info.get('subtitles', {})

    async def download(self, url: str, output_dir: str = "./descargas", format_id: Optional[str] = None) -> str:
        """Descarga un video de YouTube.
        
        Args:
            url: URL del video
            output_dir: Directorio donde se guardará el video
            format_id: ID del formato específico a descargar (opcional)
            
        Returns:
            str: Ruta al archivo descargado
        """
        os.makedirs(output_dir, exist_ok=True)
        
        ydl_opts = {
            'format': format_id if format_id else 'best',
            'outtmpl': os.path.join(output_dir, '%(id)s_%(format_id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, ydl.extract_info, url)
            filename = ydl.prepare_filename(info)
            return filename

    async def close(self):
        pass  # No need to close anything as yt-dlp handles its own resources 