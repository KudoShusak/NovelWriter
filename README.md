# NovelWriter

NovelWriter is a local AI-assisted novel writing system using [Ollama](https://ollama.com/). It is designed to write long novels (70k-100k characters) by breaking down the process into Plot -> Outline -> Writing.

## Features

- **Local AI**: Runs entirely on your machine using Ollama. No API keys or cloud costs.
- **Structured Workflow**:
    1. **Plot Generation**: Creates a detailed plot with beginning, middle, and end.
    2. **World & Character Building**: Automatically generates detailed character sheets and world settings.
    3. **Outline Construction**: Breaks the plot into chapters and scenes.
    4. **Scene Writing**: Writes the novel scene-by-scene, maintaining context from previous scenes.
- **State Management**: All progress is saved in JSON/Markdown files (`plot.md`, `outline.json`, `drafts/`), allowing for manual editing and intervention at any stage.
- **Multilingual Support**: Currently configured to output in Japanese.

## Prerequisites

- **Python 3.8+**
- **Ollama**: Installed and running.
- **Ollama Model**: Pull your preferred model (default is `gemma2`).
  ```bash
  ollama pull gemma2
  ```

## Installation

1. Clone this repository.
2. Install dependencies (requests):
   ```bash
   pip install requests
   ```

## Usage

### 1. Initialize Project
Generate the initial plot, characters, and world settings.
```bash
python main.py init --idea "Your novel idea here"
```

### 2. Generate Outline
Create a chapter and scene breakdown based on the plot.
```bash
python main.py outline
```

### 3. Write Scenes
Start writing the novel. You can specify how many scenes to write in one go.
```bash
python main.py write --count 1
```

## Configuration

Edit `config.py` to customize:
- `DEFAULT_MODEL`: The Ollama model to use.
- `OLLAMA_BASE_URL`: The API URL for Ollama.

## License

[The MIT license](LICENSE)

Copyright (c) 2025 Kudo Shusak