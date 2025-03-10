# GitHub Actionsによる自動リリース機能が追加されました

これで自動リリース機能の設定が完了しました。GitHubに以下のコマンドを実行してプッシュしてください：

```
git push -u origin main
```

その後、初期リリースを自動作成するため、v0.1.0タグもプッシュします：

```
git push origin v0.1.0
```

アクションが実行されたら、GitHubのリポジトリページの「Actions」タブで進行状況を確認できます。
正常に完了すると、「Releases」ページに自動的にリリースが作成されています。

## 今後の運用方法

今後は新しいバージョンをリリースする場合、以下の手順だけで済みます：

1. コードを変更してコミット
2. 新しいタグを作成（例: `git tag -a v0.1.1 -m "バージョン0.1.1"`）
3. タグをプッシュ（`git push origin v0.1.1`）

GitHub Actionsが自動的にビルドとリリース作成を行います。

## トラブルシューティング

Actionsが失敗した場合は以下を確認してください：

1. リポジトリの「Settings」→「Actions」→「General」で、Workflows permissions が適切に設定されていることを確認
   - 「Read and write permissions」が推奨設定です
   
2. リポジトリのシークレット設定
   - 特別な認証が必要な場合は「Settings」→「Secrets and variables」→「Actions」で設定できます 