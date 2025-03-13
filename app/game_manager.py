import os
import json
import uuid
from datetime import datetime

class GameManager:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.games = []
        self.load_games()

    def load_games(self):
        """載入現有的 JSON 檔案"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        for filename in os.listdir(self.data_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(self.data_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    game = json.load(f)
                    self.games.append(game)

    def get_games(self):
        return self.games

    def create_game(self, data):
        """新增一個遊戲"""
        game_id = str(uuid.uuid4())
        game = {
            'id': game_id,
            'world_name': data.get('world_name', 'Untitled Game'),
            'world_genre': data.get('world_genre', ''),
            'world_detail': data.get('world_detail', ''),
            'npcs': data.get('npcs', []),
            'scene_prologue': data.get('scene_prologue', {}),
            'scene_opening_line': data.get('scene_opening_line', {}),
            'scene_goal': data.get('scene_goal', {}),
            'scene_fail_when': data.get('scene_fail_when', {}),
            'scene_ending_line': data.get('scene_ending_line', {}),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 儲存到記憶體
        self.games.append(game)

        # 寫入 JSON 檔案
        file_path = os.path.join(self.data_folder, f'{game_id}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(game, f, ensure_ascii=False, indent=4)

        return game

    def delete_game(self, game_id):
        """刪除一個遊戲"""
        game = next((g for g in self.games if g['id'] == game_id), None)
        if not game:
            return False

        self.games = [g for g in self.games if g['id'] != game_id]

        file_path = os.path.join(self.data_folder, f'{game_id}.json')
        if os.path.exists(file_path):
            os.remove(file_path)

        return True

    def get_game_by_id(self, game_id):
        return next((g for g in self.games if g['id'] == game_id), None)

    def edit_game(self, game_id, data):
        """編輯遊戲"""
        game = self.get_game_by_id(game_id)
        if not game:
            return None

        # 更新遊戲內容
        game['world_name'] = data.get('world_name', game['world_name'])
        game['world_genre'] = data.get('world_genre', game['world_genre'])
        game['world_detail'] = data.get('world_detail', game['world_detail'])
        game['npcs'] = data.get('npcs', game['npcs'])
        game['scene_prologue'] = data.get('scene_prologue', game['scene_prologue'])
        game['scene_opening_line'] = data.get('scene_opening_line', game['scene_opening_line'])
        game['scene_goal'] = data.get('scene_goal', game['scene_goal'])
        game['scene_fail_when'] = data.get('scene_fail_when', game['scene_fail_when'])
        game['scene_ending_line'] = data.get('scene_ending_line', game['scene_ending_line'])

        # 寫入 JSON 檔案
        file_path = os.path.join(self.data_folder, f'{game_id}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(game, f, ensure_ascii=False, indent=4)

        return game