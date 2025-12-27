# NovelWriter (日本語)

[[English](README.md)]

NovelWriterは、[Ollama](https://ollama.com/)を使用してローカル環境で動作するAI執筆支援システムです。長編小説（7万〜10万文字）の執筆を、プロット→構成案→執筆というプロセスに分解してサポートします。

## 特徴

- **完全ローカル**: Ollamaを使用するため、APIキーや通信費は不要です。プライバシーも守られます。
- **構造化されたワークフロー**:
    1. **プロット作成**: 起承転結を含む詳細なプロットを生成します。
    2. **世界観・キャラクター設定**: プロットに基づき、登場人物や世界観の設定資料を自動生成します。
    3. **構成案（ハコ書き）作成**: プロットを章・シーンごとに分割したアウトラインを作成します。
    4. **本文執筆**: 直前のシーンの文脈を考慮しながら、シーン単位で本文を執筆します。
- **ファイル管理**: 進捗はすべてJSON/Markdownファイル（`plot.md`, `outline.json`, `drafts/`など）として保存されます。ユーザーはいつでも手動で編集・修正が可能です。
- **日本語出力**: 日本語での執筆に最適化されています。

## 前提条件

- **Python 3.8+**
- **Ollama**: インストールされ、起動していること。
- **Ollama モデル**: 使用するモデルをpullしてください（デフォルトは `gpt-oss:120b`）。
  ```bash
  ollama pull gpt-oss:120b
  ```

## インストール

1. リポジトリをクローンします。
2. 依存ライブラリ（requests）をインストールします:
   ```bash
   pip install requests
   ```

## 使い方

### 1. プロジェクトの初期化
初期アイデアを元に、プロット、キャラクター、世界観を生成します。
```bash
python main.py init --idea "ここに小説のアイデアを入力"
```

### 2. アウトライン生成
プロットに基づいて、章とシーンの構成を作成します。
```bash
python main.py outline
```

### 3. 本文執筆
小説のシーンを執筆します。`--count` オプションで一度に執筆するシーン数を指定できます。
```bash
python main.py write --count 1
```

### 4. 状態の再構築（手動修正の反映）
シーンファイル（例: `drafts/scene_2.md`）を手動で書き換えた場合、このコマンドを使ってそのシーンまでの内部整合性（`state.json`）を再構築してください。
```bash
python main.py reconstruct --scene 2
```

## 設定

`config.py` を編集することで以下の設定を変更できます:
- `DEFAULT_MODEL`: 使用するOllamaのモデル名。
- `OLLAMA_BASE_URL`: OllamaのAPI URL。

## ライセンス

[The MIT license](LICENSE)

Copyright (c) 2025 Kudo Shusak