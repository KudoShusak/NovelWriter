import os

class Config:
    # Ollama Settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "gemma2" # User can change this
    
    # Project Paths
    BASE_DIR = os.getcwd()
    CHARACTERS_FILE = os.path.join(BASE_DIR, "characters.json")
    WORLD_FILE = os.path.join(BASE_DIR, "world.json")
    PLOT_FILE = os.path.join(BASE_DIR, "plot.md")
    OUTLINE_FILE = os.path.join(BASE_DIR, "outline.json")
    DRAFTS_DIR = os.path.join(BASE_DIR, "drafts")
    STATE_FILE = os.path.join(BASE_DIR, "state.json")

    # Generation Settings
    MAX_CONTEXT_CHARS = 4000
