import json
from llm_client import LLMClient
from state_manager import StateManager

class Generator:
    def __init__(self):
        self.client = LLMClient()
        self.state_manager = StateManager()

    def generate_plot(self, idea=None):
        prompt = "7万文字から10万文字程度の長編小説のプロットを詳細に作成してください。"
        if idea:
            prompt += f"\n初期のアイデア: {idea}"
        prompt += "\n起承転結を含め、物語の始まり、中間、結末を記述してください。主要な対立と解決についても記述してください。出力はすべて日本語で行ってください。"
        
        print("Generating plot...")
        plot = self.client.generate_text(prompt)
        self.state_manager.save_plot(plot)
        return plot

    def generate_characters(self, plot):
        prompt = f"""
        以下のプロットに基づいて、登場人物のリストをJSON形式で作成してください。
        各キャラクターには、name（名前）, age（年齢）, role（役割）, personality（性格）, speech_style（口調）を含めてください。
        
        プロット:
        {plot}
        
        JSONのみを出力してください。フォーマット:
        [
            {{
                "name": "名前",
                "age": "年齢",
                "role": "役割",
                "personality": "性格",
                "speech_style": "口調"
            }}
        ]
        全ての値は日本語で記述してください。
        """
        print("Generating characters...")
        response = self.client.generate_text(prompt)
        # Basic cleanup to ensure valid JSON if the model adds markdown code blocks
        response = self._clean_json_response(response)
        try:
            characters = json.loads(response)
            self.state_manager.save_characters(characters)
            return characters
        except json.JSONDecodeError:
            print("Failed to parse characters JSON. Saving raw response.")
            self.state_manager.save_text("characters_raw.txt", response)
            return []

    def generate_world(self, plot):
        prompt = f"""
        以下のプロットに基づいて、世界観の設定をJSON形式で作成してください。
        location_names（地名リスト）, history（歴史）, magic_system（魔法や技術体系、もしあれば）, important_rules（重要なルール）を含めてください。
        
        プロット:
        {plot}
        
        JSONのみを出力してください。フォーマット:
        {{
            "location_names": ["地名1", "地名2"],
            "history": "歴史の概要...",
            "magic_system": "説明...",
            "important_rules": "ルール..."
        }}
        全ての値は日本語で記述してください。
        """
        print("Generating world settings...")
        response = self.client.generate_text(prompt)
        response = self._clean_json_response(response)
        try:
            world = json.loads(response)
            self.state_manager.save_world(world)
            return world
        except json.JSONDecodeError:
            print("Failed to parse world JSON. Saving raw response.")
            self.state_manager.save_text("world_raw.txt", response)
            return {}

    def generate_outline(self, plot, characters, world):
        prompt = f"""
        プロット、キャラクター、世界観に基づいて、小説の詳細な章とシーンの構成（アウトライン）を作成してください。
        長編小説なので、少なくとも10章以上を目指してください。
        
        プロット: {plot[:1000]}... (省略)
        
        JSONのみを出力してください。フォーマット:
        [
            {{
                "chapter_title": "第1章のタイトル",
                "scenes": [
                    {{
                        "scene_id": 1,
                        "summary": "シーンの要約...",
                        "characters_involved": ["キャラ1", "キャラ2"],
                        "location": "場所"
                    }}
                ]
            }}
        ]
        全ての値は日本語で記述してください。
        """
        print("Generating outline...")
        response = self.client.generate_text(prompt)
        response = self._clean_json_response(response)
        try:
            outline = json.loads(response)
            
            # Post-process to ensure unique scene_ids
            current_scene_id = 1
            for chapter in outline:
                if "scenes" in chapter:
                    for scene in chapter["scenes"]:
                        scene["scene_id"] = current_scene_id
                        current_scene_id += 1
            
            self.state_manager.save_outline(outline)
            return outline
        except json.JSONDecodeError:
            print("Failed to parse outline JSON. Saving raw response.")
            self.state_manager.save_text("outline_raw.txt", response)
            return []

    def write_scene(self, scene_info, previous_summary, characters, world):
        prompt = f"""
        小説のシーンを執筆してください。
        
        シーン要約: {scene_info['summary']}
        場所: {scene_info['location']}
        登場人物: {', '.join(scene_info['characters_involved'])}
        
        直前のコンテキスト: {previous_summary}
        
        世界観情報: {json.dumps(world, ensure_ascii=False)}
        キャラクター詳細: {json.dumps(characters, ensure_ascii=False)}
        
        物語調で、描写豊かに日本語で執筆してください。
        """
        print(f"Writing scene {scene_info.get('scene_id')}...")
        return self.client.generate_text(prompt)

    def summarize_scene(self, scene_text):
        prompt = f"""
        以下のシーンを3〜4文で要約してください。重要な出来事とキャラクターの状態変化に焦点を当ててください。
        出力は日本語で行ってください。
        
        シーン:
        {scene_text}
        """
        return self.client.generate_text(prompt)

    def _clean_json_response(self, response):
        # Remove markdown code blocks if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        return response.strip()
