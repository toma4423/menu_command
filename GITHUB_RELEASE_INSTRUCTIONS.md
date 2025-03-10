# GitHub上でリリースを作成する手順

## 1. GitHubにコードをプッシュ

以下のコマンドをターミナルで実行してGitHubにプッシュしてください：

```bash
git push -u origin main
git push origin v0.1.0
```

GitHub認証情報の入力を求められたら、ユーザー名とパスワード（またはアクセストークン）を入力してください。

## 2. GitHubでプレリリースを作成

1. GitHubにログイン後、リポジトリ（https://github.com/toma4423/menu_command）にアクセス
2. 「Releases」タブをクリック
3. 「Draft a new release」または「Create a new release」ボタンをクリック
4. 以下の情報を入力：
   - タグ: v0.1.0 (既存のタグを選択)
   - リリースタイトル: v0.1.0 初期リリース
   - 説明: RELEASE_NOTES.mdの内容をコピー
5. 「This is a pre-release」チェックボックスをオン
6. ビルドした「dist/menu_command-v0.1.0-linux.tar.gz」ファイルをドラッグ＆ドロップでアップロード
7. 「Publish release」ボタンをクリックしてリリースを公開

これでv0.1.0のプレリリースが完了します。

## 3. インストール方法（ユーザー向け）

### 方法1: バイナリを使用する場合

1. GitHubのReleaseページから `menu_command-v0.1.0-linux.tar.gz` をダウンロード
2. アーカイブを展開: `tar -xzvf menu_command-v0.1.0-linux.tar.gz`
3. 実行権限を確認: `chmod +x menu_command`
4. アプリケーションを実行: `./menu_command`

### 方法2: ソースコードから実行する場合

1. リポジトリをクローン: `git clone https://github.com/toma4423/menu_command.git`
2. 必要なライブラリをインストール: `sudo apt-get install python3-tk`
3. スクリプトを実行: `python3 launcher.py` 