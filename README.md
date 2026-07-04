# fable-coding

Fable 5のコーディング規律をSkill化し、Sonnet 5などで再現するためのプラグイン。

## インストール

Claude Code内で:

```
/plugin marketplace add Wanyaldee/fable-coding
/plugin install fable-coding@fable-coding
```

Privateリポジトリのため、`gh auth login` 済み(または git の GitHub 認証設定済み)の環境が必要。

## 使い方

インストール後、コーディングタスクで `fable-coding` スキルが自動的に候補になる。明示的に使う場合はプロンプトで「fable-codingスキルを使って」と指示する。
