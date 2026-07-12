# 0009: 危険な Bash コマンドを拒否する(シークレット読み取り・rm -rf・DB直接操作)

(English: [0009-bash-deny-hook.md](../en/0009-bash-deny-hook.md))

## Context(背景)

ADR 0001 は deny フックの対象を意図的に Read ツールに限定し、Bash 側のカバーは settings の `permissions.deny` ルールに委ねていた。ユーザーは今回、Bash 側もプラグイン自体で封じることを求めた — `cat .env` 型のシークレット読み取り、`rm -rf` のような破壊的コマンド、そして DB の直接操作である。これにより保護がプラグインと一緒に配布され、fable-coding セクション4(DB操作は実行せずユーザーに報告する)がスキルの文面ではなく仕組みで強制される。

## Decision(決定)

`hooks/hooks.json` に第二の `PreToolUse` フック(matcher: `Bash`)として `hooks/deny-bash.py` を追加した。次の順で deny する:

1. **`.env` への言及** — コマンドテキスト中の `.env`/`.env.*` トークン。ただしテンプレート接尾辞 `.example`/`.sample`/`.template` は除外(ADR 0008 と同一ポリシー)。
2. **破壊的コマンド** — recursive と force の両フラグを持つ `rm`(短形・長形・結合形・`sudo` 前置・`xargs`/`find -exec` 経由)、`mkfs*` 全般、`of=/dev/*` へ書き込む `dd`。
3. **DB直接操作** — パイプラインセグメント先頭の `mysql`、`mariadb`、`psql`、`sqlite3`、`mongosh`、`mongo`、`redis-cli`、および `wrangler d1 execute` / `wrangler d1 migrations apply`。deny 理由の文面で、実行するステートメントをユーザーに報告するよう Claude に指示する(fable-coding セクション4)。

ask ではなく deny としたのは、シェル文字列から書き込みか読み取りかを確実に判定できないため。承認されたコマンドはユーザー自身が実行する(例: `!` プレフィックス)。バージョンを 2.2.0 に上げた。

## Alternatives rejected(却下した代替案)

- **DB コマンドに `permissionDecision: "ask"`** — SELECT デバッグがワンクリックで通る利点はあるが、ユーザーの要望は「禁止」であり、deny なら実行ループに人間が完全に残る。dev-philosophy の自動化境界とも一致する。
- **危険なターゲット(`/`、`~`、glob)への `rm -rf` だけブロック** — シェル文字列のターゲット分類は壊れやすい。フラグの組み合わせでのブロックは予測可能。`-f` なしの `rm -r` は正当なクリーンアップ用に残る。
- **`mysqldump` / `wrangler d1 export` のブロック** — バックアップは読み取り専用かつ可逆。ブロックはデータを守らず摩擦だけ増やす。
- **環境変数ダンプ(`printenv`、`env`)** — 対象外。ユーザーの言う「env関係」は `.env` ファイルを指し、環境変数は Claude が実行するどのスクリプトからも既に見える。

## Consequences(帰結)

- `cat .env`、`rm -rf`(テストした全表記)、`mkfs`、`dd of=/dev/…`、DB クライアント起動が、代替手段を Claude に伝える理由付きで deny される。35ケースのパイプテスト行列(allow 側・deny 側)で検証済み。
- 既知の過剰ブロック(許容): コマンドテキストからは読み書きを区別できないため、`cp .env.example .env`(ブートストラップ)や `echo … > .env`(書き込み)も deny される。`rm -rf node_modules` もユーザーの手が必要になる。既知の過小ブロック(許容): これは事故防止のガードであり敵対的境界ではない — ファイルを消したり DB を開く Python スクリプトは通る(スクリプト内の `ponytail:` コメントに上限を明記)。
- パターンマッチする DB クライアントはユーザーのスタック(MariaDB/SQLite/D1)+一般的なものをカバー。新しいクライアントは正規表現への追加が必要。
- `hooks.json` のフック登録はセッション開始時に読み込まれる — 既存セッションで有効化するには `/reload-plugins` か再起動が必要(登録後はスクリプト自体は毎回読み直される)。
