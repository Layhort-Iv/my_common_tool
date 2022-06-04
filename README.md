## 概要
シナリオに沿って、動作確認を行い、その結果をコンソールに表示する

## 動作要件
Python 3.6.0 以上
* paho-mqtt
* python-dateutil
* pyyaml
* requests

```
pip install paho-mqtt python-dateutil pyyaml requests
python -m pip install beautifulsoup4
```
Pre-requisition:
1. Create Email Domain and emailFromDomainId in "Request >Mail > Mail.yml" & "Trigger > Mail_action.yml"
2. Change Email to Test Email in "Scenario > BatchDelete.py > readUser" & "Scenario > RecordExport.py > readUser"
## 動作処理
コンソール上で指定された環境でシナリオを実行する<br>
シナリオの詳細は下記の各シナリオの処理を参照<br>
但し、指定シナリオの実行前には初期処理が行われる<br>
シナリオの完了後、作成されたアプリやデバイスコレクションは削除される

## 事前準備
* ユーザの発行
* アカウントの発行
* APIキーの取得

config/environment.ymlの該当環境のapi_keyに取得したAPIキーを設定<br>
環境を追加したい場合は以下のように追記

```
(任意の文字列):
  http_host: (HTTPURL)
  http_port: (HTTPポート)
  mqtt_host: (MQTTホスト)
  mqtt_port: (MQTTポート)
  certificate: (証明書のパス)
  api_key: (取得したAPIキー)
```
また、ログ出力動作を変えたい場合はconfig/logger.ymlに記述

## 使用法
```
python . -e prod -s all(本番環境で全シナリオを実行)<br>
python . -e dev -s ABC (開発結合環境でシナリオABCを実行)<br>
python . -h (ヘルプ)
```

## 各シナリオの処理

### init(初期処理)
このシナリオは、任意で実行できず指定のシナリオの前に自動で実行する

* 更新から5分以上経過かつ表示名に"stdtest"を含むアプリ、デバイスコレクションの削除

### user
* プロフィールの取得
* プロフィールの更新

### app
* アプリ作成
* アプリ取得
* アプリ更新
* アプリ削除
* DB作成
* DB取得
* DB更新
* DB削除
* レコード登録
* レコード取得
* レコード更新
* レコード削除
* 操作元一覧取得
* 操作元取得

### recordExport
* アプリ作成
* DB作成
* 出力用にレコードを２件登録
* レコードの一括出力依頼を作成
* レコードの一括出力依頼を取得してステータスを確認
* 生成されたダウンロードAPIのURLを実行し,出力された件数やヘッダーが正しいか確認
※ システムAPIを使用しているためローカルと開発結合環境でのみ使用できるものとなるためご注意ください。
　また、アカウントIDを間違えて記述しないようご注意ください。

### batchInsert
* アプリ作成
* DB 作成
* レコードの一括登録依頼を作成
* レコードの一括登録依頼を取得して登録が完了することを確認
* レコードの一覧を取得して正しい件数だけ登録されることを確認

### batchDelete
* アプリ作成
* DB作成
* レコード登録(5 records)
* レコード取得
* 一括削除(条件はレコードIDは >2)
* 一括処理ステータス取得
* レコード取得(2 records)

### iot(IoT周りの疎通確認)
このシナリオは、IoT関連のAPIの送信、MQTTメッセージの送受でIoT周りの機能が正しく動作するかを確認することを目的とする

* アプリの作成
* DB作成
* デバイスコレクションの作成
* デバイスの作成
* トピックの作成
* ストリームの作成
* トリガの作成
* ユーザからのMQTTメッセージがデバイスへ到達することを確認
* デバイスからのMQTTメッセージの集計を確認
* トリガからのMQTTメッセージがデバイスへ到達することを確認
* トリガからのwebhook(デフォルトで行わない)

※トリガからのwebhookを確認するにはrequest/iot/trigger.ymlの設定が必要

### mail  
事前にアプリ(表示名:mail_app)、DBの作成(表示名:mail_db)、<br>レコードを2つ登録(pi-pe.co.jpとtest.smp.ne.jp)、差出人ドメインの認証(pi-pe.co.jp)を行う必要がある

* アプリ取得
* DB取得
* 差出人ドメインを取得
* EXPRESSメールの設定を作成
* テスト配信
* メール配信ログ一覧を取得
* メール配信エラー一覧を取得
* メール配信エラー情報を削除
* EXPRESSメールの設定を削除
