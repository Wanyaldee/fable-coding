# 0007: プラグインを fable-coding から wanyaldee-skills に改名

(English: [0007-rename-to-wanyaldee-skills.md](../en/0007-rename-to-wanyaldee-skills.md))

## Context(背景)

プラグインは Fable 5 のコーディング規律を再現する単一スキルとして始まった
(「fable-coding」が適切だった)。v1.7.0 までにスキル5つ — コーディング規律、
開発哲学、Fable 5 プロンプティングリファレンス、メモリ規律、メモリ監査 — と
認証情報フックを抱えるに至り、ユーザーが「名前が中身を表していない」と指摘、
「Wanyaldee's Skills Package」を提案した。

## Decision(決定)

v2.0.0 で `wanyaldee-skills` に全面改名(識別子は kebab-case、表示名は
「Wanyaldee's Skills Package」): GitHub リポジトリを `gh repo rename` で改名
(旧 URL はリダイレクトされるため既存クローンと旧マーケットプレースパスは
動き続ける)、`.claude-plugin/*.json` のプラグイン/マーケットプレース識別子を
変更、README を改題し移行手順を記載。内側の `fable-coding` **スキル**は名前を
維持 — あれは正真正銘 Fable 5 のコーディング規律であり、パッケージ名とスキルの
役割がきれいに分離する。インストール識別子が変わるためメジャーバージョン
バンプ: 既存環境は `fable-coding` をアンインストールし、旧マーケットプレースを
削除して `Wanyaldee/wanyaldee-skills` を再登録する。

## Alternatives rejected(却下した代替案)

- **リポジトリ名だけ改名** — プラグイン識別子が中身について嘘をつき続ける。
  それこそが元の不満であり、再インストール1回を節約する代償として恒久的な
  ねじれが残る。
- **`fable-coding` スキルも改名** — あの名前は実態に正確。改名すると唯一
  まだ合っている名前を壊す。
- **「あとで」に先送り** — リポジトリは数時間前に公開されたばかりで外部
  ユーザーはいない。改名コストが今より安くなることはない。

## Consequences(帰結)

- スキル名前空間が `fable-coding:*` から `wanyaldee-skills:*` に変わる。
  インストール済み環境は1回だけ再インストール。
- ローカルクローンのディレクトリ `~/fable-coding` は意図的に据え置き
  (セッション中の改名は実行中セッションを壊す)。remote は新 URL を指して
  いるので、ユーザーは好きなときに `mv` できる。
- GitHub の旧名リダイレクトは旧名で新リポジトリが作られるまで持続する。
  README には新パスを記載済みで、長期的にリダイレクトへ依存しない。
