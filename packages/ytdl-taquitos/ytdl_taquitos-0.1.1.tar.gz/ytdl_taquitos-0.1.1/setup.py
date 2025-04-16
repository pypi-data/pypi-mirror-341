from setuptools import setup, find_namespace_packages

# Leer el contenido del README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ytdl-taquitos",
    version="0.1.1",
    description="A modern YouTube and video platform downloader library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="JuandeMx",
    author_email="jgjuande.mx@gmail.com",
    url="https://github.com/JuandeMx/ytdl-taquitos",
    packages=find_namespace_packages(include=["ytdl_taquitos", "ytdl_taquitos.*"]),
    package_data={
        "ytdl_taquitos": ["extractor/*.py"],
    },
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.8.0",
        "tqdm>=4.65.0",
        "ffmpeg-python>=0.2.0",
        "beautifulsoup4>=4.12.0",
        "mutagen>=1.46.0",
        "yt-dlp>=2024.3.10",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=22.3.0',
            'isort>=5.10.1',
            'flake8>=4.0.1',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="youtube downloader video audio async",
    project_urls={
        "Bug Reports": "https://github.com/JuandeMx/ytdl-taquitos/issues",
        "Source": "https://github.com/JuandeMx/ytdl-taquitos",
        "Documentation": "https://github.com/JuandeMx/ytdl-taquitos#readme",
    },
) 