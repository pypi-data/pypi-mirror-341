# llm-yt-transcript

`llm-yt-transcript` is a LLM plugin for YouTube transcripts as fragments. It leverages `yt-dlp` for downloading subtitles.

## Installation

```
llm install git+https://github.com/kj-9/llm-yt-transcript.git
```


## Usage

### Download Subtitles

Use the `download_subtitles` function to download subtitles for a YouTube video:
```python
llm -f ytt:{youtube_video_url} 'summarize the transcript'
```

by default, it will download the English subtitles. You can specify the language using the `lang` parameter before the `:`. 
For example, to download Spanish subtitles, use:
```python
llm fragments show ytt:es:{youtube_video_url}
```


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```
cd llm-yt-transcript
uv sync --all-groups
```

Run the following command to run the tests:
```
uv run pytest
```
