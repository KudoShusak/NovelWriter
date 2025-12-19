# Changelog

All notable changes to the NovelWriter project will be documented in this file.

## v0.00.1 - 2025-12-19

### Added (Quality Improvements)
- **State Management System**:
    - Implemented `state.json` to track character locations, status, inventory, and cumulative experience logs across scenes.
    - Added `update_state` method to dynamically update the world state after each scene.
- **Character Consistency Enhancements**:
    - Expanded `characters.json` schema to include `first_person` (一人称), `second_person` (二人称), and `speech_examples` (セリフ例).
    - Updated writing prompts to strictly enforce character speech patterns and behaviors defined in the profile.
- **Narrative Viewpoint Enforcement**:
    - Added `NOVEL_VIEWPOINT` in `config.py` (Default: "Third Person Omniscient").
    - Updated prompts to prevent unintended point-of-view switching within scenes.
- **Comprehensive Character Extraction**:
    - Updated character generation logic to ensure names are invented for all relevant figures, including those appearing only in flashbacks or mentions (e.g., "father", "old master").
- **Automatic Scene Titling**:
    - Added functionality to generate a catchy title for each scene after it is written and prepend it to the markdown file.

### Changed
- **Project Structure**:
    - Generated files (`drafts/`, `characters.json`, `plot.md`, etc.) are now stored in a `writing/` subdirectory to keep the root clean. (Configured in `config.py`)
- **Prompts**:
    - Refined all prompts in `generators.py` to produce higher quality Japanese output and adhere to strict formatting rules.
