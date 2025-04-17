# GJMeta

A digital human generation service based on FastMCP.

## Installation

```bash
pip install gj_meta_mcp
```

## Configuration

The service can be configured either through environment variables or a config file:

### Environment Variables

```bash
export APP_ID=your_app_id
export SECRET_KEY=your_secret_key
export AUTHORIZE_URL=your_authorize_url
export AUTHORIZE_TEXT=your_authorize_text
```

### Config File

Create a `config.py` file with the following content:

```python
app_id = "your_app_id"
secret_key = "your_secret_key"
authorize_url = "your_authorize_url"
authorize_text = "your_authorize_text"
```

## Usage

```python
from gj_meta_mcp import create_meta_human

# Create a digital human video
result = await create_meta_human(
    video_url="https://example.com/video.mp4",
    audio_url="https://example.com/audio.wav"
)
```

## Features

- Create digital human videos from existing video and audio
- Support for MP4 video format
- Support for WAV audio format
- Environment variable and config file support
- Logging and error handling

## License

MIT License
