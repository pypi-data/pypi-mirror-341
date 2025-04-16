# ytdl-taquitos

A modern YouTube and video platform downloader library written in Python.

## Features

- Download videos and audio from YouTube
- Support for multiple video qualities
- Download subtitles in various languages
- Progress tracking with speed limiting
- Modern async/await API
- Type hints for better IDE support

## Installation

```bash
pip install ytdl-taquitos
```

## Usage

### Basic Usage

```python
import asyncio
from ytdl_taquitos import YouTubeExtractor, Downloader

async def main():
    # Initialize extractor and downloader
    extractor = YouTubeExtractor()
    downloader = Downloader(output_dir="./downloads")
    
    try:
        # Get video info
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_info = await extractor.extract_info(video_url)
        
        # Download video
        format = next(f for f in video_info.formats if f.quality == "720p")
        await downloader.download_file(format.url, f"{video_info.id}.{format.ext}")
        
        # Download subtitles
        for lang, url in video_info.subtitles.items():
            await downloader.download_subtitle(url, lang, video_info.id)
            
    finally:
        await downloader.close()

asyncio.run(main())
```

### Advanced Usage

```python
import asyncio
from ytdl_taquitos import YouTubeExtractor, Downloader

async def main():
    extractor = YouTubeExtractor()
    downloader = Downloader(
        output_dir="./downloads",
        speed_limit=1024 * 1024,  # 1MB/s
        chunk_size=512 * 1024,    # 512KB chunks
    )
    
    try:
        # Get video info
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_info = await extractor.extract_info(video_url)
        
        # Print available formats
        for fmt in video_info.formats:
            print(f"Format: {fmt.quality} ({fmt.ext})")
            if fmt.is_audio_only:
                print("  Audio only")
            elif fmt.is_video_only:
                print("  Video only")
            else:
                print("  Combined")
        
        # Download highest quality video
        best_format = max(
            (f for f in video_info.formats if not f.is_audio_only),
            key=lambda f: f.height or 0
        )
        await downloader.download_file(
            best_format.url,
            f"{video_info.id}.{best_format.ext}"
        )
        
    finally:
        await downloader.close()

asyncio.run(main())
```

## Development

### Setup

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 