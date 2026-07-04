# fable-coding

Fable 5のコーディング規律をSkill化し、Sonnet 5などで再現するためのプラグイン。

## インストール

Claude Code内で:

```
/plugin marketplace add Wanyaldee/fable-coding
/plugin install fable-coding@fable-coding
```

## 使い方

インストール後、コーディングタスクで `fable-coding` スキルが自動的に候補になる。明示的に使う場合はプロンプトで「fable-codingスキルを使って」と指示する。

## 収録スキル

- `fable-coding` — Fable 5級のコーディング規律(計画→根本原因→最小差分→検証→ADR)。v1.4.0で公式プロンプティングガイド由来の行動規則(過剰計画の抑制、ツール結果に基づく進捗報告、assessとfixの境界、最終サマリの可読性、途中終了の禁止)を統合。v1.5.0で @armadillo_ai の7則(完了の機械的定義、複数解釈の確認、ついで改善禁止、証拠付き検証報告、修正2回まで、初見セルフレビュー、確信度+3点報告)を統合。
- `prompting-fable-5` (v1.4.0〜) — Fable 5 / Mythos 5 を「使う側」のリファレンス: effort設定、公式スニペット集、サブエージェント/メモリ/send_to_userのスキャフォールディング、refusalフォールバック、旧モデルからのプロンプト移行チェックリスト。Fable 5向けのプロンプト・エージェント・スキルを書くときに発火する。
- `memory-discipline` (v1.6.0〜) — 永続オートメモリの規範: 1ファイル1事実、リポジトリ記録済み内容の保存禁止(ポインタ+差分)、`origin`(モデル+絶対日付)の記録、索引の同ターン更新、矛盾に気づいたセッションでの即時更新/削除。2026-07-04 の全プロジェクトメモリ監査の知見を規範化したもの。
- `dev-philosophy` (v1.3.0〜) — 開発哲学: 自動化の境界線(ヒューマンインザループ、外部信頼サービス優先)、仕組みによるセキュリティ、技術スタック方針(Python/Rust、MariaDB、Proxmox)、MIT License 標準。システム設計・アーキテクチャ提案時に適用される。

英語スキル(`fable-coding`, `prompting-fable-5`)には人間用の和訳 `SKILL.ja.md` を併設している(v1.4.0〜)。Claude が読み込むのは `SKILL.md`(英語版)のみ。編集は英語版に行い、和訳を追随させる。

## 認証情報ファイルの読み取りブロック(v1.2.0〜)

プラグインを有効化すると PreToolUse フックが自動で登録され、Claude が以下のファイルを Read ツールで読むことを拒否する:

- `.env` / `.env.*`
- `*.pem` / `id_rsa` / `id_ed25519`
- `credentials.json` / `.aws/` 配下

制限: このフックがカバーするのは Read ツールのみ。`cat .env` のような Bash 経由の読み取りまで固めたい場合は、settings.json の `permissions.deny` に `Read(**/.env)` 等を併せて設定する(deny ルールは Bash コマンドにも適用される)。

## License

MIT
