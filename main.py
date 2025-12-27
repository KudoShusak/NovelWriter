import argparse
import os
import json
from generators import Generator
from state_manager import StateManager
from config import Config

def main():
    parser = argparse.ArgumentParser(description="NovelWriter CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init Command
    parser_init = subparsers.add_parser("init", help="Initialize project and generate plot/world/chars")
    parser_init.add_argument("--idea", type=str, help="Initial idea for the novel", default=None)

    # Outline Command
    parser_outline = subparsers.add_parser("outline", help="Generate or update outline based on plot")

    # Write Command
    parser_write = subparsers.add_parser("write", help="Write the next scene")
    parser_write.add_argument("--count", type=int, default=1, help="Number of scenes to write")

    # Reconstruct Command
    parser_reconstruct = subparsers.add_parser("reconstruct", help="Reconstruct state and summary after manual edit")
    parser_reconstruct.add_argument("--scene", type=int, required=True, help="Target scene ID to reconstruct up to")

    args = parser.parse_args()

    generator = Generator()
    state_manager = StateManager()

    if args.command == "init":
        print("Initializing project...")
        if os.path.exists(Config.PLOT_FILE):
            print("Plot file already exists. Skipping plot generation.")
            plot = state_manager.load_plot()
        else:
            plot = generator.generate_plot(args.idea)
            print("Plot generated.")

        if os.path.exists(Config.CHARACTERS_FILE):
            print("Characters file already exists. Skipping.")
        else:
            generator.generate_characters(plot)
            print("Characters generated.")

        if os.path.exists(Config.WORLD_FILE):
            print("World file already exists. Skipping.")
        else:
            generator.generate_world(plot)
            print("World generated.")
        
        print("Initialization complete. Check the generated files.")

    elif args.command == "outline":
        print("Generating outline...")
        plot = state_manager.load_plot()
        characters = state_manager.load_characters()
        world = state_manager.load_world()
        
        if not plot:
            print("Error: Plot not found. Run 'init' first.")
            return

        outline = generator.generate_outline(plot, characters, world)
        print(f"Outline generated with {len(outline)} chapters.")

    elif args.command == "write":
        print("Starting writing process...")
        outline = state_manager.load_outline()
        characters = state_manager.load_characters()
        world = state_manager.load_world()
        current_state = state_manager.load_state() or {}
        
        if not outline:
            print("Error: Outline not found. Run 'outline' first.")
            return

        scenes_written = 0
        previous_summary = ""
        
        # Find last written scene to get context
        # This is a simplified context retrieval. Ideally we'd have a summary file.
        # For now, let's look for the last generated summary or just use empty if start.
        
        # We need to iterate through chapters and scenes
        for chapter in outline:
            for scene in chapter.get("scenes", []):
                scene_id = scene.get("scene_id")
                scene_file = os.path.join(Config.DRAFTS_DIR, f"scene_{scene_id}.md")
                summary_file = os.path.join(Config.DRAFTS_DIR, f"scene_{scene_id}_summary.txt")
                
                if os.path.exists(scene_file):
                    # Scene exists, load its summary for next context
                    if os.path.exists(summary_file):
                        previous_summary = state_manager.load_text(summary_file)
                    else:
                        # If summary missing, maybe generate it? For now just skip.
                        pass
                    continue
                
                # Scene doesn't exist, write it
                if scenes_written >= args.count:
                    print(f"Reached limit of {args.count} scenes. Stopping.")
                    return

                print(f"Writing Chapter {chapter.get('chapter_title')}, Scene {scene_id}...")
                scene_text = generator.write_scene(scene, previous_summary, characters, world, current_state)
                
                # Generate Title
                print("Generating title...")
                title = generator.generate_title(scene_text)
                final_content = f"# {title}\n\n{scene_text}"

                # Save scene
                state_manager.save_text(scene_file, final_content)

                # Update state based on the new scene
                print(f"Updating state for Scene {scene_id}...")
                current_state = generator.update_state(scene_text, current_state, characters)
                state_manager.save_state(current_state)
                state_manager.save_state_snapshot(current_state, scene_id)
                
                # Generate and save summary
                print("Summarizing scene...")
                summary = generator.summarize_scene(scene_text)
                state_manager.save_text(summary_file, summary)
                
                previous_summary = summary
                scenes_written += 1
                print(f"Scene {scene_id} written and saved.")

        if scenes_written == 0:
            print("All scenes in the outline appear to be written already.")

    elif args.command == "reconstruct":
        target_scene_id = args.scene
        print(f"Reconstructing state up to Scene {target_scene_id}...")
        
        characters = state_manager.load_characters()
        
        # Reconstruct State
        new_state = generator.reconstruct_state(target_scene_id, characters)
        state_manager.save_state(new_state)
        print("State reconstruction complete.")
        
        # Regenerate Summary for target scene
        scene_file = os.path.join(Config.DRAFTS_DIR, f"scene_{target_scene_id}.md")
        summary_file = os.path.join(Config.DRAFTS_DIR, f"scene_{target_scene_id}_summary.txt")
        
        if os.path.exists(scene_file):
            print(f"Regenerating summary for Scene {target_scene_id}...")
            scene_text = state_manager.load_text(scene_file)
            summary = generator.summarize_scene(scene_text)
            state_manager.save_text(summary_file, summary)
            print("Summary regeneration complete.")
        else:
            print(f"Scene {target_scene_id} file not found. Skipping summary regeneration.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
