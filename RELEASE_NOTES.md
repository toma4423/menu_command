# リリースノート

## v0.1.0 (初期リリース)

### 追加された機能
- sudoコマンドをGUIから実行する基本機能
- コマンド実行用ボタンのカスタマイズ（追加・編集・削除）
- 設定のJSON形式での保存
- 別ターミナルでのコマンド実行
- スクロール可能なボタンリスト

### システム要件
- OS: Lubuntu（その他のLinuxディストリビューションでも動作可能）
- Python 3.6以上（バイナリ版は不要）
- Tkinter（GUI用、バイナリ版は不要）

### インストール方法
#### 方法1: 実行ファイルを使用する場合
1. GitHubからリリースされた`menu_command`実行ファイルをダウンロード
2. 実行権限を付与: `chmod +x menu_command`
3. 実行: `./menu_command`

#### 方法2: Pythonスクリプトを使用する場合
1. リポジトリをクローン: `git clone https://github.com/toma4423/menu_command.git`
2. 必要ライブラリをインストール: `sudo apt-get install python3-tk`
3. スクリプトを実行: `python3 launcher.py`

### 注意事項
- コマンドはsudo権限で実行されるため、セキュリティに注意してください
- 初期設定ファイル（config.json）にはサンプルコマンドが含まれています 