import pytest
import asyncio
from ytdl_taquitos import YouTubeExtractor

@pytest.mark.asyncio
async def test_validate_url():
    extractor = YouTubeExtractor()
    
    # Valid URLs
    assert extractor.validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert extractor.validate_url("https://youtu.be/dQw4w9WgXcQ")
    assert extractor.validate_url("https://www.youtube.com/playlist?list=PL1234567890")
    
    # Invalid URLs
    assert not extractor.validate_url("https://www.google.com")
    assert not extractor.validate_url("https://www.youtube.com")
    assert not extractor.validate_url("https://www.youtube.com/user/username")

@pytest.mark.asyncio
async def test_extract_info():
    extractor = YouTubeExtractor()
    
    # Test with a known video
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_info = await extractor.extract_info(video_url)
    
    # Check basic info
    assert video_info.id == "dQw4w9WgXcQ"
    assert video_info.title
    assert video_info.duration > 0
    assert video_info.uploader
    assert video_info.uploader_id
    assert video_info.description is not None
    assert video_info.thumbnail
    assert video_info.webpage_url == video_url
    
    # Check formats
    assert video_info.formats
    for fmt in video_info.formats:
        assert fmt.format_id
        assert fmt.ext
        assert fmt.quality
        assert fmt.url
    
    # Check subtitles
    assert isinstance(video_info.subtitles, dict)

@pytest.mark.asyncio
async def test_get_formats():
    extractor = YouTubeExtractor()
    video_id = "dQw4w9WgXcQ"
    
    formats = await extractor.get_formats(video_id)
    assert formats
    
    # Check format properties
    for fmt in formats:
        assert fmt.format_id
        assert fmt.ext
        assert fmt.quality
        assert fmt.url
        assert isinstance(fmt.is_audio_only, bool)
        assert isinstance(fmt.is_video_only, bool)
        if fmt.fps:
            assert isinstance(fmt.fps, int)
        if fmt.width:
            assert isinstance(fmt.width, int)
        if fmt.height:
            assert isinstance(fmt.height, int)
        if fmt.bitrate:
            assert isinstance(fmt.bitrate, int)

@pytest.mark.asyncio
async def test_get_subtitles():
    extractor = YouTubeExtractor()
    video_id = "dQw4w9WgXcQ"
    
    subtitles = await extractor.get_subtitles(video_id)
    assert isinstance(subtitles, dict)
    
    # Check subtitle URLs
    for lang, url in subtitles.items():
        assert isinstance(lang, str)
        assert isinstance(url, str)
        assert url.startswith("https://www.youtube.com/api/timedtext") 