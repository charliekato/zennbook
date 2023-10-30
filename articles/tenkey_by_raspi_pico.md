---
title: "ラズパイピコでテンキーを作ってみる"
emoji: "😎"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["ラズパイピコ"]
published: false
---
# はじめに
昨年何か電子工作でもして遊ぼうと思って購入したラズパイピコで何を作ろうかと思案していたのですが、少しは実用的なものと思いテンキーを作ってみました。ユニバーサル基盤を二つを使って一つにはラズパイピコを実装して、もう一つはボタンスイッチを実装して二階建て構造にしました。実は、ボタンスイッチを実装した基盤は以前Ardino unoを使って電卓を作って遊んでいた時に作ったものです。そのため後でも述べますが無駄なものが付いています。ソフトはcircuit pythonを使いました。出来てからわかったのですが、ソフトを変えることでテンキーにもなるし、例えば矢印キーにもなり便利かなと思います。
# 外観
![](https://storage.googleapis.com/zenn-user-upload/5747a5e6f853-20230914.jpg)
*写真1*
9, 6, 3のボタンの右側にピンヘッダーがありここに何かを接続するようなイメージがありますが、このヘッダーはその用途には使いませんというか、このヘッダーではなく左側に使ったピンヘッダー(写真3)を使うべきです。恥ずかしながらなぜこのようなヘッダーを付けたのかよく覚えていません。以前Arduinoで電卓を作って遊んだ時にここに表示装置を付けていたのではないかと想像しています。
![](https://storage.googleapis.com/zenn-user-upload/3cbec6b363ee-20230914.jpg)
*写真2*
裏側から見たのがこれです。基盤の一階部分と二階部分のスペースが少ないのでラズパイピコを裏側に実装しています。
一階部分と二階部分は下の写真のようなヘッダーでつなぎます。これはたぶん、型番がPSS-410256-00というピンヘッダーだと思います。このヘッダーを使う部分だけ切って使ってます。
![](https://storage.googleapis.com/zenn-user-upload/48209339760a-20230914.png)
*写真3*
横から見たところはこんな感じです。
![](https://storage.googleapis.com/zenn-user-upload/f80d25b5933b-20230914.jpg)
*写真4*
ピンヘッダーの足が6mmあるので二階と一階をこのようにつなぐことができます。強度補強のため基盤の四隅に六角スタンドオフを付けていますが、このスタンドオフは自宅に転がっていたものを使いました。長さは6.5mmでM3のねじが付いているものです。長さは5mmでも大丈夫だと思います。
# 回路図
回路図は以下の通りです。
![](https://storage.googleapis.com/zenn-user-upload/1301ebf8c0e1-20231019.jpg)
*図1*
回路図ではジャンパーを4個使っている(基盤1で二つ、基盤2で二つ)ように書かれていますが、これは写真3のピンヘッダーで、このヘッダーで一階部分と二階部分を電気的かつ物理的に接続しています。ですからヘッダーは二個です。jp2とjp4が同一のものでjp1とjp3も同一です。jp2とjp4の同じpin番号同士が同一のピンだということです。jp1とjp3についても同様です。
二階部分の基盤1にスイッチ15個を実装しています。 S1,S4,S7,S10,S13の片側はヘッダーを通して(回路図ではJP1の1番ピンとJP3の1番ピンを通して)一階部分の基盤2に実装されているラズパイピコのGP0につながっています。同様に、 S2,S5,S8,S11,S14の片側はGP1に、S3,S6,S9,S12,S15の片側はGP2につながっています。GP0,GP1,GP2は出力として使います。S1,S2,S3のもう片側は回路図のJP2,JP4を通してラズパイピコのGP28につながっています。同様に S4,S5,S6はGP27に、S7,S8,S9はGP26に、S10,S11,S12はGP22に、S13,S14,S15はGP21に接続されています。GP28,GP27,GP26,GP22,GP21は入力として使います。Raspberry Pi PicoのGPIOは全部で26個あるのでswitch一つにGPIO を一つ対応させることも可能(switchは15個なので)で、(その場合は対応するGPIO PINはすべて入力) そうするとソフトは極めて簡単になりますが、配線が煩雑になるのとおもしろみがないので止めました。そのためソフトはちょっとわかりにくくなります。参考までに配線図を下に示します。
![](https://storage.googleapis.com/zenn-user-upload/305bb3a2bbce-20231020.jpg)
ラズパイへの入力が5本しかないのですが、15個のキーを押したことを識別できる仕組みは次の通りです。GP0, GP1, GP2 にはopen drainの出力を使い同時には一つだけLow にします。それ以外はLowにもHighにもドライブしません(つまりHigh-Z)。ある時は GP0だけLow、またある時は GP1だけLow、そしてまたある時はGP2だけLowにします。GP28, GP27, GP26, GP22, GP21 は pull upつきの入力にします。ですからスイッチが何も押されていないときはHighが入力されます。どこかの入力がLowならばどこかのスイッチが押されたということなのですが、例えばGP0がLow出力しているときにGP28がLow入力であったらS1が、GP27がLowならS4が、GP26がLowならS7が、GP22がLowならS10がGP21がLowならS13が押されているということです。GP1がLow出力しているときは、GP28 lowでS2、 GP27 lowでS5、 GP26 lowで S8、GP22 low で　S11、GP21 lowで S14が押されているということです。同様にGP2がLow出力のときは、GP28 low で S3、GP27 Low でS6、GP26 low で S9、GP22 low で S12、 GP21 lowで S15 が押されているとわかるわけです。
# 開発環境
前にも述べましたがプログラムはCircuit Pythonを使いました。editorはなんでもいいのですが、Mu Editorを使いました。Muだとシンタックスチェックや補完などをしてくれるのでpythonの初心者にはいいと思います。筆者もpythonは超初心者なのでMuを使いました。Mu Editorとcircuit pythonの開発環境に関しては[こちら](https://tech-and-investment.com/raspberrypi-pico-16-install-circuitpython-mu/)を参照してください。ラズパイピコの開発環境で驚いたのは、ラズパイピコをUSBでPCに接続するとPC側からはラズパイピコがUSBメモリーに見えてそこに code.py という名前でpythonのコードを保管するとすぐに動作するということです。そして、Circuit Pythonにはusb hid(Human interface device)というLibraryがサポートされていますが、これを使うとラズパイピコがキーボードのようにふるまうプログラムが書けるということです。
# 入出力の設定
まずはラズパイピコの入出力の設定です。
GP0, GP1, GP2 はpull up付きの入力なので次のようにコーディングします。
``` py
import board
import digitalio
sw1 = digitalio.DigitalInOut(board.GP28)
sw1.direction = digitalio.Direction.INPUT
sw1.pull = digitalio.Pull.UP
sw2 = digitalio.DigitalInOut(board.GP27)
sw2.direction = digitalio.Direction.INPUT
sw2.pull = digitalio.Pull.UP
sw3 = digitalio.DigitalInOut(board.GP26)
sw3.direction = digitalio.Direction.INPUT
sw3.pull = digitalio.Pull.UP
sw4 = digitalio.DigitalInOut(board.GP22)
sw4.direction = digitalio.Direction.INPUT
sw4.pull = digitalio.Pull.UP
sw5 = digitalio.DigitalInOut(board.GP21)
sw5.direction = digitalio.Direction.INPUT
sw5.pull = digitalio.Pull.UP
```
