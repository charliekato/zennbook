---
title: "powerpointを使った賞状印刷システム"
emoji: "🏊"
type: "idea" # tech: 技術記事 / idea: アイデア
topics: ["競泳リザルトシステム","vba","PowerPoint"]
published: true
---
# はじめに
セイコーリザルトシステムVer 6. の賞状印刷システムはexcelの差込印刷と同じ手法を使っていますが文字の位置決めが きわめて面倒で使いにくいためPowerPointを使って同様に差し込み印刷の手法をVBAで実現しました。
PowerPointで賞状原紙の画像を背景にしておき文字の位置決めを行うのでとても便利です。
![](/images/print_certificate_by_ppt/screen_shot.png =600x)
# 概要
原理はいたって簡単です。PowerPointで印刷したい場所にtextBoxを配置してそのtextBoxにセイコーのリザルトシステムが使っているSQL ServerのDBから必要な情報を取ってきて差し込み印刷を行うだけです。操作の概要は以下の通りです。
1. 賞状は通常縦長なのでPowerPointの規定値とは異なるためスライドのサイズの変更をしておきます。
2. 次にPowerPointで賞状の原紙の画像を背景に設定します。
3. textBoxなどを使って選手名、所属等を好みの位置に好みのフォントで書いていきます。
4. 差し込みしたいtextBoxに名前をつけます。プログラムはその名前のところに該当する文字を差し込みます。
5. vba で作ったプログラムを走らせて差し込み印刷をします。印刷するときは自動で背景は削除されます。
以上ですが、4までは事前準備で一回やれば終わりです。5の操作はguiでボタンを押すだけです。
# 手順
1. まず、vbaのソースコードをimportするためダウンロードしておきます。ソースコードは[github](https://github.com/charliekato/PPTSwimCertificate) にあるのですべて同じフォルダーにダウンロードします。ダウンロードするファイルは以下の通りです。
   - formEventNoPick.frm  
   - formPrgNoPick.frm 
   - formServerSelect.frm
   - formEventNoPick.frx  
   - formPrgNoPick.frx  
   - formServerSelect.frx
   - HyouShow.bas

2. PowerPointはデフォルトで「開発」のタブがないので「開発」のタブが表示されるようにしておきます。(方法についてはchatGPTなどに教えてもらってください。) 
3. このVBAはwindows SQL serverにaccessするためActiveXのライブラリーが必要です。Visual Basic Editorでツール->参照設定 で Microsoft ActiveX Data Objects 2.8 Library の左側のcheck boxにチェックを入れておきます。これでActiveXのライブラリーが使えるようになります。
4. 1.でダウンロードしたコードをインポートします。Visual Basic Editorでファイル->ファイルのインポートで一つずつインポートします。
5. 用紙の設定をします。PowerPointで　デザイン->スライドのサイズ->ユーザー設定のスライドのサイズ で適切な用紙に設定します。通常 A4縦　になるかと思います。
6. 以上下準備ができたら賞状の文字の配置を通常のPowerPointの操作で行います。
7. 文字はtextBoxなどを使って配置しますが、差し込みが必要なところには名前をつけます。その名前をみてVBAは差し込みをするので名前は次の決められたものを使う必要があります。
     - 選手名
     - 所属
     - クラス
     - 種目　(「女子200m平泳ぎ」のように表示される)
     - タイム
名前は、ホームタブ->編集->選択->オブジェクトの選択と表示　でつけることができます。     

8. 開発タブ->マクロでマクロを表示し、賞状印刷を選択しマクロを実行します。
![](/images/print_certificate_by_ppt/screen_shot2.png =600x)

9. サーバー選択画面が出てくるのでサーバー名を入力しOKボタンを押します。(リザルトシステムV6と同じ操作方法です。)
![](/images/print_certificate_by_ppt/screen_shot3.png =600x)
10. 大会名が出てくるので、該当する大会名を選択し、OKボタンを押します。
![](/images/print_certificate_by_ppt/screen_shot4.png =600x)
11. 競技名が出てくるので該当する競技を選択し、順位の指定等をして「印刷」ボタンを押せば印刷できます。
![](/images/print_certificate_by_ppt/screen_shot5.png =600x)
12. 印刷せずにプレビューだけする場合は「プレビュー」ボタンを押せば印刷されません。
13. 印刷の設定(プリンターの選択等)は通常のPowerPointの操作で事前に行っておきます。

