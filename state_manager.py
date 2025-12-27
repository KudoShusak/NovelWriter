import json
import os
from config import Config

class StateManager:
    def __init__(self):
        self._ensure_directories()

    def _ensure_directories(self):
        if not os.path.exists(Config.DRAFTS_DIR):
            os.makedirs(Config.DRAFTS_DIR)

    def save_json(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_json(self, filepath):
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_text(self, filepath, text):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

    def load_text(self, filepath):
        if not os.path.exists(filepath):
            return ""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    # Specific Loaders/Savers
    def save_characters(self, characters):
        self.save_json(Config.CHARACTERS_FILE, characters)

    def load_characters(self):
        return self.load_json(Config.CHARACTERS_FILE)

    def save_world(self, world):
        self.save_json(Config.WORLD_FILE, world)

    def load_world(self):
        return self.load_json(Config.WORLD_FILE)

    def save_plot(self, plot_text):
        self.save_text(Config.PLOT_FILE, plot_text)

    def load_plot(self):
        return self.load_text(Config.PLOT_FILE)

    def save_outline(self, outline):
        self.save_json(Config.OUTLINE_FILE, outline)

    def load_outline(self):
        return self.load_json(Config.OUTLINE_FILE)
    
    def save_state(self, state):
        self.save_json(Config.STATE_FILE, state)

    def save_state_snapshot(self, state, scene_id):
        filename = f"state_{scene_id}.json"
        self.save_json(os.path.join(Config.DRAFTS_DIR, filename), state)

    def load_state_snapshot(self, scene_id):
        filename = f"state_{scene_id}.json"
        path = os.path.join(Config.DRAFTS_DIR, filename)
        if os.path.exists(path):
            return self.load_json(path)
        return None

    def load_state(self):
        return self.load_json(Config.STATE_FILE)
