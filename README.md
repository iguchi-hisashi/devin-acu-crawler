# devin-acu-crawler

devin の特定 Organaization の セッションごとの ACU を収集する

※本スクリプトは試験的に作成したので至らない点多々あり


## 概要

本スクリプトは devin teams plan を対象に v3 API を活用して当月内の全セッションの情報をCSVへ出力する。

devin API v3 -> https://docs.devin.ai/api-reference/v3/overview

2026-02-18 時点では Beata提供


## 利用ツール

- paython 3.14
- uv 0.1.0


## 環境変数

.env.sample を元に .env を作成

| Key | Description |
| ------------- | ------------- |
| API_KEY_BASE64 | devin server user token base64 encode |
| ORG_ID | Organaization ID |
| BASE_URL | devin v3 API base URL |


## 実行

現在は CI などでの実行は整備していない

ローカルからの実行のみ

```
% uv env

% uv run main.py
```


## 出力結果

月内の前セッション情報は実行後に output_all_sessions.csv ファイルに出力されます。

### 出力情報

| Key | Description |
| --- | ----------- |
| session_id | session id |
| url | sesseion url |
| user_id | session create user id |
| acus_consumed | session ACUs |
| created_at | session create date |
| updated_at | session update date |
| is_archived | is session achived |


## その他補足情報
### Organaization の ID 確認方法

Devin Login して member ページにアクセス : https://app.devin.ai/org/dmm-com

Chrome など develoer tools の Network タブから fetch/XHR の post-auth のレスポンスから確認可能

### memer の ID 確認方法

Devin Login して member ページにアクセス : https://app.devin.ai/org/dmm-com/settings/members

Chrome など develoer tools の Network タブから fetch/XHR の members?no_cache=true のレスポンスから確認可能
