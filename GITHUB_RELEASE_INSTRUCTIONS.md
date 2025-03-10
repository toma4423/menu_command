# GitHub上でリリースを作成する手順

## 方法1: GitHub Actionsによる自動リリース (推奨)

このリポジトリはGitHub Actionsを使用した自動リリース機能を搭載しています。新しいタグを作成するだけで、ビルドとリリース作成が自動的に行われます。

1. ローカルでタグを作成
   ```bash
   git tag -a v0.1.1 -m "バージョン0.1.1をリリース"
   ```

2. タグをGitHubにプッシュ
   ```bash
   git push origin v0.1.1
   ```

3. 自動プロセスが開始されます
   - GitHub Actionsが起動しビルドが実行される
   - 実行ファイルが作成され、アーカイブ化される
   - RELEASE_NOTES.mdに基づいたリリースが自動作成される
   - ビルドされたアーカイブがリリースに添付される

4. GitHubのリポジトリページで「Actions」タブを確認して進行状況を確認できます

## 方法2: 手動でリリースを作成（旧方法）

### 1. GitHubにコードをプッシュ

以下のコマンドをターミナルで実行してGitHubにプッシュしてください：

```bash
git push -u origin main
git push origin v0.1.0
```

GitHub認証情報の入力を求められたら、ユーザー名とパスワード（またはアクセストークン）を入力してください。

### 2. GitHubでプレリリースを作成

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

## インストール方法（ユーザー向け）

### 方法1: バイナリを使用する場合

1. GitHubのReleaseページから `menu_command-vX.X.X-linux.tar.gz` をダウンロード
2. アーカイブを展開: `tar -xzvf menu_command-vX.X.X-linux.tar.gz`
3. 実行権限を確認: `chmod +x menu_command`
4. アプリケーションを実行: `./menu_command`

### 方法2: ソースコードから実行する場合

1. リポジトリをクローン: `git clone https://github.com/toma4423/menu_command.git`
2. 必要なライブラリをインストール: `sudo apt-get install python3-tk`
3. スクリプトを実行: `python3 launcher.py` 