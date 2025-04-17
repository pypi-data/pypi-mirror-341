# llm-jina-reader

[![PyPI](https://img.shields.io/pypi/v/llm-jina-reader.svg)](https://pypi.org/project/llm-jina-reader/)
[![Changelog](https://img.shields.io/github/v/release/jefftriplett/llm-jina-reader?include_prereleases&label=changelog)](https://github.com/jefftriplett/llm-jina-reader/releases)
[![Tests](https://github.com/jefftriplett/llm-jina-reader/actions/workflows/test.yml/badge.svg)](https://github.com/jefftriplett/llm-jina-reader/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jefftriplett/llm-jina-reader/blob/main/LICENSE)

LLM plugin for pulling content via Jina Reader API

For background on how this works:

- [Long context support in LLM 0.24 using fragments and template plugins](https://simonwillison.net/2025/Apr/7/long-context-llm/)

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-jina-reader
```

## Configuration

This plugin requires a Jina Reader API token. Set your token as an environment variable:

```bash
export JINA_READER_TOKEN="your-jina-reader-token"
```

## Usage

You can feed a full conversation thread from Jina Reader into LLM using the `jina:` [fragment](https://llm.datasette.io/en/stable/fragments.html) with the URL that you want to prompt against. For example:

```bash
llm --fragment jina:https://simonwillison.net/2025/Apr/7/long-context-llm/ "Please summarize this post in one sentence."
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment or just use `uv`, it's easier:

```bash
cd llm-jina-reader
```

Now install the dependencies and test dependencies:

```bash
uv sync --all-extras
```

To run the tests:

```bash
uv run pytest
```
