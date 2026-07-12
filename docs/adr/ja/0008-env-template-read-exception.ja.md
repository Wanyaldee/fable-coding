# 0008: deny フックで .env テンプレートファイルの読み取りを許可する

(English: [0008-env-template-read-exception.md](../en/0008-env-template-read-exception.md))

## Context(背景)

ADR 0001 の deny フックは `.env` と `.env.*` を一律ブロックしており、`.env.example` などの慣習上シークレットの*名前*だけを持ち値を含まないテンプレートファイルまで封じていた。その結果、Claude はプロジェクトにどのシークレットが必要かを知る手段を失い、テンプレートを読む代わりに設定を推測するしかなくなっていた。同じ過剰ブロックはユーザーの `~/.claude/settings.json` にも `Read(**/.env.*)` deny ルールとして二重に存在していた。deny ルールは allow ルールに常に優先するため、settings 側で allow を足しても例外は作れない — ルール自体を除去する必要があった。

## Decision(決定)

`hooks/deny-secrets.py` に早期リターンを追加した: ベース名が `.env` で始まり、**かつ** `.example` / `.sample` / `.template` で終わる場合、deny リスト照合の前に読み取りを許可する。例外は `.env` プレフィックス付きの名前に限定し、deny 対象の場所にあるテンプレート風ファイル(例: `~/.aws/credentials.sample`)はブロックされたままにする。settings 側では冗長な `Read(**/.env.*)` deny ルールをユーザーの `~/.claude/settings.json` から除去し、フックが無効化された場合でも素の `.env` を(Bash 経由含め)カバーするフェイルセーフとして `Read(**/.env)` は残した。バージョンを 2.1.0 に上げた。

## Alternatives rejected(却下した代替案)

- **ユーザーレベルの第二フック(`~/.claude/hooks/deny-env-read.py`)を重ねる** — 診断中に一度作成したが削除した。1つのポリシーを2つのフックで実施すると乖離していくし、プラグインと一緒に配布されるのはプラグイン側のフックである。
- **例外ではなく、シークレットを含むバリアントを deny リストに列挙する(`.env.local`、`.env.production`、…)** — 列挙は未掲載のバリアント(`.env.ci`、`.env.docker`)に対して fail open する。デフォルト deny + 狭いテンプレート例外なら fail closed になる。
- **任意の `*.example` / `*.sample` / `*.template` ベース名を許可する** — `credentials.sample` のようなファイルで `/.aws/` や `*.pem` の保護に穴が開く。`.env` プレフィックスのガードで例外を外科的に保つ。

## Consequences(帰結)

- Claude は `.env.example` / `.env.sample` / `.env.template`(`.env.local.sample` のような連結形も含む)を読んでプロジェクトに必要なキーを把握できる。値を含む `.env` バリアントはすべてブロックされたまま。8パスの合成フック入力によるパイプテストと、実際の Read 呼び出し(`.env.example` は許可、`.env.local` は拒否)で検証済み。
- テンプレート風の名前のファイルに本物のシークレットを入れるプロジェクト(例: 実値入りの `.env.example` をコミット)は保護されなくなる — ただしそのファイルはすでに git 経由で漏れており、フックが最後の防衛線ではない。
- ADR 0001 の帰結「`.env.example` / `.env.sample` もブロックされる(安全側に倒した仕様として許容)」は本 ADR により上書きされる。
- ADR 0001 の上限は変わらない: フックがカバーするのは Read ツールのみ。素の `.env` 以外のバリアントの Bash 読み取りは、`Read(**/.env.*)` を除去した今、settings ではなくフックに依存する。
