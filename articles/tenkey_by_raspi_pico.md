---
title: "ラズパイピコでテンキーを作ってみる"
emoji: "😎"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["ラズパイピコ"]
published: true
---
# はじめに
昨年何か電子工作でもして遊ぼうと思って購入したラズパイピコで何を作ろうかと思案していたのですが、少しは実用的なものと思いテンキーを作ってみました。ユニバーサル基盤を二つを使って一つにはラズパイピコを実装して、もう一つはボタンスイッチを実装して二階建て構造にしました。実は、ボタンスイッチを実装した基盤は以前Ardino unoを使って電卓を作って遊んでいた時に作ったものです。そのため後でも述べますが無駄なものが付いています。ソフトは[circuit python](https://circuitpython.org)を使いました。
ただし、キーが市販のボタンキーなのでタッチ感はあまりよくありません。テンキーとして使うなら市販の物には負けますね。残念ながら。作ってから気が付いたのですが、ユニバーサル基盤にボタンスイッチを実装しなくても4X4のキーパッドが安価で市販されていますね。それを使った方がいいと思います。
# 仕様
通常の数字キーが 0～9の10個と四則演算できるように +  - * / のキーがあります。そして右下の青色のボタンは特殊なキーにしてあります。キーボードのshiftキーのような役目をしてくれます。この青色キーを押しながらそのすぐ上の"-"キーを押すと "enter"になり、"3"のキーを押すとバックスペースになり、"9"を押すとnumlockになります。numlock状態を表示するLEDは実装されていません。
私のSurface(Windows11)では今一つこのnumlockキーがうまく動作しません。他のマシン(Lavie Windows10)iでは問題なく動くので、Surfaceの問題だと思います。しかたがないのでSurfaceでは、[numlocklock](https://www.inasoft.org/numlklk/)というアプリを使っています。
![](/images/hyou1.jpg)
# 外観
![](/images/photo2.jpg =250x)
*写真1*
9, 6, 3のボタンの右側にピンヘッダーがありここに何かを接続するようなイメージがありますが、このヘッダーはその用途には使いませんというか、このヘッダーではなく左側に使ったピンヘッダー(写真3)を使うべきです。恥ずかしながらなぜこのようなヘッダーを付けたのかよく覚えていません。以前Arduinoで電卓を作って遊んだ時にここに表示装置を付けていたのではないかと想像しています。
![](https://storage.googleapis.com/zenn-user-upload/3cbec6b363ee-20230914.jpg =250x)
*写真2*
裏側から見たのがこれです。基盤の一階部分と二階部分のスペースが少ないのでラズパイピコを裏側に実装しています。
一階部分と二階部分は下の写真のようなヘッダーでつなぎます。これはたぶん、型番がPSS-410256-00というピンヘッダーだと思います。このヘッダーを使う部分だけ切って使ってます。
![](https://storage.googleapis.com/zenn-user-upload/48209339760a-20230914.png =250x)
*写真3*
横から見たところはこんな感じです。
<!-- ![](https://storage.googleapis.com/zenn-user-upload/f80d25b5933b-20230914.jpg) -->
![](/images/photo.jpg =250x)
*写真4*
ピンヘッダーの足が6mmあるので二階と一階をこのようにつなぐことができます。強度補強のため基盤の四隅に六角スタンドオフを付けていますが、このスタンドオフは自宅に転がっていたものを使いました。長さは6.5mmでM3のねじが付いているものです。長さは5mmでも大丈夫だと思います。
# 回路図
回路図は以下の通りです。
![](/images/tenkey-1.jpg)
*図1 回路図*
回路図ではジャンパーを4個使っている(基盤1で二つ、基盤2で二つ)ように書かれていますが、これは写真3のピンヘッダーで、このヘッダーで一階部分と二階部分を電気的かつ物理的に接続しています。ですからヘッダーは二個です。jp2とjp4が同一のものでjp1とjp3も同一です。jp2とjp4の同じpin番号同士が同一のピンだということです。jp1とjp3についても同様です。
二階部分の基盤1にスイッチ15個を実装しています。 S0,S3,S6,S9,S12の片側はヘッダーを通して(回路図ではJP1の1番ピンとJP3の1番ピンを通して)一階部分の基盤2に実装されているラズパイピコのGP0につながっています。同様に、 S1,S4,S7,S10,S13の片側はGP1に、S2,S5,S8,S11,S14の片側はGP2につながっています。GP0,GP1,GP2は出力として使います。S0,S1,S2のもう片側は回路図のJP2,JP4を通してラズパイピコのGP21につながっています。同様に S3,S4,S5はGP22に、S6,S7,S8はGP26に、S9,S10,S11はGP27に、S12,S13,S15はGP28に接続されています。GP21,GP22,GP26,GP27,GP28は入力として使います。図1ではボタンスイッチとラズパイピコの接続が今一つ分かりにくいので分かりやすい図を以下に示します。
![](/images/tenkey2.jpg =400x)
*図2*
Raspberry Pi PicoのGPIOは全部で26個あるのでswitch一つにGPIO を一つ対応させることも可能(switchは15個なので)で、(その場合は対応するGPIO PINはすべて入力) そうするとソフトは極めて簡単になりますが、配線が煩雑になるのとおもしろみがないので止めました。そのためソフトはちょっとわかりにくくなります。参考までに配線図を下に示します。
![](/images/tenkeyp.jpg)
*図3 配線図*
ラズパイへの入力が5本しかないのですが、15個のキーを押したことを識別できる仕組みは次の通りです。GP0, GP1, GP2 にはopen drainの出力を使い同時には一つだけLow にします。それ以外はLowにもHighにもドライブしません(つまりHigh-Z)。ある時は GP0だけLow、またある時は GP1だけLow、そしてまたある時はGP2だけLowにします。GP28, GP27, GP26, GP22, GP21 は pull upつきの入力にします。ですからスイッチが何も押されていないときはHighが入力されます。どこかの入力がLowならばどこかのスイッチが押されたということなのですが、例えばGP0がLow出力しているときにGP28がLow入力であったらS12が、GP27がLowならS9が、GP26がLowならS6が、GP22がLowならS3がGP21がLowならS0が押されているということです。GP1がLow出力しているときは、GP28 lowでS13、 GP27 lowでS10、 GP26 lowで S7、GP22 low で　S4、GP21 lowで S1が押されているということです。同様にGP2がLow出力のときは、GP28 low で S14、GP27 Low でS11、GP26 low で S8、GP22 low で S5、 GP21 lowで S2 が押されているとわかるわけです。
下の表で例えば回路図での番号の行でS0の列の対応する出力がGP0で対応する入力がGP21になっていますが、これはGP0がLow (つまりアクティブ)の時にGP0がLow入力ならS0が押されたという意味です。
![](/images/hyou2.jpg)
# 開発環境
前にも述べましたがプログラムはCircuit Pythonを使いました。editorはなんでもいいのですが、Mu Editorを使いました。Muだとシンタックスチェックや補完などをしてくれるのでpythonの初心者にはいいと思います。筆者もpythonは超初心者なのでMuを使いました。(Muだと検索とかの機能もないので使いずらい面もあり実際にはVimと併用していましたが。) Mu Editorとcircuit pythonの開発環境に関しては[こちら](https://tech-and-investment.com/raspberrypi-pico-16-install-circuitpython-mu/)を参照してください。ラズパイピコの開発環境で驚いたのは、ラズパイピコをUSBでPCに接続するとPC側からはラズパイピコがUSBメモリーに見えてそこに code.py という名前でpythonのコードを保管するとすぐに動作するということです。そして、Circuit Pythonにはusb hid(Human interface device)というLibraryがサポートされていますが、これを使うとラズパイピコがキーボードのようにふるまうプログラムが書けるということです。
プログラムの説明の前にプログラムで使う変数と実際の回路とスイッチとの対応表を示します。この後のプログラムの説明はこの表を参照しながら読むと理解できるかと思います。

# USB HIDを使ってホストにキーコードを送る
テンキーにするためにはホスト(PC)にキーコードを送る必要があります。これには[USB_HIDというライブラリー](https://docs.circuitpython.org/projects/hid/en/latest/)を使います。 USB_HIDを使うためにはソースコードの先頭に次の三行を追加する必要があります。
```py
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
```
キーコードをホストに送るには、次のようにKeyboard.send()という関数を使ってもいいのですが、キーを押し続けたときに対応できるよう、キーを押したときに Keyboard.push()を、離したときに Keyboard.release()を呼ぶようにしました。いずれも引数はキーコードです。キーコードはusb_hidのライブラリーに定義されています。例えば数字の 1 のキーコードはKeycode.ONE なので、それをホストに送るには次のようにします。
```py
kbd = Keyboard(usb_hid.devices)
kbd.send(Keycode.ONE)
# Keyboard.send() で一回キーを押したことになる。
```
```py
kbd = Keyboard(usb_hid.devices)
# keyを押したときに
kbd.push(Keycode.ONE)
# keyを離したときに
kbd.release(Keycode.ONE)
```
実に簡単ですよね。
表2をもう一度見てください。一番上のkeyNoというのはボタンスイッチを押したときのラズパイピコの入出力信号からプログラムの内部でどのキーが押されたかを示す値で、rowValueとcolumnからpythonで計算します。それについては後ほどせ説明します。このkeyNoを添え字(index)にしたアレイkeycodeを次のように定義します。これが表2の一番下のKeycodeに対応します。


```py
keycode = [ Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_FORWARD_SLASH, Keycode.ENTER, \
    Keycode.KEYPAD_ZERO, Keycode.KEYPAD_KEYPAD_PLUS, Keycode.KEYPAD_KEYPAD_MINUS, \
    Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO, Keycode.KEYPAD_THREE, \
    Keycode.KEYPAD_FOUR, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_SIX, \
    Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_EIGHT, Keycode.KEYPAD_NINE ]

```
ここで、keyNoというのが引数でボタン番号と呼ぶことにします。ボタン番号はこのプログラムを見ていただければ容易にわかると思いますが、左下が0で右上が14です。表2を見てもらっても分かるかと思います。
Keycodeには例えば数字の1のコードに Keycode.KEYPAD_ONEとKeycode.ONEがありますが、後者はテンキーではなくキーボードの1です。テンキーの1は前者を使います。
# 入出力の設定
次にラズパイピコの入出力の設定です。boardとdigitalioというライブラリーを使います。
``` py
import board
import digitalio
```
そして例えばGP21を入力に設定するには次のように書きます。これについてはpythonの知識が乏しい筆者がごちゃごちゃ説明するより[ここ](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html)なんかを参照していただければと思います。

``` py
sw1 = digitalio.DigitalInOut(board.GP21)
sw1.direction = digitalio.Direction.INPUT
```
これでラズパイピコのGP28が変数sw1に対応されることになります。そしてこのGP28を内部でpull upするには次のように書きます。
``` py
sw1.pull = digitalio.Pull.UP
```

同様にGP22,GP26,GP27,GP28を設定します。

``` py
sw2 = digitalio.DigitalInOut(board.GP22)
sw2.direction = digitalio.Direction.INPUT
sw2.pull = digitalio.Pull.UP
sw3 = digitalio.DigitalInOut(board.GP26)
sw3.direction = digitalio.Direction.INPUT
sw3.pull = digitalio.Pull.UP
sw4 = digitalio.DigitalInOut(board.GP27)
sw4.direction = digitalio.Direction.INPUT
sw4.pull = digitalio.Pull.UP
sw5 = digitalio.DigitalInOut(board.GP28)
sw5.direction = digitalio.Direction.INPUT
sw5.pull = digitalio.Pull.UP
```

次は出力側です。出力はOpen Drainを使ってLow activeとして使います。Open Drainではなく普通の push/pull (High/Lowの出力ができるタイプ)で High activeの方がわかりやすいのではと思うでしょうが、それだと２つ以上のkeyを同時に押したときにショートする危険性があります。それについては後ほど説明することにしますが、ここでは、Open Drainの Low activeが常識だと理解してください。
入力に割り当てる変数をsw1,sw2,...,sw5としたので出力はswout1,swout2,swout3を割り当てることにします。swout1をGP0にswout2をGP1にswout3をGP2に割り当ててみます。
``` py
swout1 = digitalio.DigitalInOut(board.GP0)
swout1.direction = digitalio.Direction.OUTPUT
swout1.drive_mode = digitalio.DriveMode.OPEN_DRAIN
swout2 = digitalio.DigitalInOut(board.GP1)
swout2.direction = digitalio.Direction.OUTPUT
swout2.drive_mode = digitalio.DriveMode.OPEN_DRAIN
swout3 = digitalio.DigitalInOut(board.GP2)
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

sw5 = define_input_pin(board.GP28)
sw4 = define_input_pin(board.GP27)
sw3 = define_input_pin(board.GP26)
sw2 = define_input_pin(board.GP22)
sw1 = define_input_pin(board.GP21)

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
counterが 0～9ではswout1 つまりGP0が、10～19ではswout2つまりGP1が、20～29ではswout3つまりGP2がactiveになります。counterは30で0にもどります。
プログラムは見やすくするためできる限り短くするのが望ましいです。長いと追うのが大変です。上のプログラムは、 counter をインクリメントしているところは関数にしてしまいます。そのほうが見やすいからです。

``` py
def increment_counter():
    global loopCounter
    loopCounter += 1
    if loopCounter == 30:
        loopCounter = 0
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
    increment_loopCounter(loopCounter)
    if loopCounter == 0:
        gp_output(False,True,True)
    if loopCounter == 10:
        gp_output(True,False,True)
    if loopCounter == 20:
        gp_output(True,True,False)
```

ついでにwhile以下の七行も関数にしてしまいます。アクティブにする出力を切り替える関数なので rotate_outputという名前にします。
```py
def rotate_output():
    global loopCounter
    increment_loopCounter()
    if loopCounter == 0:
        gp_output(False, True, True)
    if loopCounter == 10:
        gp_output(True, False, True)
    if loopCounter == 20:
        gp_output(True, True, False)
```

Falseがactiveというのはなんとなく抵抗があるのでFalseの代わりに0、Treuの代わりに1を使うことにします。こちらだと抵抗は感じないです。あくまで個人の感覚ですが。
```py
def rotate_output():
    global loopCounter
    increment_loopCounter()
    if loopCounter == 0:
        gp_output(0, 1, 1)
    if loopCounter == 10:
        gp_output(1, 0, 1)
    if loopCounter == 20:
        gp_output(1, 1, 0)
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

def get_rowValue(sw5, sw4, sw3, sw2, sw1):
    rowValue = (sw5.value == 0) * 16 + \
            (sw4.value == 0) * 8 + \
            (sw3.value == 0) * 4 + \
            (sw2.value == 0) * 2 + \
            (sw1.value == 0)
    return rowValue

```
sw5を最上位(MSB)にsw1を最下位(LSB)にした5bitのバイナリということになるわけですが、このようにややこしくした理由は二つのキーを同時押しに対応するためです。shift key (S2 = 右下の青色のボタン)を押しながら「-」(S5 )キーを押したときは「Enter」に「3」(S8)
このget_active_columnとget_row_valueで得られる値を元にどのボタンキーが押されたかを示すkeyNoをkeyin関数に渡す関数を作ります。keyin関数の中でホスト側にkeycodeを送信しますが、これは後ほど作ります。
```py
counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CHATTERING_PREVENT_NUM = 100
def decode_key(rowValue, column):
    if ((rowValue == 1) and (column == 2)) or (rowValue == 0):
        if column == 2:
            for keyNo in range(15, 18, 1):
                if counter[keyNo] >= 1:
                    counter[keyNo] -= 1
                if counter[keyNo] == 1:
                    kbd.release(keycode[keyNo])
            for keyNo in range(2, 15, 3):
                if counter[keyNo] >= 1:
                    counter[keyNo] -= 1
                if counter[keyNo] == 1:
                    kbd.release(keycode[keyNo])
        else:
            for keyNo in range(column, 15, 3):
                if counter[keyNo] >= 1:
                    counter[keyNo] -= 1
                if counter[keyNo] == 1:
                    kbd.release(keycode[keyNo])
    else:
        keyNo = get_keyNo(rowValue, column)
        if counter[keyNo] <= CHATTERING_PREVENT_NUM:
            counter[keyNo] += 1
        if counter[keyNo] == CHATTERING_PREVENT_NUM:
            kbd.press(keycode[keyNo])


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
0番のキー(ボタンとキーという用語が混在していますが、どちらも同じ意味で使っています。)はS13です。以下、 1->S14, 2->S15, 3->S10, 4->S11, 5->S12, 6->S7, 7->S8, 8->S9, 9->S4, 10->S5, 11->S6, 12->S1, 13->S2, 14->S15 となります。(表2にも書いています。)
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
はrowValueとcolumnからどのキーつまりkeyNoを求める式です。これは表2を眺めていただければわかると思います。で、問題は上のelse以下のコードですね。一見よさそうにも見えますが、これでは、キーを押している間何回もkeyin()を呼ぶことになりホストにkeycodeを送り続けることになります。それではまずいので一回ホストに送ったらそのあとは送らないようにします。でも、それだけだったらカウンターは必要ではなくフラグを使えば済みますが、次に説明するチャタリングを防止するためにカウンターが使われています。
## チャタリングについて
チャタリングとは下の図のようにスイッチを押した時に何回もlow/highを繰り返しながらlowになる現象のことです。スイッチを離したときも同様にlow/highを繰り返しながら最終的にはhighになります。
![](https://storage.googleapis.com/zenn-user-upload/3b7f8cd520bb-20231217.png)
*図 チャタリング*
これを防止するためchattering_prevention_counterを使っています。チャタリングが落ち着くまで待つために使っているわけです。chattering_prevention_counterはキーが押されるといきなりHALF_CHATNUMている間カウントアップされます。chattering_prevention_counterの値が CHATTERING_PREVENT_NUMと等しくなったら初めて keyin()関数を呼び出してホストにキーコードを送信し、chattering_prevention_counterの値は CHATTERING_PREVENT_NUM+1になります。その後keyを押し続けていてもchattering_prevention_counterはカウントアップされないためkeyin()は呼び出されることはありません。キーを離すとchattering_prevention_counterがリセットされ次にキーが押されるまではカウントアップされません。CHATTERING_PREVENT_NUMはチャタリングが落ち着くのに必要な時間分の値をセットしておきます。これが小さな値だとチャタリングのためにchattering_prevention_counterがリセットされ再びカウントアップが始まりkeyin()関数が呼び出されてホストにキーコードを送信してしまいます。
CHATTERING_PREVENT_NUMはチャタリングが落ち着くのに必要な時間に対応する数値ですが、スイッチの特性で値をどれくらいにすればいいかはわかりません。試行錯誤で適切な値を決めます。筆者の作った物ですと10程度の数字ではキーによっては何回も取り込みがされていました。100ぐらいで落ち着きました。100でも取り込みが遅くなるという感覚は全くなかったのでこれを採用したわけです。



# 
最後にメインです。メインは以下の通りでいたって簡単です。

```py
loopCounter = 0
#
while True:
    rotate_output()
    activeColumn = get_active_column(loopCounter)
    rowValue=get_row_value(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)

```


## 補足、Open Drainを使ってLow activeにする理由
![](/images/short.jpg )
もしGP0,GP1,GP2をpush pullを使ってhigh/lowにドライブしていると例えば、図のようにS12('7'のキー)とS13('8'のキー)を同時に押したときにGP0=High, GP1=Low もしくはその逆で赤色の線の経路で大電流が流れます。Open Drainを使っていれば、Highにドライブできないので(1はHigh-Z)このような問題は起きません。

# ソースコード
ソースコード全体は以下になります。
```py:code.py

import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
keycode = [Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_FORWARD_SLASH, 0,
           Keycode.KEYPAD_ZERO, Keycode.KEYPAD_PLUS, Keycode.KEYPAD_MINUS,
           Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO, Keycode.KEYPAD_THREE,
           Keycode.KEYPAD_FOUR, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_SIX,
           Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_EIGHT, Keycode.KEYPAD_NINE,
           Keycode.ENTER, Keycode.BACKSPACE, Keycode.KEYPAD_NUMLOCK]
PADSHIFT = 2
NUMLOCK = 17
ENTER = 15
BACK = 16

def gp_output(value1, value2, value3):
    swout1.value = value1
    swout2.value = value2
    swout3.value = value3
#
# swout1, swout2, swout3
def rotate_output():
    global loopCounter
    increment_loopCounter()
    if loopCounter == 0:
        gp_output(0, 1, 1)
    if loopCounter == 10:
        gp_output(1, 0, 1)
    if loopCounter == 20:
        gp_output(1, 1, 0)

def increment_loopCounter():
    global loopCounter
    loopCounter += 1
    if loopCounter == 30:
        loopCounter = 0


def get_active_column(switch):
    if switch < 10:
        return 0
    if switch < 20:
        return 1
    return 2

def get_rowValue(sw5, sw4, sw3, sw2, sw1):
    rawValue = (sw5.value == 0) * 16 + \
            (sw4.value == 0) * 8 + \
            (sw3.value == 0) * 4 + \
            (sw2.value == 0) * 2 + \
            (sw1.value == 0)
    return rawValue

def get_keyNo(rowValue, column):
    if rowValue == 16:
        return 12 + column
    if rowValue == 8:
        return 9 + column
    if rowValue == 4:
        return 6 + column
    if rowValue == 2:
        return 3 + column
    if rowValue == 1:
        return column
    if rowValue == 17:
        return NUMLOCK
    if rowValue == 5:
        return BACK
    if rowValue == 3:
        return ENTER

chattering_prevention_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

CHATTERING_PREVENT_NUM = 100
HALF_OF_CHATNUM = 50

def key_release(keyNo):
    if chattering_prevention_counter[keyNo] == CHATTERING_PREVENT_NUM:
        chattering_prevention_counter[keyNo] = HALF_OF_CHATNUM
    if chattering_prevention_counter[keyNo] >= 1:
        chattering_prevention_counter[keyNo] -= 1
    if chattering_prevention_counter[keyNo] == 1:
        kbd.release(keycode[keyNo])


def key_press(keyNo):
    if chattering_prevention_counter[keyNo] == 0:
        chattering_prevention_counter[keyNo] = HALF_OF_CHATNUM
    if chattering_prevention_counter[keyNo] <= CHATTERING_PREVENT_NUM:
        chattering_prevention_counter[keyNo] += 1
    if chattering_prevention_counter[keyNo] == CHATTERING_PREVENT_NUM:
        kbd.press(keycode[keyNo])


def decode_key(rowValue, column):
    if ((rowValue == 1) and (column == 2)) or (rowValue == 0):
        if column == 2:
            for keyNo in range(15, 18, 1):
                key_release(keyNo)
            for keyNo in range(5, 15, 3):
                key_release(keyNo)
        else:
            for keyNo in range(column, 15, 3):
                key_release(keyNo)
    else:
        keyNo = get_keyNo(rowValue, column)
        key_press(keyNo)

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

swout3 = define_output_pin(board.GP2)
swout2 = define_output_pin(board.GP1)
swout1 = define_output_pin(board.GP0)
#
# swout1, swout2, swout3
gp_output(0, 1, 1)
#
loopCounter = 0
#
while True:
    rotate_output()
    activeColumn = get_active_column(loopCounter)
    rowValue = get_rowValue(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)

#
```
# おわりに
ラズパイピコは700円ぐらいで買えるマイコンで手軽に電子工作が楽しめます。pythonでなくてもCなどの言語でも動きますが、今回は不慣れな言語にも挑戦しようと思いpythonでプログラミングをしてみました。pythonはちょっととっつきにくいところがあります。一番違和感があったのは、ミュータブルかイミュータブルかでまるで扱いが違うということです。上のプログラムではglobalに loopCounterというイミュータブルなオブジェクトをincrement_loopCounter()という関数の中でインクリメントしていますが、この関数の中でloopCounterはglobalだという宣言をしています。そうしないとエラーになります。ところが、chattering_prevention_counterというオブジェクトはリストでこちらはミュータブルです。これも key_press()とkey_release()という関数でインクリメントしたりデクリメントしたりしてますがこちらはミュータブルなので global宣言していませんがエラーになりません。同様にCHATTERING_PREVENT_NUMとHALF_OF_CHATNUMをkey_press()とkey_release()でglobal宣言せずに参照していますが、エラーになりません。参照するだけならglobal宣言は必要ないと言うことです。このあたりはpythonの超初心者の私には非常に抵抗がありますね。
