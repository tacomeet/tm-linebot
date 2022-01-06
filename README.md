# TeenMakers公式LINEボット

## アプリの概要

私が個人的に行っているTeenMakersという「中高生が社会人に取材をする」プロジェクトの公式LINEアカウントです。
42tokyo Advent Calendar 2021の記事として「[LINE公式垢でボットとチャット両立させてみた！](https://qiita.com/tacomeet/items/a3945d3321ab104a72e2) 」にて機能の解説なども行っています。

TeenMakersについてご興味を持って頂けた方は[こちらのウェブサイト](https://teenmakers.jp/) をご覧ください！


## 使用言語

```
Python 3.9.9
```

## 機能

1. レコメンド機能 (LINE)
2. 会話機能 (LINE)
3. お問い合わせ機能 (LINE, Slack)

## 注力点

- ユーザー毎に状況を保存することで会話を行えるようにした
- LINEボットでは、Botモードとチャットモードの片方しか選択できないが、Slackを用いることで、自動対応と個別対応の両方を行えるようにした

それぞれ詳細についてはこちらの記事をご覧ください！

[LINE公式垢でボットとチャット両立させてみた！ - Qiita](https://qiita.com/tacomeet/items/a3945d3321ab104a72e2)

## 環境構築の手順

1. ローカルへダウンロード

```
git clone https://github.com/tacomeet/linebot-tm
cd linebot-tm
```

2. SlackとLINEのAPIを使用するのに必要な情報を `.env` ファイルに記述

```
SLACK_TOKEN=***
LINE_CHANNEL_ACCESS_TOKEN=***
LINE_CHANNEL_SECRET=***
```

3. 起動

```
python app.py
```

## デモ

### LINEアカウント

<a href="https://lin.ee/BbMdvBt"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="36" border="0"></a>

### デモ動画

|　　　　　　　　  　　　　　　　　   　　　　　　　　　　　　　　　　　　　　　　　　　|
|:-:|
|![demo.gif](https://github.com/tacomeet/linebot-tm/blob/master/gif/demo1.gif) |
|<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1212145/194c9814-1127-682b-3d5c-49f2bd9dc9bf.gif" width="800" > |


## 著者

[moromin](https://github.com/moromin)

[tacomeet](https://github.com/tacomeet)
