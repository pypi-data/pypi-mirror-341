import pytest
import asyncio
import os
from pathlib import Path
from ytdl_taquitos import Downloader

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path / "downloads"

@pytest.fixture
async def downloader(temp_dir):
    downloader = Downloader(output_dir=temp_dir)
    yield downloader
    await downloader.close()

@pytest.mark.asyncio
async def test_download_file(downloader, temp_dir):
    # Test with a small file
    url = "https://httpbin.org/bytes/1024"  # 1KB file
    filename = "test.bin"
    
    output_path = await downloader.download_file(url, filename)
    
    assert output_path.exists()
    assert output_path.stat().st_size == 1024
    assert output_path.parent == temp_dir

@pytest.mark.asyncio
async def test_download_subtitle(downloader, temp_dir):
    # Test with a small subtitle file
    url = "https://httpbin.org/bytes/512"  # 512B file
    lang = "en"
    video_id = "test123"
    
    output_path = await downloader.download_subtitle(url, lang, video_id)
    
    assert output_path.exists()
    assert output_path.stat().st_size == 512
    assert output_path.parent == temp_dir
    assert output_path.name == f"{video_id}.{lang}.srt"

@pytest.mark.asyncio
async def test_speed_limit(downloader, temp_dir):
    # Test with speed limit
    url = "https://httpbin.org/bytes/2048"  # 2KB file
    filename = "test_speed.bin"
    speed_limit = 1024  # 1KB/s
    
    downloader.speed_limit = speed_limit
    
    import time
    start_time = time.time()
    await downloader.download_file(url, filename)
    end_time = time.time()
    
    # Check if download took at least 2 seconds (2KB at 1KB/s)
    assert end_time - start_time >= 2.0

@pytest.mark.asyncio
async def test_chunk_size(downloader, temp_dir):
    # Test with custom chunk size
    url = "https://httpbin.org/bytes/4096"  # 4KB file
    filename = "test_chunk.bin"
    chunk_size = 512  # 512B chunks
    
    downloader.chunk_size = chunk_size
    output_path = await downloader.download_file(url, filename)
    
    assert output_path.exists()
    assert output_path.stat().st_size == 4096 