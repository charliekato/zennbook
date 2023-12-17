---
title: "ラズパイピコでテンキーを作ってみる"
emoji: "😎"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["ラズパイピコ"]
published: true
---
# はじめに
昨年何か電子工作でもして遊ぼうと思って購入したラズパイピコで何を作ろうかと思案していたのですが、少しは実用的なものと思いテンキーを作ってみました。ユニバーサル基盤を二つを使って一つにはラズパイピコを実装して、もう一つはボタンスイッチを実装して二階建て構造にしました。実は、ボタンスイッチを実装した基盤は以前Ardino unoを使って電卓を作って遊んでいた時に作ったものです。そのため後でも述べますが無駄なものが付いています。ソフトはcircuit pythonを使いました。ソフトを変えることでテンキーにもなるし、例えば矢印キーにもなるし、自分の好みのキーを割り当てることができます。
ただし、キーが市販のボタンキーなのでタッチ感はあまりよくありません。テンキーとして使うなら市販の物には負けますね。残念ながら。
# 外観
<!--- ![](/images/photo2.jpg) -->
![](https://storage.googleapis.com/zenn-user-upload/bf038e48f028-20231216.jpg)
*写真1*
9, 6, 3のボタンの右側にピンヘッダーがありここに何かを接続するようなイメージがありますが、このヘッダーはその用途には使いませんというか、このヘッダーではなく左側に使ったピンヘッダー(写真3)を使うべきです。恥ずかしながらなぜこのようなヘッダーを付けたのかよく覚えていません。以前Arduinoで電卓を作って遊んだ時にここに表示装置を付けていたのではないかと想像しています。
![](https://storage.googleapis.com/zenn-user-upload/3cbec6b363ee-20230914.jpg)
*写真2*
裏側から見たのがこれです。基盤の一階部分と二階部分のスペースが少ないのでラズパイピコを裏側に実装しています。
一階部分と二階部分は下の写真のようなヘッダーでつなぎます。これはたぶん、型番がPSS-410256-00というピンヘッダーだと思います。このヘッダーを使う部分だけ切って使ってます。
<!-- ![](https://storage.googleapis.com/zenn-user-upload/48209339760a-20230914.png) -->
![](/images/photo.jpg)

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
*図2*
ラズパイへの入力が5本しかないのですが、15個のキーを押したことを識別できる仕組みは次の通りです。GP0, GP1, GP2 にはopen drainの出力を使い同時には一つだけLow にします。それ以外はLowにもHighにもドライブしません(つまりHigh-Z)。ある時は GP0だけLow、またある時は GP1だけLow、そしてまたある時はGP2だけLowにします。GP28, GP27, GP26, GP22, GP21 は pull upつきの入力にします。ですからスイッチが何も押されていないときはHighが入力されます。どこかの入力がLowならばどこかのスイッチが押されたということなのですが、例えばGP0がLow出力しているときにGP28がLow入力であったらS1が、GP27がLowならS4が、GP26がLowならS7が、GP22がLowならS10がGP21がLowならS13が押されているということです。GP1がLow出力しているときは、GP28 lowでS2、 GP27 lowでS5、 GP26 lowで S8、GP22 low で　S11、GP21 lowで S14が押されているということです。同様にGP2がLow出力のときは、GP28 low で S3、GP27 Low でS6、GP26 low で S9、GP22 low で S12、 GP21 lowで S15 が押されているとわかるわけです。
# 開発環境
前にも述べましたがプログラムはCircuit Pythonを使いました。editorはなんでもいいのですが、Mu Editorを使いました。Muだとシンタックスチェックや補完などをしてくれるのでpythonの初心者にはいいと思います。筆者もpythonは超初心者なのでMuを使いました。Mu Editorとcircuit pythonの開発環境に関しては[こちら](https://tech-and-investment.com/raspberrypi-pico-16-install-circuitpython-mu/)を参照してください。ラズパイピコの開発環境で驚いたのは、ラズパイピコをUSBでPCに接続するとPC側からはラズパイピコがUSBメモリーに見えてそこに code.py という名前でpythonのコードを保管するとすぐに動作するということです。そして、Circuit Pythonにはusb hid(Human interface device)というLibraryがサポートされていますが、これを使うとラズパイピコがキーボードのようにふるまうプログラムが書けるということです。
プログラムの説明の前にプログラムで使う変数と実際の回路とスイッチとの対応表を示します。この後のプログラムの説明はこの表を参照しながら読むと理解できるかと思います。
![](https://storage.googleapis.com/zenn-user-upload/7549122f9c09-20231216.jpg)
*表1*
# 入出力の設定
まずはラズパイピコの入出力の設定ですが、設定プログラムを書くためには次の２行をプログラムの先頭に書く必要があります。
``` py
import board
import digitalio
```
そして例えばGP28を入力に設定するには次のように書きます。これについてはpythonの知識が乏しい筆者がごちゃごちゃ説明するより[ここ](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html)なんかを参照していただければと思います。

``` py
sw1 = digitalio.DigitalInOut(board.GP28)
sw1.direction = digitalio.Direction.INPUT
```
これでラズパイピコのGP28が変数sw1に対応されることになります。そしてこのGP28を内部でpull upするには次のように書きます。
``` py
sw1.pull = digitalio.Pull.UP
```

同様にGP27,GP26,GP22,GP21を設定します。

``` py
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

次は出力側です。出力はOpen Drainを使ってLow activeとして使います。Open Drainではなく普通の push/pull (High/Lowの出力ができるタイプ)で High activeの方がわかりやすいのではと思うでしょうが、それだと２つ以上のkeyを同時に押したときにショートする危険性があります。それについては後ほど説明することにしますが、ここでは、Open Drainの Low activeが常識だと理解してください。
入力に割り当てる変数をsw1,sw2,...,sw5としたので出力はswout1,swout2,swout3を割り当てることにします。swout1をGP2にswout2をGP1にswout3をGP0に割り当ててみます。
``` py
swout1 = digitalio.DigitalInOut(board.GP2)
swout1.direction = digitalio.Direction.OUTPUT
swout1.drive_mode = digitalio.DriveMode.OPEN_DRAIN
swout2 = digitalio.DigitalInOut(board.GP1)
swout2.direction = digitalio.Direction.OUTPUT
swout2.drive_mode = digitalio.DriveMode.OPEN_DRAIN
swout3 = digitalio.DigitalInOut(board.GP0)
swout3.direction = digitalio.Direction.OUTPUT
swout3.drive_mode = digitalio.DriveMode.OPEN_DRAIN
```
さて入力と出力の記述ですが、このようにべたに書いてももちろんいいのですが、これでは見ずらいですしあまりよくありません。何か工夫が必要です。そこで入力側は関数を使って次のように書き換えました。
```py
def define_input_pin(boardpin):
    inpin = digitalio.DigitalInOut(boardpin)
    inpin.direction = digitalio.Direction.INPUT
    inpin.pull = digitalio.Pull.UP
    return inpin

sw1 = define_input_pin(board.GP28)
sw2 = define_input_pin(board.GP27)
sw3 = define_input_pin(board.GP26)
sw4 = define_input_pin(board.GP22)
sw5 = define_input_pin(board.GP21)

```
これだと分かりやすいですし、間違いも少なくなると思います。同様に出力側も次のように書き換えます。
```py
def define_output_pin(boardpin):
    outpin = digitalio.DigitalInOut(boardpin)
    outpin.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
    return outpin

swout1 = define_output_pin(board.GP2)
swout2 = define_output_pin(board.GP1)
swout3 = define_output_pin(board.GP0)
```

ラズパイピコのpinとそれに対応するpythonの変数名の対応表を以下に示します。
![](https://storage.googleapis.com/zenn-user-upload/af3ddec962b5-20231216.jpg)
*表2*
# 出力信号の切り替え
Outputは３つのうちどれか一つだけActive(low)にします。lowはFalseで highはTrueです。open drainなのでhighではなく実際にはhi-Zです。GP2をlowにするには次のように書きます。
``` py
swout1.value = False
```
Activeにする出力を順番に切り替える必要があります。これは while True の永久loopのなかでカウンターを回してカウンターの値でactiveにするpinを切り替えていきます。次のようにコーディングします。
``` py:プログラム1

counter = 0
while True:
    counter += 1
    if counter == 30:
        counter = 0
    if counter == 0:
	swout1.value = False
	swout2.value = True
        swout3.value = True
    if counter == 10:
	swout1.value = True
	swout2.value = False
        swout3.value = True
    if couter == 20:
	swout1.value = True
	swout2.value = True
        swout3.value = False
```
counterが 0～9ではswout1 つまりGP2が、10～19ではswout2つまりGP1が、20～29ではswout3つまりGP0がactiveになります。counterは30で0にもどります。
プログラムは見やすくするためできる限り短くするのが望ましいです。長いと追うのが大変です。上のプログラムは、 counter をインクリメントしているところは関数にしてしまいます。そのほうが見やすいからです。

``` py
def increment_counter(counter):
    counter += 1
    if counter == 30:
        counter = 0
    return counter
```
そして、出力を出しているところも関数にしてしまいます。
``` py
def gp_output(value1, value2, value3):
    swout1.value = value1
    swout2.value = value2
    swout3.value = value3
```
そして本体を次のように書き換えます。
``` py
while True:
    counter = increment_counter(counter)
    if counter == 0:
        gp_output(False,True,True)
    if counter == 10:
        gp_output(True,False,True)
    if counter == 20:
        gp_output(True,True,False)
```

ついでにwhile以下の七行も関数にしてしまいます。アクティブにする出力を切り替える関数なので rotate_outputという名前にします。
```py
def rotate_output(ctn):
    ctn = increment_counter(ctn)
    if ctn == 0:
        gp_output(False, True, True)
    if ctn == 10:
        gp_output(True, False, True)
    if ctn == 20:
        gp_output(True, True, False)
    return ctn
```



counterの値からどの列がアクティブになっているかを知るための関数を作っておきます。 get_active_columnという名前にしておきます。

```py
def get_active_column(switch):
        if switch < 10:
        return 2
    if switch < 20:
        return 1
    return 0
```
同様にどの行のボタンが押されているかを数値で返す関数を作っておきます。
```py
def get_row_value(sw5, sw4, sw3, sw2, sw1):
    rowValue = (sw5.value == 0) * 16
    rowValue = rowValue + (sw4.value == 0) * 8
    rowValue = rowValue + (sw3.value == 0) * 4
    rowValue = rowValue + (sw2.value == 0) * 2
    rowValue = rowValue + (sw1.value == 0)
    return rowValue
```
ちょっとややこしいですが、これは二つ以上のキーを同時に押したときにも対応しようと考えて作ってます。実をいうと同時押しの時の処理をどうすればいいのかわかっていないのですが、とりあえず将来できるようにと考えてこのようにしています。
sw5に対応するキー(どの列がアクティブかによって三つありますが、)が押された時は16が、sw4に対応するキーの時は、8がsw3では4、sw2では2、そしてsw1では1が得られます。sw5とsw4が同時に押された時は、と言っても同じ列のボタンが同時に押された場合ですが、24が得られる関数です。
このget_active_columnとget_row_valueで得られる値を元にどのキーが押されたかを調べてさらにそのキー番号をkeyin関数に渡す関数を作ります。keyin関数の中でホスト側にkeycodeを送信しますが、これは後ほど作ります。
```py
counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else:
        row = myLog(rowValue)
        keyNo = row * 3 + column
        if counter[keyNo] < 4:
            counter[keyNo] += 1
        if counter[keyNo] == 3:
            keyin(keyNo)

```
myLog()という関数がでてきますが、これは、引数のlog(底が2の対数)を返す関数ですが、引数は 1,2,4,8,16しかありえないので次のように定義しています。
```py
def myLog(rowValue):
    if rowValue == 1:
        return 0
    if rowValue == 2:
        return 1
    if rowValue == 4:
        return 2
    if rowValue == 8:
        return 3
    if rowValue == 16:
        return 4
    return 0
```
なぜこんなややこしいことをしているかというと前にも述べたように二つのキーを同時に押したときにも対応しようと考えたためです。そのためget_row_value()は2のべき乗の値を返すようにしたので、対数を取る必要が出たわけです。まあでも結局同時押しの処理は試行錯誤をしたのですが、うまくいっていません。
どうせうまくいっていないので、myLog()のようなちょっとややこしいことをやめましょう。 そうするには、decode_key()とget_row_value()は次のように書き換えます。こうなると、myLog()関数はもはや不要です。

```py
counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

CHATTERING_PREVENT_NUM=100
def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else :
        keyNo = (rowValue - 1) * 3 + column
        if counter[keyNo] <= CHATTERING_PREVENT_NUM:
            counter[keyNo] += 1
        if counter[keyNo] == CHATTERING_PREVENT_NUM:
            keyin(keyNo)
```


```py
def get_row_value(sw5, sw4, sw3, sw2, sw1):
    if sw5.value == 0:
        return 5
    if sw4.value == 0:
        return 4
    if sw3.value == 0:
        return 3
    if sw2.value == 0:
        return 2
    if sw1.value == 0:
        return 1
    return 0

```
get_row_value()は単純に 0ならばどのキーも押されていないということで、1ならsw1(GP21)につながっている三つのボタンのうちどれか、2なら sw2(GP22)で、3なら sw3(GP26) 4なら sw4(GP27) 5ならsw5(GP28) ということになります。
同時に押したときは、swの数字の小さい方は無視されることになります。以前のコードと違うのは無視するか、考慮するかです。無視しても機能上は特に問題はありません。

# キーの取り込み関数 decode_key()を作る
さて、 decode_key()関数の説明に戻ります。rowValueが0のときに

```py
	for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
```
としていますが、counter[]とはキーが押さされ続けたときにホスト側にコードを何回も送ってしまうのと、チャタリングを防ぐためのcounterで15個のキーに対応して、counterもcounter[0] ... counter[14]の15個あります。これについては後ほど説明します。
counter[i]はi番のkeyに対応するcounterということです。decode_key()関数の中では、このiはkeyNoという変数になります。
i番のキーとはどれかというのを説明するため図1のボタンアレイの部分の回路図をもう少し分かりやすく書いたものを見てみます。

![](https://storage.googleapis.com/zenn-user-upload/b423fc436103-20231216.jpg)
0番のキー(ボタンとキーという用語が混在していますが、どちらも同じ意味で使っています。)はS13です。以下、 1->S14, 2->S15, 3->S10, 4->S11, 5->S12, 6->S7, 7->S8, 8->S9, 9->S4, 10->S5, 11->S6, 12->S1, 13->S2, 14->S15 となります。(表1にも書いています。)
rowValueが0というのは、いまアクティブな列のボタンがどれも押されていない状態を示しています。その時にその列のボタンに対応するcounterがゼロクリアされます。 range(column, 15, 3)はpythonの標準の関数で、columnから15まで3おきの数字のリストを返してくれます。詳しくはpythonのマニュアルを見てください。
columnが0の時つまり一番左の列(GP0につながっている列)がアクティブの時は、range(0,15,3)となり、これは、
[0, 3, 6, 9, 12] となります。ですので、
```py
     for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
```
は、 counter[0], counter[3], counter[6], counter[9] と、counter[12] が0にクリアされます。
さて、ややこしいのは、counterの動作ですね。このcounterはチャタリングという現象とキーを押し続けたときにそのキーが何度も入力されるのを防止する仕組みに使われています。
decode_key()のelse以下を見てみましょう。else以下ということは、rowValueが0でないときの処理です。
```py
    else :
        keyNo = (rowValue - 1) * 3 + column
        if counter[keyNo] <= CHATTERING_PREVENT_NUM:
            counter[keyNo] += 1
        if counter[keyNo] == CHATTERING_PREVENT_NUM:
            keyin(keyNo)
```
rowValueが0でないときはsw1からsw5のどれかにlow信号が入ったということです。つまりどこかのkeyが押されたということです。どこかのkeyが押されたらそれに対応するkeycodeをホストに送るわけです。そのホストに送る処理をする関数が keyin()です。keyin()は、その引数のキーに対応するkeycodeをホストに送ります。この中身は後で説明します。さて、else以下を次の様に書いたらどうなるでしょうか。
```py
    else:
	keyNo = (rowValue - 1) * 3 + column
	keyin(keyNo)
```
説明していませんでしたが、
```py
	keyNo = (rowValue - 1) * 3 + column
```
はrowValueとcolumnからどのキーつまりkeyNoを求める式です。これは表1を眺めていただければわかると思います。で、問題は上のelse以下のコードですね。一見よさそうにも見えますが、これでは、キーを押している間何回もkeyin()を呼ぶことになりホストにkeycodeを送り続けることになります。それではまずいので一回ホストに送ったらそのあとは送らないようにします。でも、それだけだったらカウンターは必要ではなくフラグを使えば済みますが、次に説明するチャタリングを防止するためにカウンターが使われています。
## チャタリングについて
チャタリングとは下の図のようにスイッチを押した時に何回もlow/highを繰り返しながらlowになる現象のことです。スイッチを離したときも同様にlow/highを繰り返しながら最終的にはhighになります。
![](https://storage.googleapis.com/zenn-user-upload/3b7f8cd520bb-20231217.png)
*図 チャタリング*
これを防止するためcounterを使っています。チャタリングが落ち着くまで待つために使っているわけです。counterはキーが押されている間カウントアップされます。counterの値が CHATTERING_PREVENT_NUMと等しくなったら初めて keyin()関数を呼び出してホストにキーコードを送信し、counterの値は CHATTERING_PREVENT_NUM+1になります。その後keyを押し続けていてもcounterはカウントアップされないためkeyin()は呼び出されることはありません。キーを離すとcounterがリセットされ次にキーが押されるまではカウントアップされません。CHATTERING_PREVENT_NUMはチャタリングが落ち着くのに必要な時間分の値をセットしておきます。これが小さな値だとチャタリングのためにcounterがリセットされ再びカウントアップが始まりkeyin()関数が呼び出されてホストにキーコードを送信してしまいます。
CHATTERING_PREVENT_NUMはチャタリングが落ち着くのに必要な時間に対応する数値ですが、スイッチの特性で値をどれくらいにすればいいかはわかりません。試行錯誤で適切な値を決めます。筆者の作った物ですと10程度の数字ではキーによっては何回も取り込みがされていました。100ぐらいで落ち着きました。100でも取り込みが遅くなるという感覚は全くなかったのでこれを採用したわけです。



# ホストに送信 (keyin()関数を作る)
キーを取り込んだらPCに信号を送る必要があります。これは usb_hidというライブラリーを使います。usb_hidについては[ここ](https://docs.circuitpython.org/projects/hid/en/latest/)を参照してください。usb_hidを使うためにはソースコードの先頭に次の三行を追加する必要があります。
```py
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
```
そしてホストに送信するための関数keyin()を作ります。押されたボタンに対応する番号を引数にしてこの関数を呼ぶとそのボタンに対応するコードがホスト側に送られます。次のようになります。kbd.send()というライブラリーの関数を使えばこのように簡単に作れます。
```py
def keyin(keyNo):
    if keyNo == 14:
        kbd.send(Keycode.NINE)
    if keyNo == 13:
        kbd.send(Keycode.EIGHT)
    if keyNo == 12:
        kbd.send(Keycode.SEVEN)
    if keyNo == 11:
        kbd.send(Keycode.SIX)
    if keyNo == 10:
        kbd.send(Keycode.FIVE)
    if keyNo == 9:
        kbd.send(Keycode.FOUR)
    if keyNo == 8:
        kbd.send(Keycode.THREE)
    if keyNo == 7:
        kbd.send(Keycode.TWO)
    if keyNo == 6:
        kbd.send(Keycode.ONE)
    if keyNo == 5:
        kbd.send(Keycode.KEYPAD_MINUS)
    if keyNo == 4:
        kbd.send(Keycode.KEYPAD_PLUS)
    if keyNo == 3:
        kbd.send(Keycode.ZERO)
    if keyNo == 2:
        kbd.send(Keycode.ENTER)
    if keyNo == 1:
        kbd.send(Keycode.FORWARD_SLASH)
    if keyNo == 0:
        kbd.send(Keycode.KEYPAD_ASTERISK)
```
ここで、keyNoというのが引数でボタン番号と呼ぶことにします。ボタン番号はこのプログラムを見ていただければ容易にわかると思いますが、左下が0で右上が14です。表1を見てもらっても分かるかと思います。
それではmainです。mainはいたってかんだんです。次のようになります。

```py
loopCounter = 0
#
while True:
    loopCounter = rotate_output(loopCounter)
    activeColumn = get_active_column(loopCounter)
    rowValue=get_row_value(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)

```
# ソースコード
ソースコード全体は以下になります。
```py
import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


def keyin(keyNo):
    if keyNo == 14:
        kbd.send(Keycode.NINE)
    if keyNo == 13:
        kbd.send(Keycode.EIGHT)
    if keyNo == 12:
        kbd.send(Keycode.SEVEN)
    if keyNo == 11:
        kbd.send(Keycode.SIX)
    if keyNo == 10:
        kbd.send(Keycode.FIVE)
    if keyNo == 9:
        kbd.send(Keycode.FOUR)
    if keyNo == 8:
        kbd.send(Keycode.THREE)
    if keyNo == 7:
        kbd.send(Keycode.TWO)
    if keyNo == 6:
        kbd.send(Keycode.ONE)
    if keyNo == 5:
        kbd.send(Keycode.ENTER)
    if keyNo == 3:
        kbd.send(Keycode.ZERO)

def gp_output(value1, value2, value3):
    swout1.value = value1
    swout2.value = value2
    swout3.value = value3
#
# swout1, swout2, swout3
def rotate_output(ctn):
    ctn = increment_counter(ctn)
    if ctn == 0:
        gp_output(False, True, True)
    if ctn == 10:
        gp_output(True, False, True)
    if ctn == 20:
        gp_output(True, True, False)
    return ctn

def increment_counter(a):
    a += 1
    if a == 30:
        a = 0
    return a


def get_active_column(switch):
    if switch < 10:
        return 2
    if switch < 20:
        return 1
    return 0
'''
def get_row_value(sw5, sw4, sw3, sw2, sw1):
    rowValue = (sw5.value == 0) * 16
    rowValue = rowValue + (sw4.value == 0) * 8
    rowValue = rowValue + (sw3.value == 0) * 4
    rowValue = rowValue + (sw2.value == 0) * 2
    rowValue = rowValue + (sw1.value == 0)
    return rowValue
'''
def get_row_value(sw5, sw4, sw3, sw2, sw1):
    if sw5.value == 0:
        return 5
    if sw4.value == 0:
        return 4
    if sw3.value == 0:
        return 3
    if sw2.value == 0:
        return 2
    if sw1.value == 0:
        return 1
    return 0




counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
'''
def myLog(rowValue):
    if rowValue == 1:
        return 0
    if rowValue == 2:
        return 1
    if rowValue == 4:
        return 2
    if rowValue == 8:
        return 3
    if rowValue == 16:
        return 4
    return 0

def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else:
        row = myLog(rowValue)
        keyNo = row * 3 + column
        if counter[keyNo] < 4:
            counter[keyNo] += 1
        if counter[keyNo] == 3:
            keyin(keyNo)
'''
def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else :
        keyNo = (rowValue - 1) * 3 + column
        if counter[keyNo] < 4:
            counter[keyNo] += 1
        if counter[keyNo] == 3:
            keyin(keyNo)


def define_input_pin(boardpin):
    inpin = digitalio.DigitalInOut(boardpin)
    inpin.direction = digitalio.Direction.INPUT
    inpin.pull = digitalio.Pull.UP
    return inpin

def define_output_pin(boardpin):
    outpin = digitalio.DigitalInOut(boardpin)
    outpin.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
    return outpin

#

kbd = Keyboard(usb_hid.devices)
sw5 = define_input_pin(board.GP28)
sw4 = define_input_pin(board.GP27)
sw3 = define_input_pin(board.GP26)
sw2 = define_input_pin(board.GP22)
sw1 = define_input_pin(board.GP21)

swout1 = define_output_pin(board.GP2)
swout2 = define_output_pin(board.GP1)
swout3 = define_output_pin(board.GP0)
#
# swout1, swout2, swout3
gp_output(False, True, True)
#
loopCounter = 0
#
while True:
    loopCounter = rotate_output(loopCounter)
    activeColumn = get_active_column(loopCounter)
    rowValue=get_row_value(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)


```
# おわりに
今回はテンキーを作りましたが、keyin()関数を書き換えれば自分の好きなキーを割り当てることも当然できます。今回はうまくいきませんでしたが、キーの同時押しをすることや、あるキーを順番に押すことでキーの割り当てを変更することもできます。例えば、1234567890+-/* と順番に押したらテンキーではなく矢印キーに割り当てを変えるというようなこともできます。次はそれに挑戦しようかなと思います。
